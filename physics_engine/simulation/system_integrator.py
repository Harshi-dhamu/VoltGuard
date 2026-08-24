from telemetry_service import TelemetryService
from health_summary_service import HealthSummaryService


class SystemIntegrator:
    """
    Integrates flow calculation, tank simulation,
    safety checking, and asset telemetry into
    one system workflow.
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

        # Keep telemetry service optional for backward compatibility.
        self.telemetry_service = telemetry_service or TelemetryService()
        self.health_summary_service = HealthSummaryService()

    def run_cycle(
        self,
        pump_speed_rpm: float,
        valve_position_percent: float,
        initial_tank_level_liters: float,
        time_minutes: float,
        pipe_pressure_psi: float,
    ) -> dict:
        """
        Run one complete simulation cycle.
        """

        # Step 1: Calculate pump and actual flow
        flow_state = self.flow_calculator.get_flow_state(
            pump_speed_rpm=pump_speed_rpm,
            valve_position_percent=valve_position_percent,
        )

        actual_flow_lpm = flow_state["actual_flow_lpm"]

        # Step 2: Simulate tank level
        tank_state = self.tank_simulator.get_simulation_state(
            initial_level_liters=initial_tank_level_liters,
            flow_rate_lpm=actual_flow_lpm,
            time_minutes=time_minutes,
        )

        # Step 3: Check system safety
        safety_state = self.safety_checker.check_system(
            pump_speed_rpm=pump_speed_rpm,
            pipe_pressure_psi=pipe_pressure_psi,
            tank_level_liters=tank_state["final_level_liters"],
        )

        # Step 4: Build structured asset telemetry
        telemetry_state = self.telemetry_service.build_asset_telemetry(
            flow_data=flow_state,
            tank_data=tank_state,
            safety_data=safety_state,
        )

        # Step 5: Build health summary
        health_summary = self.health_summary_service.build_health_summary(
            telemetry_data=telemetry_state,
        )

        # Step 6: Combine everything
        return {
            "flow": flow_state,
            "tank": tank_state,
            "safety": safety_state,
            "telemetry": telemetry_state,
            "health_summary": health_summary,
        }