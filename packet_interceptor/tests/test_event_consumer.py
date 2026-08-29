import pytest
import sys
import os
import time

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.event_consumer import EventBusConsumer
from src.event_bus_adapter import EventBusAdapter

def test_async_event_consumer_processing():
    consumer = EventBusConsumer()
    adapter = EventBusAdapter()

    normal_data = {
        "transaction_id": 901,
        "function_code": 6,
        "register_address": 1001,
        "device_id": "PUMP_01",
        "command": "SET_SPEED",
        "value": 1200,
        "unit": "RPM",
        "is_suspicious": False
    }

    event = adapter.format_integration_event(normal_data)

    # Start consumer thread
    consumer.start()

    # Enqueue event
    success = consumer.enqueue_event(event)
    assert success is True

    # Allow worker thread time to process
    time.sleep(0.5)

    consumer.stop()

    assert len(consumer.consumed_events) == 1
    assert consumer.consumed_events[0]["event_id"] == event["event_id"]