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

    print("=== VoltGuard Integrated Health Summary Test ===")

    # Validate top-level sections
    required_sections = {
        "flow",
        "tank",
        "safety",
        "telemetry",
        "health_summary",
    }

    missing_sections = required_sections - result.keys()

    if missing_sections:
        print("Validation FAILED.")
        print(f"Missing sections: {sorted(missing_sections)}")
        return

    # Validate health summary
    health_summary = result["health_summary"]

    if health_summary["total_assets"] != 4:
        print("Validation FAILED.")
        print("Expected 4 assets.")
        return

    if health_summary["normal_assets"] != 4:
        print("Validation FAILED.")
        print("Expected 4 normal assets.")
        return

    print("\nValidation Result: PASSED")
    print(f"System Status: {health_summary['system_status']}")
    print(f"Total Assets: {health_summary['total_assets']}")
    print(f"Normal Assets: {health_summary['normal_assets']}")
    print(f"Warning Assets: {health_summary['warning_assets']}")
    print(f"Critical Assets: {health_summary['critical_assets']}")

    print("\nIntegrated health summary validation successful.")


if __name__ == "__main__":
    main()