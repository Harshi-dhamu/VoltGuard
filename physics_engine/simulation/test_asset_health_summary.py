import sys
from pathlib import Path

# Add project root to Python path
PROJECT_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(PROJECT_ROOT))

from physics_engine.simulation.telemetry_service import TelemetryService


def build_health_summary(telemetry_data):
    """
    Create a dashboard-friendly health summary
    from structured asset telemetry.
    """

    assets = telemetry_data.get("assets", {})

    summary = {
        "system_status": telemetry_data.get("system_status", "UNKNOWN"),
        "total_assets": len(assets),
        "normal_assets": 0,
        "warning_assets": 0,
        "critical_assets": 0,
        "assets": {},
    }

    for asset_id, asset_data in assets.items():
        status = asset_data.get("health_status", "UNKNOWN")

        if status == "NORMAL":
            summary["normal_assets"] += 1
        elif status == "WARNING":
            summary["warning_assets"] += 1
        elif status == "CRITICAL":
            summary["critical_assets"] += 1

        summary["assets"][asset_id] = {
            "asset_type": asset_data.get("asset_type", "UNKNOWN"),
            "health_status": status,
        }

    return summary


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

    health_summary = build_health_summary(telemetry)

    print("=== VoltGuard Asset Health Summary Test ===")
    print()
    print("Health Summary:")
    print(health_summary)

    print()
    print(
        f"Total Assets: {health_summary['total_assets']}"
    )
    print(
        f"Normal Assets: {health_summary['normal_assets']}"
    )
    print(
        f"Warning Assets: {health_summary['warning_assets']}"
    )
    print(
        f"Critical Assets: {health_summary['critical_assets']}"
    )


if __name__ == "__main__":
    main()