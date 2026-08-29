class Valve:
    """
    Represents the valve in the VoltGuard industrial pipeline model.
    """

    def __init__(
        self,
        device_id: str = "VALVE_01",
        min_position: float = 0.0,
        max_position: float = 100.0,
    ):
        self.device_id = device_id
        self.min_position = min_position
        self.max_position = max_position
        self.position = 0.0

    def set_position(self, position: float) -> None:
        """Set valve opening percentage after validating the range."""
        if position < self.min_position:
            raise ValueError("Valve position cannot be below 0%.")

        if position > self.max_position:
            raise ValueError("Valve position cannot exceed 100%.")

        self.position = float(position)

    def is_within_limits(self) -> bool:
        """Return True when the valve position is within its operating range."""
        return self.min_position <= self.position <= self.max_position

    def get_state(self) -> dict:
        """Return the current valve state."""
        return {
            "device_id": self.device_id,
            "position_percent": self.position,
            "min_position_percent": self.min_position,
            "max_position_percent": self.max_position,
            "within_limits": self.is_within_limits(),
        }