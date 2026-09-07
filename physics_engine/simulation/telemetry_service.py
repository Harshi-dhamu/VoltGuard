class TelemetryService:
    """
    Converts Physics Engine simulation output
    into structured asset telemetry data.

    This service is independent from the dashboard/UI.
    """

    def build_asset_telemetry(self, flow_data, tank_data, safety_data):
        safety_checks = safety_data.get("checks", {})

        pump_check = safety_checks.get("pump", {})
        pipe_check = safety_checks.get("pipe_pressure", {})
        tank_check = safety_checks.get("tank", {})

        return {
            "system_status": safety_data.get("overall_status", "UNKNOWN"),

            "assets": {
                "PUMP_01": {
                    "asset_type": "PUMP",
                    "health_status": pump_check.get("status", "UNKNOWN"),
                    "speed_rpm": flow_data.get("pump_speed_rpm"),
                    "flow_lpm": flow_data.get("pump_flow_lpm"),
                },

                "VALVE_01": {
                    "asset_type": "VALVE",
                    "health_status": "NORMAL",
                    "position_percent": flow_data.get(
                        "valve_position_percent"
                    ),
                },

                "PIPE_01": {
                    "asset_type": "PIPE",
                    "health_status": pipe_check.get("status", "UNKNOWN"),
                },

                "TANK_01": {
                    "asset_type": "TANK",
                    "health_status": tank_check.get("status", "UNKNOWN"),
                    "level_liters": tank_data.get("final_level_liters"),
                    "fill_percentage": tank_data.get(
                        "final_fill_percentage"
                    ),
                },
            },

            "telemetry": {
                "actual_flow_lpm": flow_data.get("actual_flow_lpm"),
                "tank_level_liters": tank_data.get("final_level_liters"),
                "tank_fill_percentage": tank_data.get(
                    "final_fill_percentage"
                ),
            },
        }