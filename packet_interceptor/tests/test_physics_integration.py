import pytest
import sys
import os

# Ensure packet_interceptor root directory is in sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.parser import ModbusParser
from src.normalizer import CommandNormalizer
from src.suspicious_detector import SuspiciousTrafficDetector
from src.physics_interface import PhysicsEngineInterface
from scripts.mock_generator import build_modbus_tcp_packet

def test_physics_interface_callback_integration():
    received_payloads = []

    # Mock callback to simulate Dhruti's Physics Engine ingestion
    def mock_physics_engine_receiver(payload):
        received_payloads.append(payload)
        return True

    interface = PhysicsEngineInterface(dispatch_callback=mock_physics_engine_receiver)

    # Process sample packet
    raw = build_modbus_tcp_packet(201, 1, 6, 1001, 1500)
    pkt = ModbusParser.parse_packet(raw)
    norm = CommandNormalizer.normalize(pkt)
    analyzed = SuspiciousTrafficDetector.analyze(norm)

    # Dispatch to interface
    success = interface.send_to_physics_engine(analyzed)

    assert success is True
    assert len(received_payloads) == 1
    assert received_payloads[0]["device_id"] == "PUMP_01"
    assert received_payloads[0]["value"] == 1500.0
    assert received_payloads[0]["unit"] == "RPM"