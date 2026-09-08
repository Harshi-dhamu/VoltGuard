import pytest
import time
from src.resilient_dispatcher import ResilientEventDispatcher, CircuitBreakerOpenException

def test_day26_successful_dispatch():
    """Validates standard event delivery to active subscribers."""
    received = []
    dispatcher = ResilientEventDispatcher(max_retries=2, failure_threshold=3)

    dispatcher.register_subscriber(lambda evt: received.append(evt))
    test_evt = {"event_id": "evt-001", "event_type": "NETWORK_TRAFFIC"}

    success = dispatcher.dispatch(test_evt)

    assert success is True
    assert len(received) == 1
    assert dispatcher.get_dlq_size() == 0

def test_day26_subscriber_fault_isolation_and_dlq_routing():
    """Ensures throwing subscriber exceptions trigger retries and route payload to DLQ without crashing."""
    dispatcher = ResilientEventDispatcher(max_retries=2, failure_threshold=5)

    def faulty_subscriber(evt):
        raise RuntimeError("Subscriber crashed unexpectedly")

    dispatcher.register_subscriber(faulty_subscriber)
    test_evt = {"event_id": "evt-002", "event_type": "NETWORK_ANOMALY"}

    success = dispatcher.dispatch(test_evt)

    assert success is False
    assert dispatcher.get_dlq_size() == 1
    
    dlq_items = dispatcher.purge_dlq()
    assert dlq_items[0]["event"]["event_id"] == "evt-002"
    assert "Exceeded max retries" in dlq_items[0]["reason"]

def test_day26_circuit_breaker_tripping():
    """Confirms circuit breaker opens after failure threshold is breached and fast-fails subsequent dispatches."""
    dispatcher = ResilientEventDispatcher(max_retries=1, failure_threshold=2, recovery_time_sec=5.0)

    def failing_subscriber(evt):
        raise ValueError("Connection timeout")

    dispatcher.register_subscriber(failing_subscriber)

    # Dispatch 1 -> Fails, failure_count = 1
    dispatcher.dispatch({"event_id": "evt-101"})
    assert dispatcher.state == "CLOSED"

    # Dispatch 2 -> Fails, failure_count = 2 -> Circuit OPENS
    dispatcher.dispatch({"event_id": "evt-102"})
    assert dispatcher.state == "OPEN"

    # Dispatch 3 -> Fast-fails immediately due to OPEN circuit breaker
    success = dispatcher.dispatch({"event_id": "evt-103"})

    assert success is False
    assert dispatcher.get_dlq_size() == 3
    assert "Circuit breaker is OPEN" in dispatcher.purge_dlq()[-1]["reason"]