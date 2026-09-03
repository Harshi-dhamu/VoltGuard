from integration.application_context import (
    ApplicationContext,
)

from integration.decision_engine_adapter import (
    DecisionEngineAdapter,
)


def run_test() -> None:
    print("=" * 60)
    print("DECISION ENGINE INTEGRATION TEST")
    print("=" * 60)

    # --------------------------------------------------
    # Create the existing central application context
    # --------------------------------------------------

    context = ApplicationContext()

    adapter = DecisionEngineAdapter(
        context.integration_manager
    )

    # --------------------------------------------------
    # Subscribe to the existing EventBus
    # --------------------------------------------------

    received_events = []

    def event_listener(event):
        received_events.append(event)

        print()
        print("EventBus received:")
        print(event.to_dict())

    context.event_bus.subscribe(
        event_listener
    )

    # --------------------------------------------------
    # Test 1: ALLOW
    # --------------------------------------------------

    allow_event = """
    {
        "event_id": "DEC-0001",
        "source_module": "decision_engine",
        "event_type": "SECURITY_DECISION",
        "timestamp": "2026-09-01 20:00:00",
        "severity": "LOW",
        "asset": "PUMP_01",
        "message": "Security decision generated for PUMP_01: ALLOW",
        "payload": {
            "decision": "ALLOW",
            "reason": "PHYSICS_STATUS_SAFE",
            "source_event_id": "PKT-0001"
        }
    }
    """

    published = adapter.publish_json(
        allow_event
    )

    print()
    print("--- ALLOW TEST ---")
    print("Published:", published)

    status = context.integration_manager.get_status()

    print("Total events:", status["total_events"])

    assert published is True

    assert status["total_events"] == 1

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
        == "ALLOW"
    )

    # --------------------------------------------------
    # Test 2: BLOCK
    # --------------------------------------------------

    block_event = """
    {
        "event_id": "DEC-0002",
        "source_module": "decision_engine",
        "event_type": "SECURITY_DECISION",
        "timestamp": "2026-09-01 20:01:00",
        "severity": "HIGH",
        "asset": "PUMP_01",
        "message": "Security decision generated for PUMP_01: BLOCK",
        "payload": {
            "decision": "BLOCK",
            "reason": "PRESSURE_LIMIT_EXCEEDED",
            "source_event_id": "PKT-0002"
        }
    }
    """

    published = adapter.publish_json(
        block_event
    )

    print()
    print("--- BLOCK TEST ---")
    print("Published:", published)

    status = context.integration_manager.get_status()

    print("Total events:", status["total_events"])

    assert published is True

    assert status["total_events"] == 2

    assert (
        status["last_event"]["payload"]["decision"]
        == "BLOCK"
    )

    assert (
        status["last_event"]["severity"]
        == "HIGH"
    )

    # --------------------------------------------------
    # Test 3: Invalid JSON
    # --------------------------------------------------

    try:
        adapter.publish_json(
            "{ invalid json }"
        )

    except ValueError:
        print()
        print("--- INVALID JSON TEST ---")
        print("Invalid JSON test: PASSED")

    else:
        raise AssertionError(
            "Invalid JSON should raise ValueError"
        )

    # --------------------------------------------------
    # Verify EventBus received both events
    # --------------------------------------------------

    assert len(received_events) == 2

    print()
    print(
        "EventBus received events:",
        len(received_events),
    )

    print()
    print("=" * 60)
    print(
        "ALL DECISION ENGINE INTEGRATION TESTS PASSED"
    )
    print("=" * 60)


if __name__ == "__main__":
    run_test()