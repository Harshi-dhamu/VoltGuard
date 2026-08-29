class HealthSummaryService:
    """
    Creates a dashboard-friendly health summary
    from structured asset telemetry.
    """

    def build_health_summary(self, telemetry_data: dict) -> dict:
        assets = telemetry_data.get("assets", {})

        summary = {
            "system_status": telemetry_data.get(
                "system_status", "UNKNOWN"
            ),
            "total_assets": len(assets),
            "normal_assets": 0,
            "warning_assets": 0,
            "critical_assets": 0,
            "assets": {},
        }

        for asset_id, asset_data in assets.items():
            status = asset_data.get(
                "health_status", "UNKNOWN"
            )

            if status == "NORMAL":
                summary["normal_assets"] += 1
            elif status == "WARNING":
                summary["warning_assets"] += 1
            elif status == "CRITICAL":
                summary["critical_assets"] += 1

            summary["assets"][asset_id] = {
                "asset_type": asset_data.get(
                    "asset_type", "UNKNOWN"
                ),
                "health_status": status,
            }

        return summary