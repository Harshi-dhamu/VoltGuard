from integration.application_context import ApplicationContext

from integration.packet_interceptor_adapter import (
    PacketInterceptorAdapter,
)

from integration.physics_engine_adapter import (
    PhysicsEngineAdapter,
)

from integration.decision_engine_adapter import (
    DecisionEngineAdapter,
)


def run_test() -> None:
    print("=" * 70)
    print("VOLTGUARD UNIFIED EVENT PIPELINE TEST")
    print("=" * 70)

    # ---------------------------------------------------------
    # ONE shared ApplicationContext
    # ---------------------------------------------------------

    context = ApplicationContext()

    # ---------------------------------------------------------
    # Create all three adapters using the SAME
    # IntegrationManager.
    # ---------------------------------------------------------

    packet_adapter = PacketInterceptorAdapter(
        context.integration_manager
    )

    physics_adapter = PhysicsEngineAdapter(
        context.integration_manager
    )

    decision_adapter = DecisionEngineAdapter(
        context.integration_manager
    )

    # ---------------------------------------------------------
    # Central EventBus subscriber
    # ---------------------------------------------------------

    received_events = []

    def event_listener(event):
        received_events.append(event)

        print()
        print(
            f"[EventBus] "
            f"{event.source_module} → "
            f"{event.event_type} → "
            f"{event.severity} → "
            f"{event.asset}"
        )

    context.event_bus.subscribe(
        event_listener
    )

    # =========================================================
    # EVENT 1 — PACKET INTERCEPTOR
    # =========================================================

    packet_event = {
        "event_id": "PKT-TEST-0001",
        "source_module": "packet_interceptor",
        "event_type": "NETWORK_ANOMALY",
        "timestamp": "2026-09-01 20:00:00",
        "severity": "CRITICAL",
        "asset": "PUMP_01",
        "message": (
            "Parameter anomaly detected on "
            "PUMP_01: EXCEEDS_MAX_THRESHOLD"
        ),
        "payload": {
            "transaction_id": 302,
            "function_code": 6,
            "register_address": 1001,
            "command": "SET_SPEED",
            "value": 50000,
            "unit": "RPM",
            "is_suspicious": True,
            "suspicious_reason": (
                "EXCEEDS_MAX_THRESHOLD"
            ),
        },
    }

    packet_result = packet_adapter.publish_event(
        packet_event
    )

    print()
    print("--- PACKET INTERCEPTOR ---")
    print("Published:", packet_result)

    # =========================================================
    # EVENT 2 — PHYSICS ENGINE
    # =========================================================

    physics_event = {
        "event_id": "PHY-TEST-0001",
        "source_module": "physics_engine",
        "event_type": "PROCESS_ANOMALY",
        "timestamp": "2026-09-01 20:00:01",
        "severity": "CRITICAL",
        "asset": "PUMP_01",
        "message": (
            "Critical abnormal process "
            "behaviour detected"
        ),
        "payload": {
            "anomaly_score": 0.94,
            "category": "SAFETY ANOMALY",
            "details": {
                "critical_items": [
                    "PUMP_01"
                ],
                "reason": (
                    "Physics safety check failed."
                ),
            },
            "flow": {
                "pump_speed_rpm": 50000,
                "actual_flow_lpm": 5.0,
            },
            "tank": {
                "final_level_liters": 5800.0,
            },
            "safety": {
                "overall_status": "CRITICAL",
            },
            "telemetry": {},
            "health_summary": {
                "system_status": "CRITICAL",
            },
        },
    }

    physics_result = physics_adapter.publish_event(
        physics_event
    )

    print()
    print("--- PHYSICS ENGINE ---")
    print("Published:", physics_result)

    # =========================================================
    # EVENT 3 — DECISION ENGINE
    # =========================================================

    decision_event = """
    {
        "event_id": "DEC-TEST-0001",
        "source_module": "decision_engine",
        "event_type": "SECURITY_DECISION",
        "timestamp": "2026-09-01 20:00:02",
        "severity": "HIGH",
        "asset": "PUMP_01",
        "message": "Security decision generated for PUMP_01: BLOCK",
        "payload": {
            "decision": "BLOCK",
            "reason": "PRESSURE_LIMIT_EXCEEDED",
            "source_event_id": "PHY-TEST-0001"
        }
    }
    """

    decision_result = decision_adapter.publish_json(
        decision_event
    )

    print()
    print("--- DECISION ENGINE ---")
    print("Published:", decision_result)

    # =========================================================
    # CENTRAL VALIDATION
    # =========================================================

    status = context.integration_manager.get_status()

    print()
    print("=" * 70)
    print("CENTRAL INTEGRATION STATUS")
    print("=" * 70)

    print(
        "Total events:",
        status["total_events"],
    )

    print(
        "Subscribers:",
        status["subscriber_count"],
    )

    print(
        "EventBus received:",
        len(received_events),
    )

    print(
        "Last event:",
        status["last_event"],
    )

    # ---------------------------------------------------------
    # Assertions
    # ---------------------------------------------------------

    assert packet_result is True
    assert physics_result is True
    assert decision_result is True

    assert status["total_events"] == 3

    assert len(received_events) == 3

    # ---------------------------------------------------------
    # Verify event sources
    # ---------------------------------------------------------

    sources = [
        event.source_module
        for event in received_events
    ]

    assert "packet_interceptor" in sources
    assert "physics_engine" in sources
    assert "decision_engine" in sources

    # ---------------------------------------------------------
    # Verify event types
    # ---------------------------------------------------------

    event_types = [
        event.event_type
        for event in received_events
    ]

    assert "NETWORK_ANOMALY" in event_types
    assert "PROCESS_ANOMALY" in event_types
    assert "SECURITY_DECISION" in event_types

    # ---------------------------------------------------------
    # Verify final Decision Engine event
    # ---------------------------------------------------------

    assert (
        status["last_event"]["source_module"]
        == "decision_engine"
    )

    assert (
        status["last_event"]["event_type"]
        == "SECURITY_DECISION"
    )

    assert (
        status["last_event"]["payload"]["decision"]
        == "BLOCK"
    )

    print()
    print("=" * 70)
    print("UNIFIED EVENT PIPELINE TEST PASSED")
    print("=" * 70)


if __name__ == "__main__":
    run_test()