class FlowCalculator:
    """
    Calculates estimated flow, actual flow,
    and predicted process pressure.
    """

    def __init__(self, max_flow_lpm: float = 100.0):
        self.max_flow_lpm = max_flow_lpm

    def calculate_pump_flow(self, pump_speed_rpm: float) -> float:
        """
        Calculate pump flow based on pump speed.

        5000 RPM is treated as the maximum supported
        reference speed.
        """

        if pump_speed_rpm < 0:
            raise ValueError("Pump speed cannot be negative.")

        if pump_speed_rpm > 5000:
            raise ValueError("Pump speed exceeds the supported range.")

        return round(
            (pump_speed_rpm / 5000.0) * self.max_flow_lpm,
            2,
        )

    def calculate_actual_flow(
        self,
        pump_speed_rpm: float,
        valve_position_percent: float,
    ) -> float:
        """
        Calculate actual flow after applying valve opening.
        """

        if not 0 <= valve_position_percent <= 100:
            raise ValueError(
                "Valve position must be between 0 and 100%."
            )

        pump_flow = self.calculate_pump_flow(pump_speed_rpm)

        return round(
            pump_flow * (valve_position_percent / 100.0),
            2,
        )

    def calculate_predicted_pressure(
        self,
        pump_speed_rpm: float,
        predicted_flow_lpm: float,
    ) -> float:
        """
        Estimate predicted process pressure.

        This is a simplified Physics Engine model used
        for process anomaly detection and IntegrationEvent
        generation.

        Reference operating condition:
            2500 RPM
            50 LPM
            approximately 50 PSI
        """

        if pump_speed_rpm < 0:
            raise ValueError(
                "Pump speed cannot be negative."
            )

        if predicted_flow_lpm < 0:
            raise ValueError(
                "Predicted flow cannot be negative."
            )

        speed_component = (
            pump_speed_rpm / 2500.0
        ) * 25.0

        flow_component = (
            predicted_flow_lpm / 50.0
        ) * 25.0

        predicted_pressure = (
            speed_component + flow_component
        )

        return round(predicted_pressure, 2)

    def get_flow_state(
        self,
        pump_speed_rpm: float,
        valve_position_percent: float,
    ) -> dict:
        """
        Return complete flow and pressure prediction state.
        """

        pump_flow = self.calculate_pump_flow(
            pump_speed_rpm
        )

        actual_flow = self.calculate_actual_flow(
            pump_speed_rpm,
            valve_position_percent,
        )

        predicted_pressure = (
            self.calculate_predicted_pressure(
                pump_speed_rpm=pump_speed_rpm,
                predicted_flow_lpm=pump_flow,
            )
        )

        return {
            "pump_speed_rpm": pump_speed_rpm,
            "valve_position_percent": valve_position_percent,
            "pump_flow_lpm": pump_flow,
            "actual_flow_lpm": actual_flow,
            "predicted_flow_lpm": pump_flow,
            "predicted_pressure_psi": predicted_pressure,
        }