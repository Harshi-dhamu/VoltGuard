import pytest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.event_bus_adapter import EventBusAdapter

def test_event_bus_adapter_formatting():
    adapter = EventBusAdapter()
    
    sample_command = {
        "transaction_id": 88,
        "function_code": 6,
        "register_address": 1001,
        "device_id": "PUMP_01",
        "command": "SET_SPEED",
        "value": 1200,
        "unit": "RPM",
        "is_suspicious": False
    }

    event = adapter.format_integration_event(sample_command)

    assert "event_id" in event
    assert event["source_module"] == "packet_interceptor"
    assert event["event_type"] in ["NETWORK_TRAFFIC", "PACKET_PROCESSED"]
    assert event["severity"] == "LOW"
    assert event["asset"] == "PUMP_01"