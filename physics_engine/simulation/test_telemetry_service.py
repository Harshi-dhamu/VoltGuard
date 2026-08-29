from telemetry_service import TelemetryService


flow_data = {
    "pump_speed_rpm": 2500,
    "valve_position_percent": 50,
    "pump_flow_lpm": 50.0,
    "actual_flow_lpm": 25.0,
}

tank_data = {
    "initial_level_liters": 5000,
    "flow_rate_lpm": 25.0,
    "time_minutes": 10,
    "final_level_liters": 5250.0,
    "final_fill_percentage": 52.5,
}

safety_data = {
    "overall_status": "NORMAL",
    "checks": {
        "pump": {
            "status": "NORMAL",
            "message": "Pump speed is within the safe limit.",
        },
        "pipe_pressure": {
            "status": "NORMAL",
            "message": "Pipe pressure is within the safe limit.",
        },
        "tank": {
            "status": "NORMAL",
            "message": "Tank level is within capacity.",
        },
    },
    "critical_items": [],
}


service = TelemetryService()

result = service.build_asset_telemetry(
    flow_data,
    tank_data,
    safety_data,
)


print("=== VoltGuard Asset Telemetry Test ===")
print()

print("System Status:")
print(result["system_status"])

print()

print("Assets:")
for asset_id, asset in result["assets"].items():
    print(asset_id, ":", asset)

print()

print("Telemetry:")
print(result["telemetry"])