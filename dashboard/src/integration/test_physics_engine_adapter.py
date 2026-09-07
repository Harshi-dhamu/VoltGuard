from integration.application_context import ApplicationContext
from integration.physics_engine_adapter import PhysicsEngineAdapter


def main() -> None:
    print("=" * 60)
    print("PHYSICS ENGINE INTEGRATION TEST")
    print("=" * 60)

    context = ApplicationContext()

    adapter = PhysicsEngineAdapter(
        context.integration_manager
    )

    physics_event = {
        "event_id": "TEST-PHY-0001",
        "source_module": "physics_engine",
        "event_type": "PROCESS_ANOMALY",
        "timestamp": "2026-08-29T15:39:09.554395+00:00",
        "severity": "CRITICAL",
        "asset": "MAIN-PLC",
        "message": "Critical abnormal process behaviour detected",
        "payload": {
            "anomaly_score": 0.94,
            "category": "COMMAND ANOMALY",
            "details": {
                "reason": (
                    "Critical process deviation detected "
                    "by the Physics Engine."
                )
            },
            "flow": {
                "pump_speed_rpm": 4000,
                "actual_flow_lpm": 5.0,
            },
            "tank": {
                "final_level_liters": 5800.0,
                "final_fill_percentage": 58.0,
            },
            "safety": {
                "overall_status": "CRITICAL",
            },
            "telemetry": {
                "actual_flow_lpm": 5.0,
            },
            "health_summary": {
                "system_status": "CRITICAL",
                "total_assets": 4,
                "normal_assets": 2,
                "warning_assets": 1,
                "critical_assets": 1,
            },
        },
    }

    published = adapter.publish_event(
        physics_event
    )

    status = context.integration_manager.get_status()

    print(f"Published: {published}")
    print(f"Total events: {status['total_events']}")
    print(f"Last event: {status['last_event']}")

    assert published is True
    assert status["total_events"] == 1
    assert (
        status["last_event"]["source_module"]
        == "physics_engine"
    )
    assert (
        status["last_event"]["event_type"]
        == "PROCESS_ANOMALY"
    )
    assert (
        status["last_event"]["severity"]
        == "CRITICAL"
    )
    assert (
        status["last_event"]["asset"]
        == "MAIN-PLC"
    )

    print("-" * 60)
    print("PHYSICS ENGINE INTEGRATION TEST PASSED")
    print("=" * 60)


if __name__ == "__main__":
    main()