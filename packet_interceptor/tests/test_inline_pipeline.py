import pytest
import sys
import os

# Point path directly to packet_interceptor root
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.inline_pipeline import InlineInterceptorPipeline
from scripts.mock_generator import build_modbus_tcp_packet

def test_inline_pipeline_normal_packet():
    pipeline = InlineInterceptorPipeline()
    normal_bytes = build_modbus_tcp_packet(701, 1, 6, 1001, 1200) # Safe value

    result = pipeline.process_raw_stream_inline(normal_bytes)
    assert result["status"] == "ALLOW"

def test_inline_pipeline_malicious_packet():
    pipeline = InlineInterceptorPipeline()
    malicious_bytes = build_modbus_tcp_packet(702, 1, 6, 1001, 50000) # Dangerous value

    result = pipeline.process_raw_stream_inline(malicious_bytes)
    assert result["status"] == "DROP"