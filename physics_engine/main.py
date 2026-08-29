"""
VoltGuard Physics Engine
Day 1 - Basic Industrial Pipeline Foundation

System:
Pump -> Pipe -> Valve -> Tank
"""


class Pump:
    """Represents the industrial pump."""

    def __init__(self, device_id: str):
        self.device_id = device_id


class Pipe:
    """Represents the industrial pipe."""

    def __init__(self, pipe_id: str):
        self.pipe_id = pipe_id


class Valve:
    """Represents the industrial valve."""

    def __init__(self, device_id: str):
        self.device_id = device_id


class Tank:
    """Represents the industrial tank."""

    def __init__(self, device_id: str):
        self.device_id = device_id


class IndustrialPipeline:
    """Represents the complete mock industrial pipeline."""

    def __init__(
        self,
        pump: Pump,
        pipe: Pipe,
        valve: Valve,
        tank: Tank,
    ):
        self.pump = pump
        self.pipe = pipe
        self.valve = valve
        self.tank = tank

    def describe(self) -> str:
        """Return the pipeline component flow."""

        return (
            f"{self.pump.device_id} -> "
            f"{self.pipe.pipe_id} -> "
            f"{self.valve.device_id} -> "
            f"{self.tank.device_id}"
        )


def main():
    """Create the basic VoltGuard industrial pipeline."""

    pump = Pump("PUMP_01")
    pipe = Pipe("PIPE_01")
    valve = Valve("VALVE_01")
    tank = Tank("TANK_01")

    pipeline = IndustrialPipeline(
        pump=pump,
        pipe=pipe,
        valve=valve,
        tank=tank,
    )

    print("=" * 60)
    print("VoltGuard Physics Engine")
    print("=" * 60)
    print("Industrial Pipeline:")
    print(pipeline.describe())
    print("=" * 60)


if __name__ == "__main__":
    main()