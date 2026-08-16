import pytest
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from packet_interceptor.src.parser import ModbusParser, ModbusParserError
from packet_interceptor.src.validator import PacketValidator
from packet_interceptor.scripts.mock_generator import build_modbus_tcp_packet

# 1. Valid Packet Test
def test_valid_packet_parsing():
    raw = build_modbus_tcp_packet(101, 1, 6, 1001, 1200)
    pkt = ModbusParser.parse_packet(raw)
    assert pkt.transaction_id == 101
    assert pkt.function_code == 6
    assert pkt.register_address == 1001
    assert pkt.value == 1200

# 2. Invalid Packet Test (Truncated MBAP)
def test_malformed_short_packet():
    with pytest.raises(ModbusParserError):
        ModbusParser.parse_packet(b"\x00\x01\x00")

# 3. Invalid Function Code Test
def test_invalid_function_code():
    raw = build_modbus_tcp_packet(102, 1, 0x1F, 1001, 100)
    pkt = ModbusParser.parse_packet(raw)
    is_valid, msg = PacketValidator.validate(pkt)
    assert is_valid is False
    assert "Unsupported function code" in msg

# 4. Invalid Register Address Test
def test_invalid_register_address():
    raw = build_modbus_tcp_packet(103, 1, 6, 9999, 100)
    pkt = ModbusParser.parse_packet(raw)
    is_valid, msg = PacketValidator.validate(pkt)
    assert is_valid is False
    assert "out of operational block range" in msg

# 5. Invalid Unit ID Test
def test_invalid_unit_id():
    raw = build_modbus_tcp_packet(104, 0, 6, 1001, 100)
    pkt = ModbusParser.parse_packet(raw)
    is_valid, msg = PacketValidator.validate(pkt)
    assert is_valid is False
    assert "Unit ID" in msg