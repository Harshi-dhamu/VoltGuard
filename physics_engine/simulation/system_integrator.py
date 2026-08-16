class SystemIntegrator:
    """
    Integrates flow calculation, tank simulation,
    and safety checking into one system workflow.
    """

    def __init__(self, flow_calculator, tank_simulator, safety_checker):
        self.flow_calculator = flow_calculator
        self.tank_simulator = tank_simulator
        self.safety_checker = safety_checker

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

        # Step 4: Combine everything
        return {
            "flow": flow_state,
            "tank": tank_state,
            "safety": safety_state,
        }