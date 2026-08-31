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
        Build a standard IntegrationEvent dictionary.

        Contract fields:
            event_id
            source_module
            event_type
            timestamp
            severity
            asset
            message
            payload
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
        predicted_pressure: float | None = None,
        pressure_limit: float = 100.0,
        predicted_flow: float | None = None,
        pump_speed: float | None = None,
        status: str | None = None,
        health_score: float | None = None,
    ) -> dict:
        """
        Build a PROCESS_ANOMALY IntegrationEvent.

        This adapter does not depend on the dashboard.
        It only converts Physics Engine information into
        the agreed IntegrationEvent dictionary structure.
        """

        flow_data = flow_data or {}
        tank_data = tank_data or {}
        safety_data = safety_data or {}
        telemetry_data = telemetry_data or {}
        health_summary = health_summary or {}
        details = details or {}

        # -----------------------------------------------------
        # Get process values from flow data when not explicitly
        # supplied.
        # -----------------------------------------------------

        if pump_speed is None:
            pump_speed = flow_data.get("pump_speed_rpm")

        if predicted_flow is None:
            predicted_flow = flow_data.get("actual_flow_lpm")

        # -----------------------------------------------------
        # Pressure information
        # -----------------------------------------------------

        if predicted_pressure is None:
            predicted_pressure = safety_data.get(
                "predicted_pressure",
                safety_data.get("pipe_pressure_psi", 0),
            )

        # -----------------------------------------------------
        # Calculate health score automatically when not supplied.
        #
        # anomaly_score:
        # 0.0 = normal
        # 1.0 = extremely anomalous
        #
        # health_score:
        # 100 = healthy
        # 0 = failed
        # -----------------------------------------------------

        if health_score is None:
            health_score = round(
                max(
                    0.0,
                    min(
                        100.0,
                        (1.0 - anomaly_score) * 100.0,
                    ),
                ),
                2,
            )

        # -----------------------------------------------------
        # Determine process status automatically.
        # -----------------------------------------------------

        if status is None:
            if severity == "CRITICAL" and anomaly_score >= 0.90:
                status = "CATASTROPHIC_FAILURE"
            elif severity in {"HIGH", "CRITICAL"}:
                status = "ANOMALY_DETECTED"
            else:
                status = "NORMAL"

        # -----------------------------------------------------
        # Build payload
        # -----------------------------------------------------

        payload = {
            "anomaly_score": anomaly_score,
            "category": category,

            # Values requested by Harshi
            "predicted_pressure": predicted_pressure,
            "pressure_limit": pressure_limit,
            "predicted_flow": predicted_flow,
            "pump_speed": pump_speed,
            "status": status,
            "health_score": health_score,

            # Detailed Physics Engine information
            "details": details,
            "flow": flow_data,
            "tank": tank_data,
            "safety": safety_data,
            "telemetry": telemetry_data,
            "health_summary": health_summary,
        }

        return self.build_event(
            severity=severity,
            asset=asset,
            message=message,
            payload=payload,
        )