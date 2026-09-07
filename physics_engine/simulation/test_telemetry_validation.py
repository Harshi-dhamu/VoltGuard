import sys
from pathlib import Path

# Add project root to Python path
PROJECT_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(PROJECT_ROOT))

from physics_engine.simulation.telemetry_service import TelemetryService


def validate_telemetry(data):
    """
    Validate the structure and basic values of asset telemetry.
    """

    errors = []

    if data.get("system_status") not in {"NORMAL", "WARNING", "CRITICAL", "UNKNOWN"}:
        errors.append("Invalid system status.")

    assets = data.get("assets", {})

    required_assets = {
        "PUMP_01",
        "VALVE_01",
        "PIPE_01",
        "TANK_01",
    }

    missing_assets = required_assets - assets.keys()

    if missing_assets:
        errors.append(f"Missing assets: {sorted(missing_assets)}")

    tank = assets.get("TANK_01", {})

    fill_percentage = tank.get("fill_percentage")

    if fill_percentage is not None:
        if not 0 <= fill_percentage <= 100:
            errors.append("Tank fill percentage is outside 0-100 range.")

    valve = assets.get("VALVE_01", {})

    position = valve.get("position_percent")

    if position is not None:
        if not 0 <= position <= 100:
            errors.append("Valve position is outside 0-100 range.")

    telemetry = data.get("telemetry", {})

    actual_flow = telemetry.get("actual_flow_lpm")

    if actual_flow is not None and actual_flow < 0:
        errors.append("Actual flow cannot be negative.")

    return {
        "valid": len(errors) == 0,
        "errors": errors,
    }


def main():
    service = TelemetryService()

    flow_data = {
        "pump_speed_rpm": 2500,
        "valve_position_percent": 50,
        "pump_flow_lpm": 50.0,
        "actual_flow_lpm": 25.0,
    }

    tank_data = {
        "final_level_liters": 5250.0,
        "final_fill_percentage": 52.5,
    }

    safety_data = {
        "overall_status": "NORMAL",
        "checks": {
            "pump": {"status": "NORMAL"},
            "pipe_pressure": {"status": "NORMAL"},
            "tank": {"status": "NORMAL"},
        },
    }

    telemetry = service.build_asset_telemetry(
        flow_data=flow_data,
        tank_data=tank_data,
        safety_data=safety_data,
    )

    validation = validate_telemetry(telemetry)

    print("=== VoltGuard Telemetry Validation Test ===")
    print()
    print("Validation Result:")
    print(validation)

    if validation["valid"]:
        print("\nTelemetry validation PASSED.")
    else:
        print("\nTelemetry validation FAILED.")


if __name__ == "__main__":
    main()