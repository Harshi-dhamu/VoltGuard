import sys
from pathlib import Path

# Add the project root to Python's import path
PROJECT_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(PROJECT_ROOT))

from physics_engine.models.tank import Tank
from physics_engine.simulation.tank_simulator import TankSimulator


def main():
    tank = Tank(capacity_liters=10000.0)
    simulator = TankSimulator(tank)

    # Test 1: Fill tank
    fill_state = simulator.get_simulation_state(
        initial_level_liters=5000,
        flow_rate_lpm=25,
        time_minutes=10,
    )

    print("Fill Test:")
    print(fill_state)

    # Test 2: Drain tank
    drain_state = simulator.get_simulation_state(
        initial_level_liters=5000,
        flow_rate_lpm=-20,
        time_minutes=10,
    )

    print("\nDrain Test:")
    print(drain_state)


if __name__ == "__main__":
    main()