class FlowCalculator:
    """
    Calculates the estimated and actual flow through the system.
    """

    def __init__(self, max_flow_lpm: float = 100.0):
        self.max_flow_lpm = max_flow_lpm

    def calculate_pump_flow(self, pump_speed_rpm: float) -> float:
        """
        Calculate pump flow based on pump speed.

        5000 RPM is treated as the maximum reference speed.
        """
        if pump_speed_rpm < 0:
            raise ValueError("Pump speed cannot be negative.")

        if pump_speed_rpm > 5000:
            raise ValueError("Pump speed exceeds the supported range.")

        return (pump_speed_rpm / 5000.0) * self.max_flow_lpm

    def calculate_actual_flow(
        self,
        pump_speed_rpm: float,
        valve_position_percent: float,
    ) -> float:
        """
        Calculate actual flow after applying valve opening.
        """
        if not 0 <= valve_position_percent <= 100:
            raise ValueError("Valve position must be between 0 and 100%.")

        pump_flow = self.calculate_pump_flow(pump_speed_rpm)

        return pump_flow * (valve_position_percent / 100.0)

    def get_flow_state(
        self,
        pump_speed_rpm: float,
        valve_position_percent: float,
    ) -> dict:
        """Return the calculated flow information."""
        pump_flow = self.calculate_pump_flow(pump_speed_rpm)
        actual_flow = self.calculate_actual_flow(
            pump_speed_rpm,
            valve_position_percent,
        )

        return {
            "pump_speed_rpm": pump_speed_rpm,
            "valve_position_percent": valve_position_percent,
            "pump_flow_lpm": pump_flow,
            "actual_flow_lpm": actual_flow,
        }