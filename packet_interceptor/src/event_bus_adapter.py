import time
from typing import Dict, Any, List, Optional
from src.logger import setup_logger

logger = setup_logger()

class EventBusAdapter:
    """Formats and dispatches Packet Interceptor anomalies to the VoltGuard EventBus."""

    def __init__(self):
        self.published_events: List[Dict[str, Any]] = []

    def format_integration_event(self, analyzed_command: Dict[str, Any]) -> Dict[str, Any]:
        """Converts normalized/analyzed packet dict into standard IntegrationEvent schema."""
        is_suspicious = analyzed_command.get("is_suspicious", False)
        reason = analyzed_command.get("suspicious_reason", "NONE")
        value = analyzed_command.get("value", 0)
        unit = analyzed_command.get("unit", "")
        asset_id = analyzed_command.get("device_id", "UNKNOWN_ASSET")

        severity = "HIGH" if is_suspicious else "INFO"
        if value > 10000:
            severity = "CRITICAL"

        event_payload = {
            "source_module": "packet_interceptor",
            "event_type": "NETWORK_ANOMALY" if is_suspicious else "NETWORK_TRAFFIC",
            "severity": severity,
            "asset_id": asset_id,
            "message": f"Parameter anomaly detected on {asset_id}: {reason} ({value} {unit})",
            "timestamp": time.time(),
            "detection_details": {
                "transaction_id": analyzed_command.get("transaction_id", 0),
                "function_code": analyzed_command.get("function_code", 0),
                "register_address": analyzed_command.get("register_address", 0),
                "command": analyzed_command.get("command", "UNKNOWN"),
                "value": value,
                "unit": unit,
                "is_suspicious": is_suspicious,
                "suspicious_reason": reason
            }
        }
        return event_payload

    def publish_event(self, analyzed_command: Dict[str, Any]) -> Dict[str, Any]:
        """Publishes formatted event payload to EventBus queue."""
        event = self.format_integration_event(analyzed_command)
        self.published_events.append(event)
        logger.info(f"[EVENT BUS] Published {event['event_type']} ({event['severity']}) for {event['asset_id']}")
        return event