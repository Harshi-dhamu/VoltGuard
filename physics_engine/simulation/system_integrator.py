from telemetry_service import TelemetryService
from health_summary_service import HealthSummaryService
from integration_event_adapter import IntegrationEventAdapter
from anomaly_detector import AnomalyDetector


class SystemIntegrator:
    """
    Integrates:
    - Flow calculation
    - Tank simulation
    - Safety checking
    - Asset telemetry
    - Health summary
    - Anomaly detection
    - Integration event generation
    """

    def __init__(
        self,
        flow_calculator,
        tank_simulator,
        safety_checker,
        telemetry_service=None,
    ):
        self.flow_calculator = flow_calculator
        self.tank_simulator = tank_simulator
        self.safety_checker = safety_checker

        # Services
        self.telemetry_service = telemetry_service or TelemetryService()
        self.health_summary_service = HealthSummaryService()

        # Integration event adapter
        self.integration_event_adapter = IntegrationEventAdapter()

        # Anomaly detector
        self.anomaly_detector = AnomalyDetector()

    def run_cycle(
        self,
        pump_speed_rpm: float,
        valve_position_percent: float,
        initial_tank_level_liters: float,
        time_minutes: float,
        pipe_pressure_psi: float,
    ) -> dict:
        """
        Run one complete Physics Engine simulation cycle.
        """

        # =====================================================
        # STEP 1: FLOW CALCULATION
        # =====================================================

        flow_state = self.flow_calculator.get_flow_state(
            pump_speed_rpm=pump_speed_rpm,
            valve_position_percent=valve_position_percent,
        )

        actual_flow_lpm = flow_state["actual_flow_lpm"]

        # =====================================================
        # STEP 2: TANK SIMULATION
        # =====================================================

        tank_state = self.tank_simulator.get_simulation_state(
            initial_level_liters=initial_tank_level_liters,
            flow_rate_lpm=actual_flow_lpm,
            time_minutes=time_minutes,
        )

        # =====================================================
        # STEP 3: SAFETY CHECK
        # =====================================================

        safety_state = self.safety_checker.check_system(
            pump_speed_rpm=pump_speed_rpm,
            pipe_pressure_psi=pipe_pressure_psi,
            tank_level_liters=tank_state["final_level_liters"],
        )

        # =====================================================
        # STEP 4: ASSET TELEMETRY
        # =====================================================

        telemetry_state = self.telemetry_service.build_asset_telemetry(
            flow_data=flow_state,
            tank_data=tank_state,
            safety_data=safety_state,
        )

        # =====================================================
        # STEP 5: HEALTH SUMMARY
        # =====================================================

        health_summary = self.health_summary_service.build_health_summary(
            telemetry_data=telemetry_state,
        )

        # =====================================================
        # STEP 6: ANOMALY DETECTION
        # =====================================================

        anomaly_state = self.anomaly_detector.detect(
            flow_data=flow_state,
            tank_data=tank_state,
            safety_data=safety_state,
        )

        # =====================================================
        # STEP 7: INTEGRATION EVENT
        # =====================================================

        integration_event = None

        if anomaly_state["anomaly_detected"]:

            anomalies = anomaly_state.get("anomalies", [])

            # Take the most important anomaly
            primary_anomaly = (
                anomalies[0]
                if anomalies
                else {}
            )

            asset = primary_anomaly.get(
                "asset",
                "PROCESS",
            )

            message = primary_anomaly.get(
                "message",
                "Abnormal process behaviour detected.",
            )

            anomaly_score = anomaly_state.get(
                "anomaly_score",
                0.0,
            )

            severity = anomaly_state.get(
                "severity",
                "LOW",
            )

            anomaly_type = primary_anomaly.get(
                "type",
                "PROCESS_ANOMALY",
            )

            # Convert anomaly type into readable category
            category_map = {
                "PUMP_SPEED_ANOMALY": "PUMP SPEED ANOMALY",
                "PRESSURE_ANOMALY": "PRESSURE ANOMALY",
                "TANK_LEVEL_ANOMALY": "TANK LEVEL ANOMALY",
                "FLOW_ANOMALY": "FLOW ANOMALY",
            }

            category = category_map.get(
                anomaly_type,
                "PROCESS ANOMALY",
            )

            # =================================================
            # Calculate event status
            # =================================================

            if severity == "CRITICAL":
                event_status = "CATASTROPHIC_FAILURE"

            elif severity == "HIGH":
                event_status = "ANOMALY_DETECTED"

            elif severity == "MEDIUM":
                event_status = "WARNING"

            else:
                event_status = "NORMAL"

            # =================================================
            # Health score
            # =================================================

            health_score = max(
                0.0,
                round((1.0 - anomaly_score) * 100, 2),
            )

            # =================================================
            # Predicted values
            # =================================================

            predicted_pressure = flow_state.get(
                "predicted_pressure_psi",
                pipe_pressure_psi,
            )

            predicted_flow = flow_state.get(
                "predicted_flow_lpm",
                flow_state.get(
                    "pump_flow_lpm",
                    actual_flow_lpm,
                ),
            )

            # =================================================
            # Event payload
            # =================================================

            details = {
                "anomaly_count": anomaly_state.get(
                    "anomaly_count",
                    0,
                ),
                "anomalies": anomalies,
                "reason": (
                    "Physics Engine anomaly detector "
                    "identified abnormal process behaviour."
                ),
            }

            integration_event = (
                self.integration_event_adapter.build_process_anomaly_event(
                    severity=severity,
                    asset=asset,
                    message=message,
                    anomaly_score=anomaly_score,
                    category=category,
                    details=details,
                    flow_data=flow_state,
                    tank_data=tank_state,
                    safety_data=safety_state,
                    telemetry_data=telemetry_state,
                    health_summary=health_summary,
                )
            )

            # Add additional fields required by the
            # Physics Engine integration contract.
            integration_event["payload"]["predicted_pressure"] = (
                predicted_pressure
            )

            integration_event["payload"]["pressure_limit"] = (
                self.safety_checker.max_pipe_pressure_psi
            )

            integration_event["payload"]["predicted_flow"] = (
                predicted_flow
            )

            integration_event["payload"]["pump_speed"] = (
                pump_speed_rpm
            )

            integration_event["payload"]["status"] = (
                event_status
            )

            integration_event["payload"]["health_score"] = (
                health_score
            )

        # =====================================================
        # STEP 8: FINAL SYSTEM RESULT
        # =====================================================

        return {
            "flow": flow_state,
            "tank": tank_state,
            "safety": safety_state,
            "telemetry": telemetry_state,
            "health_summary": health_summary,
            "anomaly": anomaly_state,
            "integration_event": integration_event,
        }