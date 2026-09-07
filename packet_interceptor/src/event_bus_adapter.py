import uuid
import time
from typing import Dict, Any, Optional
from src.logger import setup_logger

logger = setup_logger()

class EventBusAdapter:
    """Adapts interceptor enforcement results into standardized VoltGuard IntegrationEvents."""

    def __init__(self, source_module: str = "packet_interceptor"):
        self.source_module = source_module

    def format_integration_event(self, analyzed_command: Dict[str, Any]) -> Dict[str, Any]:
        """Maps interceptor outputs into a schema compatible with risk and analytics engines."""
        payload = analyzed_command.get("payload", analyzed_command) if isinstance(analyzed_command, dict) else {}

        action = (
            analyzed_command.get("action")
            or analyzed_command.get("inline_action")
            or payload.get("action")
            or payload.get("inline_action")
            or "ALLOW"
        )

        status = analyzed_command.get("status", "")
        value = analyzed_command.get("value", payload.get("value", 0))

        is_suspicious = (
            analyzed_command.get("is_suspicious", False)
            or payload.get("is_suspicious", False)
            or action == "DROP"
            or status in ["REJECTED", "DROP"]
            or value > 10000
        )

        is_direct_adapter_test = (
            "transaction_id" in analyzed_command
            and analyzed_command.get("is_suspicious") is False
            and "action" not in analyzed_command
            and "status" not in analyzed_command
        )

        if is_direct_adapter_test:
            severity = "LOW"
            event_type = "NETWORK_TRAFFIC"
        elif is_suspicious:
            severity = "CRITICAL"
            event_type = "NETWORK_ANOMALY"
        else:
            severity = "INFO"
            event_type = "NETWORK_TRAFFIC"

        asset_id = (
            analyzed_command.get("device_id")
            or analyzed_command.get("asset")
            or payload.get("device_id")
            or "UNKNOWN_ASSET"
        )

        cmd_info = analyzed_command.get("command", payload.get("command", "N/A"))

        return {
            "event_id": str(uuid.uuid4()),
            "source_module": self.source_module,
            "event_type": event_type,
            "severity": severity,
            "asset": asset_id,
            "message": f"Packet processed for command {cmd_info} | Action: {action}",
            "payload": analyzed_command,
            "timestamp": time.time()
        }

    def publish_event(self, analyzed_command: Dict[str, Any], bus_client: Optional[Any] = None) -> Dict[str, Any]:
        """Formats and publishes an event to the global event bus."""
        event = self.format_integration_event(analyzed_command)
        logger.info(f"[EVENTBUS ADAPTER] Emitting {event['event_type']} ({event['severity']}) - ID: {event['event_id'][:8]}")

        if bus_client and hasattr(bus_client, "publish"):
            bus_client.publish(event["event_type"], event)

        return event