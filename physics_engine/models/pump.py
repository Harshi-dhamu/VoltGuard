class Pump:
    """
    Represents the pump in the VoltGuard industrial pipeline model.
    """

    def __init__(
        self,
        device_id: str = "PUMP_01",
        min_speed_rpm: float = 0.0,
        max_speed_rpm: float = 5000.0,
    ):
        self.device_id = device_id
        self.min_speed_rpm = min_speed_rpm
        self.max_speed_rpm = max_speed_rpm
        self.speed_rpm = 0.0

    def set_speed(self, speed_rpm: float) -> None:
        """Set pump speed after validating the operating range."""
        if speed_rpm < self.min_speed_rpm:
            raise ValueError("Pump speed cannot be below the minimum limit.")

        if speed_rpm > self.max_speed_rpm:
            raise ValueError("Pump speed exceeds the maximum operating limit.")

        self.speed_rpm = float(speed_rpm)

    def is_within_limits(self) -> bool:
        """Return True when the pump speed is within its safe operating range."""
        return self.min_speed_rpm <= self.speed_rpm <= self.max_speed_rpm

    def get_state(self) -> dict:
        """Return the current pump state."""
        return {
            "device_id": self.device_id,
            "speed_rpm": self.speed_rpm,
            "min_speed_rpm": self.min_speed_rpm,
            "max_speed_rpm": self.max_speed_rpm,
            "within_limits": self.is_within_limits(),
        }