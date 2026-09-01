import pytest
import sys
import os
import time

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.resilient_dispatcher import ResilientEventBusDispatcher

def test_resilient_dispatcher_dlq_on_overflow():
    # Small buffer size to force overflow into DLQ
    dispatcher = ResilientEventBusDispatcher(async_buffer_size=2, dlq_capacity=10)
    
    command = {
        "transaction_id": 999,
        "function_code": 6,
        "register_address": 1001,
        "device_id": "PUMP_01",
        "command": "SET_SPEED",
        "value": 1500,
        "unit": "RPM",
        "is_suspicious": False
    }

    # Flood the dispatcher without starting async consumer worker loop
    for _ in range(5):
        dispatcher.dispatch_safe(command)

    # Queue should take 2 items, remaining 3 should route to DLQ
    assert len(dispatcher.dead_letter_queue) == 3
    assert dispatcher.dead_letter_queue[0]["dlq_reason"] == "AsyncBufferOverflow"

def test_resilient_dispatcher_sync_listener_fault_isolation():
    dispatcher = ResilientEventBusDispatcher()

    def failing_listener(event):
        raise RuntimeError("Simulated listener crash")

    dispatcher.register_sync_listener(failing_listener)

    command = {
        "transaction_id": 1000,
        "function_code": 6,
        "register_address": 1001,
        "device_id": "PUMP_01",
        "command": "SET_SPEED",
        "value": 1200,
        "unit": "RPM",
        "is_suspicious": False
    }

    event = dispatcher.dispatch_safe(command)

    assert len(dispatcher.dead_letter_queue) == 1
    assert "ListenerError" in dispatcher.dead_letter_queue[0]["dlq_reason"]