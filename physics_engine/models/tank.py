class Tank:
    """
    Represents the storage tank in the VoltGuard industrial system.
    """

    def __init__(
        self,
        device_id: str = "TANK_01",
        capacity_liters: float = 10000.0,
        max_pressure_psi: float = 100.0,
    ):
        self.device_id = device_id
        self.capacity_liters = capacity_liters
        self.max_pressure_psi = max_pressure_psi
        self.level_liters = 0.0

    def set_level(self, level_liters: float) -> None:
        """Set the tank level after validating its capacity."""
        if level_liters < 0:
            raise ValueError("Tank level cannot be negative.")

        if level_liters > self.capacity_liters:
            raise ValueError("Tank level exceeds tank capacity.")

        self.level_liters = float(level_liters)

    def get_fill_percentage(self) -> float:
        """Return the current tank fill percentage."""
        if self.capacity_liters == 0:
            return 0.0

        return (self.level_liters / self.capacity_liters) * 100

    def get_state(self) -> dict:
        """Return the current tank state."""
        return {
            "device_id": self.device_id,
            "capacity_liters": self.capacity_liters,
            "level_liters": self.level_liters,
            "fill_percentage": self.get_fill_percentage(),
            "max_pressure_psi": self.max_pressure_psi,
        }