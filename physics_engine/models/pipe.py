class Pipe:
    """
    Represents the pipeline section in the VoltGuard industrial system.
    """

    def __init__(
        self,
        device_id: str = "PIPE_01",
        length_m: float = 100.0,
        diameter_m: float = 0.1,
        max_pressure_psi: float = 100.0,
    ):
        self.device_id = device_id
        self.length_m = length_m
        self.diameter_m = diameter_m
        self.max_pressure_psi = max_pressure_psi

    def get_state(self) -> dict:
        """Return the pipe configuration and operating limit."""
        return {
            "device_id": self.device_id,
            "length_m": self.length_m,
            "diameter_m": self.diameter_m,
            "max_pressure_psi": self.max_pressure_psi,
        }