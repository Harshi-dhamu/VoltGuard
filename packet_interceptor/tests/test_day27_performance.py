import pytest
import time
from src.inline_pipeline import InlineInterceptorPipeline
from src.telemetry_probe import PerformanceMonitor
from scripts.mock_generator import build_modbus_tcp_packet

def test_day27_telemetry_probe_calculations():
    """Validates accurate mean and percentile calculations in PerformanceMonitor."""
    probe = PerformanceMonitor()

    # Record mock durations (in seconds)
    probe.record_latency(0.000, 0.001)  # 1.0 ms
    probe.record_latency(0.000, 0.002)  # 2.0 ms
    probe.record_latency(0.000, 0.003)  # 3.0 ms

    stats = probe.get_statistics()
    assert stats["count"] == 3.0
    assert stats["avg_ms"] == 2.0
    assert stats["max_ms"] == 3.0

def test_day27_sub_millisecond_throughput_sla():
    """Validates that end-to-end processing across 1,000 packets maintains sub-millisecond average latency."""
    pipeline = InlineInterceptorPipeline()
    probe = PerformanceMonitor()

    # Pre-generate 1,000 Modbus TCP packets (50% normal, 50% high value)
    packets = []
    for tx_id in range(1, 1001):
        val = 500 if tx_id % 2 == 0 else 50000
        packets.append(build_modbus_tcp_packet(tx_id, 1, 6, 1001, val))

    # Benchmark end-to-end inline execution
    for raw_bytes in packets:
        t_start = time.perf_counter()
        pipeline.process_raw_stream_inline(raw_bytes)
        t_end = time.perf_counter()
        probe.record_latency(t_start, t_end)

    stats = probe.get_statistics()

    # Performance SLA Assertions
    assert stats["count"] == 1000.0
    # Assert average latency per packet is below 1.0 millisecond (1,000 microseconds)
    assert stats["avg_ms"] < 1.0, f"SLA Violation: Average latency {stats['avg_ms']}ms exceeds 1.0ms limit"