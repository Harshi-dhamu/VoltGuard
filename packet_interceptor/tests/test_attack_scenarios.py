import pytest
import sys
import os

# Add packet_interceptor root directory to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.parser import ModbusParser, ModbusParserError
from src.validator import PacketValidator
from src.normalizer import CommandNormalizer
from src.suspicious_detector import SuspiciousTrafficDetector
from scripts.mock_generator import build_modbus_tcp_packet

def test_overpressure_attack_detection():
    # Attack: Set Pressure to 1000 PSI on register 1003 (Max threshold is 150 PSI)
    raw = build_modbus_tcp_packet(301, 1, 6, 1003, 1000)
    pkt = ModbusParser.parse_packet(raw)
    is_valid, validation_msg = PacketValidator.validate(pkt)
    assert is_valid is True, f"Validation failed: {validation_msg}"

    norm = CommandNormalizer.normalize(pkt)
    analyzed = SuspiciousTrafficDetector.analyze(norm)
    assert analyzed.is_suspicious is True
    assert "EXCEEDS_MAX_THRESHOLD" in analyzed.suspicious_reason

def test_pump_overspeed_attack_detection():
    # Attack: Set Pump Speed to 50000 RPM on register 1001 (Max threshold is 5000 RPM)
    raw = build_modbus_tcp_packet(302, 1, 6, 1001, 50000)
    pkt = ModbusParser.parse_packet(raw)
    is_valid, validation_msg = PacketValidator.validate(pkt)
    assert is_valid is True, f"Validation failed: {validation_msg}"

    norm = CommandNormalizer.normalize(pkt)
    analyzed = SuspiciousTrafficDetector.analyze(norm)
    assert analyzed.is_suspicious is True
    assert "EXCEEDS_MAX_THRESHOLD" in analyzed.suspicious_reason