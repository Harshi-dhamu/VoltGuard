import sys
from pathlib import Path

# Add project root to Python path
PROJECT_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(PROJECT_ROOT))

from physics_engine.simulation.safety_checker import SafetyChecker


def main():
    checker = SafetyChecker()

    # Test 1: Normal system
    normal_result = checker.check_system(
        pump_speed_rpm=2500,
        pipe_pressure_psi=60,
        tank_level_liters=5000,
    )

    print("Normal System Test:")
    print(normal_result)

    # Test 2: Critical pump speed
    pump_result = checker.check_system(
        pump_speed_rpm=6000,
        pipe_pressure_psi=60,
        tank_level_liters=5000,
    )

    print("\nPump Safety Test:")
    print(pump_result)

    # Test 3: Critical pipe pressure
    pressure_result = checker.check_system(
        pump_speed_rpm=2500,
        pipe_pressure_psi=150,
        tank_level_liters=5000,
    )

    print("\nPressure Safety Test:")
    print(pressure_result)

    # Test 4: Critical tank level
    tank_result = checker.check_system(
        pump_speed_rpm=2500,
        pipe_pressure_psi=60,
        tank_level_liters=12000,
    )

    print("\nTank Safety Test:")
    print(tank_result)


if __name__ == "__main__":
    main()