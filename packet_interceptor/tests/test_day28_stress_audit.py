import pytest
import gc
from src.inline_pipeline import InlineInterceptorPipeline
from src.memory_audit import MemoryAuditTracker
from scripts.mock_generator import build_modbus_tcp_packet

def test_day28_memory_leak_and_stress_audit():
    """Executes 10,000 packets under load and asserts zero significant memory leakage (< 5.0 MB delta)."""
    pipeline = InlineInterceptorPipeline()
    tracker = MemoryAuditTracker()

    total_packets = 10000

    # Stream 10,000 mixed Modbus TCP packets through the pipeline
    for i in range(1, total_packets + 1):
        # Alternate between safe values and high-value attacks
        value = 800 if i % 2 == 0 else 45000
        raw_bytes = build_modbus_tcp_packet(i, 1, 6, 1001, value)
        
        result = pipeline.process_raw_stream_inline(raw_bytes)
        assert result["status"] in ["ALLOW", "DROP"]

    # Force explicit garbage collection cycle
    gc.collect()
    report = tracker.audit_report()

    # Memory Audit Assertions:
    # 1. Ensure PacketHoldBuffer contains zero residual held packets
    if hasattr(pipeline, "hold_buffer") and hasattr(pipeline.hold_buffer, "get_held_count"):
        assert pipeline.hold_buffer.get_held_count() == 0, "Memory leak error: Unreleased packets in hold buffer"

    # 2. Ensure total memory growth stays under 5.0 MB after processing 10,000 packets
    assert report["delta_mb"] < 5.0, f"Memory Leak Detected: Process grew by {report['delta_mb']} MB"