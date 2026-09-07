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


def create_system():
    tank = Tank(capacity_liters=10000.0)

    flow_calculator = FlowCalculator(max_flow_lpm=100.0)
    tank_simulator = TankSimulator(tank)
    safety_checker = SafetyChecker()

    return SystemIntegrator(
        flow_calculator=flow_calculator,
        tank_simulator=tank_simulator,
        safety_checker=safety_checker,
    )


def main():
    # =========================================================
    # TEST 1: NORMAL PROCESS
    # =========================================================

    system = create_system()

    normal_result = system.run_cycle(
        pump_speed_rpm=2500,
        valve_position_percent=50,
        initial_tank_level_liters=5000,
        time_minutes=10,
        pipe_pressure_psi=60,
    )

    print("=== VoltGuard Integrated System Test ===")

    print("\nFlow:")
    print(normal_result["flow"])

    print("\nTank:")
    print(normal_result["tank"])

    print("\nSafety:")
    print(normal_result["safety"])

    print("\nAsset Telemetry:")
    print(normal_result["telemetry"])

    print("\nHealth Summary:")
    print(normal_result["health_summary"])

    print("\nIntegration Event:")
    print(normal_result["integration_event"])

    # Normal condition must not create an anomaly event.
    assert normal_result["safety"]["overall_status"] == "NORMAL"
    assert normal_result["integration_event"] is None

    print("\nNormal condition Integration Event check: PASSED")

    # =========================================================
    # TEST 2: CRITICAL PROCESS
    # =========================================================

    system = create_system()

    critical_result = system.run_cycle(
    pump_speed_rpm=4000,
    valve_position_percent=50,
    initial_tank_level_liters=5000,
    time_minutes=10,
    pipe_pressure_psi=120,
)
    print("\n\n=== Critical Process Test ===")

    print("\nSafety:")
    print(critical_result["safety"])

    print("\nIntegration Event:")
    print(critical_result["integration_event"])

    event = critical_result["integration_event"]

    # Critical condition must create an event.
    assert event is not None

    # =========================================================
    # IntegrationEvent CONTRACT
    # =========================================================

    assert set(event.keys()) == {
        "event_id",
        "source_module",
        "event_type",
        "timestamp",
        "severity",
        "asset",
        "message",
        "payload",
    }

    assert event["event_id"]
    assert event["source_module"] == "physics_engine"
    assert event["event_type"] == "PROCESS_ANOMALY"
    assert event["timestamp"]
    assert event["severity"] == "CRITICAL"
    assert event["asset"]
    assert event["message"]

    # =========================================================
    # PAYLOAD
    # =========================================================

    assert isinstance(event["payload"], dict)

    assert "anomaly_score" in event["payload"]
    assert "category" in event["payload"]
    assert "details" in event["payload"]
    assert "flow" in event["payload"]
    assert "tank" in event["payload"]
    assert "safety" in event["payload"]
    assert "telemetry" in event["payload"]
    assert "health_summary" in event["payload"]

    # =========================================================
    # VERIFY CRITICAL DATA
    # =========================================================

    assert event["payload"]["anomaly_score"] == 0.94
    assert event["payload"]["category"] == "SAFETY ANOMALY"

    assert (
        event["payload"]["safety"]["overall_status"]
        == "CRITICAL"
    )

    print("\nCritical Integration Event checks: PASSED")

    print("\n=== All System Integration Checks PASSED ===")


if __name__ == "__main__":
    main()