import pytest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.event_bus_adapter import EventBusAdapter

def test_event_bus_adapter_formatting():
    adapter = EventBusAdapter()
    
    analyzed_data = {
        "transaction_id": 302,
        "function_code": 6,
        "register_address": 1001,
        "device_id": "PUMP_01",
        "command": "SET_SPEED",
        "value": 50000,
        "unit": "RPM",
        "is_suspicious": True,
        "suspicious_reason": "EXCEEDS_MAX_THRESHOLD"
    }

    event = adapter.publish_event(analyzed_data)

    assert event["source_module"] == "packet_interceptor"
    assert event["event_type"] == "NETWORK_ANOMALY"
    assert event["severity"] == "CRITICAL"
    assert event["asset_id"] == "PUMP_01"
    assert event["detection_details"]["value"] == 50000
    assert len(adapter.published_events) == 1