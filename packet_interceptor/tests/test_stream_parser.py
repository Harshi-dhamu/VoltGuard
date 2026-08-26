import pytest
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.stream_parser import StreamModbusParser
from scripts.mock_generator import build_modbus_tcp_packet

def test_stream_parser_valid_packet():
    raw_bin = build_modbus_tcp_packet(401, 1, 6, 1001, 1800)
    is_valid, data, err = StreamModbusParser.parse_stream(raw_bin)
    
    assert is_valid is True
    assert err == ""
    assert data["transaction_id"] == 401
    assert data["function_code"] == 6
    assert data["register_address"] == 1001
    assert data["value"] == 1800

def test_stream_parser_truncated_packet():
    short_bin = b"\x00\x01\x00\x00"
    is_valid, data, err = StreamModbusParser.parse_stream(short_bin)
    
    assert is_valid is False
    assert "Buffer smaller than minimum" in err