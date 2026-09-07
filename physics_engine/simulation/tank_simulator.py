class TankSimulator:
    """
    Simulates tank level changes based on flow rate and time.
    """

    def __init__(self, tank):
        self.tank = tank

    def calculate_level_after_time(
        self,
        initial_level_liters: float,
        flow_rate_lpm: float,
        time_minutes: float,
    ) -> float:
        """
        Calculate tank level after a given amount of time.

        Positive flow fills the tank.
        Negative flow drains the tank.
        """
        if initial_level_liters < 0:
            raise ValueError("Initial tank level cannot be negative.")

        if initial_level_liters > self.tank.capacity_liters:
            raise ValueError("Initial tank level exceeds tank capacity.")

        if time_minutes < 0:
            raise ValueError("Time cannot be negative.")

        level_change = flow_rate_lpm * time_minutes
        final_level = initial_level_liters + level_change

        if final_level < 0:
            final_level = 0.0

        if final_level > self.tank.capacity_liters:
            final_level = self.tank.capacity_liters

        return final_level

    def get_simulation_state(
        self,
        initial_level_liters: float,
        flow_rate_lpm: float,
        time_minutes: float,
    ) -> dict:
        """Return the tank simulation result."""
        final_level = self.calculate_level_after_time(
            initial_level_liters,
            flow_rate_lpm,
            time_minutes,
        )

        return {
            "initial_level_liters": initial_level_liters,
            "flow_rate_lpm": flow_rate_lpm,
            "time_minutes": time_minutes,
            "final_level_liters": final_level,
            "final_fill_percentage": (
                final_level / self.tank.capacity_liters
            ) * 100,
        }