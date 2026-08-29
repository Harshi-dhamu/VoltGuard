import pytest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.event_handler import EventBusIntegrationHandler
from scripts.mock_generator import build_modbus_tcp_packet

def test_event_handler_normal_packet_emission():
    emitted_events = []
    def mock_event_bus(event):
        emitted_events.append(event)

    handler = EventBusIntegrationHandler(event_bus_callback=mock_event_bus)
    normal_bytes = build_modbus_tcp_packet(801, 1, 6, 1001, 1200)

    event = handler.process_and_emit(normal_bytes)

    assert len(emitted_events) == 1
    assert event["source_module"] == "packet_interceptor"
    assert event["event_type"] == "NETWORK_TRAFFIC"
    assert event["severity"] == "INFO"

def test_event_handler_malicious_packet_emission():
    emitted_events = []
    def mock_event_bus(event):
        emitted_events.append(event)

    handler = EventBusIntegrationHandler(event_bus_callback=mock_event_bus)
    malicious_bytes = build_modbus_tcp_packet(802, 1, 6, 1001, 50000)

    event = handler.process_and_emit(malicious_bytes)

    assert len(emitted_events) == 1
    assert event["source_module"] == "packet_interceptor"
    assert event["event_type"] == "NETWORK_ANOMALY"
    assert event["severity"] == "CRITICAL"