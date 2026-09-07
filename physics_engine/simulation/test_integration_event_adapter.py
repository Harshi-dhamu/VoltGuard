import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(PROJECT_ROOT))
from physics_engine.simulation.integration_event_adapter import (
    IntegrationEventAdapter,
)


def main():
    adapter = IntegrationEventAdapter()

    sample_events = [
        adapter.build_process_anomaly_event(
            severity="NORMAL",
            asset="PUMP_01",
            message="Process operating within expected parameters",
            anomaly_score=0.12,
            category="NORMAL PROCESS CONDITION",
            details={
                "reason": "Flow and safety values are within expected range."
            },
            flow_data={
                "pump_speed_rpm": 2500,
                "actual_flow_lpm": 25.0,
            },
            tank_data={
                "final_level_liters": 5250.0,
                "final_fill_percentage": 52.5,
            },
            safety_data={
                "overall_status": "NORMAL",
            },
            telemetry_data={
                "actual_flow_lpm": 25.0,
            },
            health_summary={
                "system_status": "NORMAL",
                "total_assets": 4,
                "normal_assets": 4,
                "warning_assets": 0,
                "critical_assets": 0,
            },
        ),
        adapter.build_process_anomaly_event(
            severity="HIGH",
            asset="PUMP_01",
            message="Abnormal pump process behaviour detected",
            anomaly_score=0.82,
            category="FLOW ANOMALY",
            details={
                "reason": "Actual flow is significantly different from expected flow."
            },
            flow_data={
                "pump_speed_rpm": 3000,
                "actual_flow_lpm": 12.0,
            },
            tank_data={
                "final_level_liters": 5120.0,
                "final_fill_percentage": 51.2,
            },
            safety_data={
                "overall_status": "WARNING",
            },
            telemetry_data={
                "actual_flow_lpm": 12.0,
            },
            health_summary={
                "system_status": "WARNING",
                "total_assets": 4,
                "normal_assets": 3,
                "warning_assets": 1,
                "critical_assets": 0,
            },
        ),
        adapter.build_process_anomaly_event(
            severity="CRITICAL",
            asset="MAIN-PLC",
            message="Critical abnormal process behaviour detected",
            anomaly_score=0.94,
            category="COMMAND ANOMALY",
            details={
                "reason": "Critical process deviation detected by the Physics Engine."
            },
            flow_data={
                "pump_speed_rpm": 4000,
                "actual_flow_lpm": 5.0,
            },
            tank_data={
                "final_level_liters": 5800.0,
                "final_fill_percentage": 58.0,
            },
            safety_data={
                "overall_status": "CRITICAL",
            },
            telemetry_data={
                "actual_flow_lpm": 5.0,
            },
            health_summary={
                "system_status": "CRITICAL",
                "total_assets": 4,
                "normal_assets": 2,
                "warning_assets": 1,
                "critical_assets": 1,
            },
        ),
    ]

    print("=== VoltGuard Integration Event Adapter Test ===")
    print()

    required_fields = {
        "event_id",
        "source_module",
        "event_type",
        "timestamp",
        "severity",
        "asset",
        "message",
        "payload",
    }

    for index, event in enumerate(sample_events, start=1):
        assert set(event.keys()) == required_fields
        assert event["source_module"] == "physics_engine"
        assert event["event_type"] == "PROCESS_ANOMALY"
        assert event["severity"] in {
            "NORMAL",
            "HIGH",
            "CRITICAL",
        }
        assert event["asset"]
        assert event["message"]
        assert isinstance(event["payload"], dict)
        assert "anomaly_score" in event["payload"]
        assert "category" in event["payload"]

        print(f"--- Sample Event {index} ---")
        print(event)
        print()

    print("All IntegrationEvent adapter checks passed.")


if __name__ == "__main__":
    main()