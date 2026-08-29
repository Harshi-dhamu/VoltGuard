from datetime import datetime, timezone
from uuid import uuid4


class IntegrationEventAdapter:
    """
    Converts Physics Engine output into the agreed
    VoltGuard IntegrationEvent contract.

    Dashboard-independent.
    """

    SOURCE_MODULE = "physics_engine"
    EVENT_TYPE = "PROCESS_ANOMALY"

    def build_event(
        self,
        severity: str,
        asset: str,
        message: str,
        payload: dict,
    ) -> dict:
        """
        Build a Physics Engine integration event.

        The returned dictionary follows the agreed
        IntegrationEvent contract.
        """

        return {
            "event_id": str(uuid4()),
            "source_module": self.SOURCE_MODULE,
            "event_type": self.EVENT_TYPE,
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "severity": severity,
            "asset": asset,
            "message": message,
            "payload": payload,
        }

    def build_process_anomaly_event(
        self,
        severity: str,
        asset: str,
        message: str,
        anomaly_score: float,
        category: str,
        details: dict | None = None,
        flow_data: dict | None = None,
        tank_data: dict | None = None,
        safety_data: dict | None = None,
        telemetry_data: dict | None = None,
        health_summary: dict | None = None,
    ) -> dict:
        """
        Build a PROCESS_ANOMALY event containing
        Physics Engine process information.
        """

        payload = {
            "anomaly_score": anomaly_score,
            "category": category,
            "details": details or {},
            "flow": flow_data or {},
            "tank": tank_data or {},
            "safety": safety_data or {},
            "telemetry": telemetry_data or {},
            "health_summary": health_summary or {},
        }

        return self.build_event(
            severity=severity,
            asset=asset,
            message=message,
            payload=payload,
        )