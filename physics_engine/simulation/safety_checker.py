class SafetyChecker:
    """
    Checks industrial system values against safety limits.
    """

    def __init__(
        self,
        max_pump_speed_rpm: float = 5000.0,
        max_pipe_pressure_psi: float = 100.0,
        max_tank_level_liters: float = 10000.0,
    ):
        self.max_pump_speed_rpm = max_pump_speed_rpm
        self.max_pipe_pressure_psi = max_pipe_pressure_psi
        self.max_tank_level_liters = max_tank_level_liters

    def check_pump_speed(self, speed_rpm: float) -> dict:
        """Check whether pump speed is within the safe limit."""
        if speed_rpm < 0:
            return {
                "status": "CRITICAL",
                "message": "Pump speed cannot be negative.",
            }

        if speed_rpm > self.max_pump_speed_rpm:
            return {
                "status": "CRITICAL",
                "message": "Pump speed exceeds the safe limit.",
            }

        return {
            "status": "NORMAL",
            "message": "Pump speed is within the safe limit.",
        }

    def check_pipe_pressure(self, pressure_psi: float) -> dict:
        """Check whether pipe pressure is within the safe limit."""
        if pressure_psi < 0:
            return {
                "status": "CRITICAL",
                "message": "Pipe pressure cannot be negative.",
            }

        if pressure_psi > self.max_pipe_pressure_psi:
            return {
                "status": "CRITICAL",
                "message": "Pipe pressure exceeds the safe limit.",
            }

        return {
            "status": "NORMAL",
            "message": "Pipe pressure is within the safe limit.",
        }

    def check_tank_level(self, level_liters: float) -> dict:
        """Check whether tank level is within capacity."""
        if level_liters < 0:
            return {
                "status": "CRITICAL",
                "message": "Tank level cannot be negative.",
            }

        if level_liters > self.max_tank_level_liters:
            return {
                "status": "CRITICAL",
                "message": "Tank level exceeds tank capacity.",
            }

        return {
            "status": "NORMAL",
            "message": "Tank level is within capacity.",
        }

    def check_system(
        self,
        pump_speed_rpm: float,
        pipe_pressure_psi: float,
        tank_level_liters: float,
    ) -> dict:
        """Run all safety checks and return a combined system result."""

        pump_result = self.check_pump_speed(pump_speed_rpm)
        pressure_result = self.check_pipe_pressure(pipe_pressure_psi)
        tank_result = self.check_tank_level(tank_level_liters)

        checks = {
            "pump": pump_result,
            "pipe_pressure": pressure_result,
            "tank": tank_result,
        }

        critical_items = [
            name
            for name, result in checks.items()
            if result["status"] == "CRITICAL"
        ]

        overall_status = "CRITICAL" if critical_items else "NORMAL"

        return {
            "overall_status": overall_status,
            "checks": checks,
            "critical_items": critical_items,
        }