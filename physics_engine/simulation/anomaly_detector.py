class AnomalyDetector:
    """
    Detects physical process anomalies from
    Physics Engine simulation output.
    """

    def detect(
        self,
        flow_data: dict,
        tank_data: dict,
        safety_data: dict,
    ) -> dict:
        anomalies = []

        # -----------------------------
        # Pump speed anomaly
        # -----------------------------
        pump_speed = flow_data.get("pump_speed_rpm")

        if pump_speed is not None:
            if pump_speed < 0:
                anomalies.append({
                    "type": "PUMP_SPEED_ANOMALY",
                    "asset": "PUMP_01",
                    "value": pump_speed,
                    "message": "Pump speed cannot be negative.",
                })

            elif pump_speed > 5000:
                anomalies.append({
                    "type": "PUMP_SPEED_ANOMALY",
                    "asset": "PUMP_01",
                    "value": pump_speed,
                    "message": "Pump speed exceeds the physical safety limit.",
                })

        # -----------------------------
        # Pipe pressure anomaly
        # -----------------------------
        pipe_check = safety_data.get("checks", {}).get(
            "pipe_pressure", {}
        )

        if pipe_check.get("status") == "CRITICAL":
            anomalies.append({
                "type": "PRESSURE_ANOMALY",
                "asset": "PIPE_01",
                "message": pipe_check.get(
                    "message",
                    "Abnormal pipe pressure detected.",
                ),
            })

        # -----------------------------
        # Tank level anomaly
        # -----------------------------
        tank_level = tank_data.get("final_level_liters")

        if tank_level is not None:
            if tank_level < 0:
                anomalies.append({
                    "type": "TANK_LEVEL_ANOMALY",
                    "asset": "TANK_01",
                    "value": tank_level,
                    "message": "Tank level cannot be negative.",
                })

            elif tank_level > 10000:
                anomalies.append({
                    "type": "TANK_LEVEL_ANOMALY",
                    "asset": "TANK_01",
                    "value": tank_level,
                    "message": "Tank level exceeds tank capacity.",
                })

        # -----------------------------
        # Flow anomaly
        # -----------------------------
        actual_flow = flow_data.get("actual_flow_lpm")
        pump_flow = flow_data.get("pump_flow_lpm")

        if actual_flow is not None and actual_flow < 0:
            anomalies.append({
                "type": "FLOW_ANOMALY",
                "asset": "PUMP_01",
                "value": actual_flow,
                "message": "Actual flow cannot be negative.",
            })

        if (
            actual_flow is not None
            and pump_flow is not None
            and pump_flow > 0
            and actual_flow < pump_flow * 0.25
        ):
            anomalies.append({
                "type": "FLOW_ANOMALY",
                "asset": "PUMP_01",
                "value": actual_flow,
                "expected": pump_flow,
                "message": "Actual flow is significantly below expected pump flow.",
            })

        return {
            "anomaly_detected": len(anomalies) > 0,
            "anomaly_count": len(anomalies),
            "anomalies": anomalies,
        }