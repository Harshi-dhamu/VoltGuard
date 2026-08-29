import pytest
import sys
import os
import time

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.event_dispatcher import CentralEventBusDispatcher

def test_dispatcher_sync_and_async_routing():
    dispatcher = CentralEventBusDispatcher()
    sync_received = []

    def mock_sync_listener(event):
        sync_received.append(event)

    dispatcher.register_sync_listener(mock_sync_listener)
    dispatcher.start_async_pipeline()

    normal_command = {
        "transaction_id": 905,
        "function_code": 6,
        "register_address": 1001,
        "device_id": "PUMP_01",
        "command": "SET_SPEED",
        "value": 1500,
        "unit": "RPM",
        "is_suspicious": False
    }

    event = dispatcher.dispatch(normal_command)

    # Allow background thread worker to digest queue item
    time.sleep(0.4)
    dispatcher.stop_async_pipeline()

    # Verify synchronous delivery
    assert len(sync_received) == 1
    assert sync_received[0]["event_id"] == event["event_id"]

    # Verify asynchronous queue consumption
    assert len(dispatcher.consumer.consumed_events) == 1
    assert dispatcher.consumer.consumed_events[0]["event_id"] == event["event_id"]