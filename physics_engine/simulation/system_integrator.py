from telemetry_service import TelemetryService
from health_summary_service import HealthSummaryService
from integration_event_adapter import IntegrationEventAdapter
from anomaly_detector import AnomalyDetector


class SystemIntegrator:
    """
    Integrates the complete Physics Engine pipeline:

    Flow calculation
    -> Tank simulation
    -> Safety checking
    -> Asset telemetry
    -> Health summary
    -> Anomaly detection
    -> Integration event generation
    """

    def __init__(
        self,
        flow_calculator,
        tank_simulator,
        safety_checker,
        telemetry_service=None,
        anomaly_detector=None,
    ):
        self.flow_calculator = flow_calculator
        self.tank_simulator = tank_simulator
        self.safety_checker = safety_checker

        self.telemetry_service = (
            telemetry_service or TelemetryService()
        )

        self.health_summary_service = HealthSummaryService()

        self.integration_event_adapter = (
            IntegrationEventAdapter()
        )

        self.anomaly_detector = (
            anomaly_detector or AnomalyDetector()
        )

    def run_cycle(
        self,
        pump_speed_rpm: float,
        valve_position_percent: float,
        initial_tank_level_liters: float,
        time_minutes: float,
        pipe_pressure_psi: float,
    ) -> dict:

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

        telemetry_state = (
            self.telemetry_service.build_asset_telemetry(
                flow_data=flow_state,
                tank_data=tank_state,
                safety_data=safety_state,
            )
        )

        # =====================================================
        # STEP 5: HEALTH SUMMARY
        # =====================================================

        health_summary = (
            self.health_summary_service.build_health_summary(
                telemetry_data=telemetry_state,
            )
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

            anomalies = anomaly_state["anomalies"]

            first_anomaly = anomalies[0]

            # Determine severity
            if safety_state["overall_status"] == "CRITICAL":
                severity = "CRITICAL"
                status = "CATASTROPHIC_FAILURE"
                health_score = 6.0

            else:
                severity = "HIGH"
                status = "ANOMALY_DETECTED"
                health_score = 18.0

            # Determine category
            anomaly_type = first_anomaly["type"]

            if anomaly_type == "PRESSURE_ANOMALY":
                category = "PRESSURE ANOMALY"

            elif anomaly_type == "FLOW_ANOMALY":
                category = "FLOW ANOMALY"

            elif anomaly_type == "PUMP_SPEED_ANOMALY":
                category = "COMMAND ANOMALY"

            elif anomaly_type == "TANK_LEVEL_ANOMALY":
                category = "TANK ANOMALY"

            else:
                category = "PROCESS ANOMALY"

            # Build event
            integration_event = (
                self.integration_event_adapter
                .build_process_anomaly_event(
                    severity=severity,
                    asset=first_anomaly.get(
                        "asset",
                        "PUMP_01",
                    ),
                    message=first_anomaly.get(
                        "message",
                        "Abnormal process behaviour detected",
                    ),
                    anomaly_score=0.94
                    if severity == "CRITICAL"
                    else 0.82,
                    category=category,
                    details={
                        "anomaly_count": anomaly_state[
                            "anomaly_count"
                        ],
                        "anomalies": anomalies,
                        "reason": (
                            "Physics Engine anomaly detector "
                            "identified abnormal process behaviour."
                        ),
                    },
                    flow_data=flow_state,
                    tank_data=tank_state,
                    safety_data=safety_state,
                    telemetry_data=telemetry_state,
                    health_summary=health_summary,
                )
            )

            # Add additional integration payload
            integration_event["payload"].update(
                {
                    "predicted_pressure": flow_state.get(
                        "predicted_pressure_psi",
                        pipe_pressure_psi,
                    ),
                    "pressure_limit": (
                        self.safety_checker
                        .max_pipe_pressure_psi
                    ),
                    "predicted_flow": flow_state.get(
                        "predicted_flow_lpm",
                        flow_state.get(
                            "pump_flow_lpm",
                            0.0,
                        ),
                    ),
                    "pump_speed": pump_speed_rpm,
                    "status": status,
                    "health_score": health_score,
                }
            )

        # =====================================================
        # STEP 8: RETURN COMPLETE SYSTEM RESULT
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