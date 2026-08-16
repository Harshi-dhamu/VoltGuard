import sys
from pathlib import Path

# Add project root to Python path
PROJECT_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(PROJECT_ROOT))

from physics_engine.models.tank import Tank
from physics_engine.simulation.flow_calculator import FlowCalculator
from physics_engine.simulation.tank_simulator import TankSimulator
from physics_engine.simulation.safety_checker import SafetyChecker
from physics_engine.simulation.system_integrator import SystemIntegrator


def main():
    # Create system components
    tank = Tank(capacity_liters=10000.0)

    flow_calculator = FlowCalculator(max_flow_lpm=100.0)
    tank_simulator = TankSimulator(tank)
    safety_checker = SafetyChecker()

    # Create integrated system
    system = SystemIntegrator(
        flow_calculator=flow_calculator,
        tank_simulator=tank_simulator,
        safety_checker=safety_checker,
    )

    # Run one complete cycle
    result = system.run_cycle(
        pump_speed_rpm=2500,
        valve_position_percent=50,
        initial_tank_level_liters=5000,
        time_minutes=10,
        pipe_pressure_psi=60,
    )

    print("=== VoltGuard Integrated System Test ===")

    print("\nFlow:")
    print(result["flow"])

    print("\nTank:")
    print(result["tank"])

    print("\nSafety:")
    print(result["safety"])


if __name__ == "__main__":
    main()