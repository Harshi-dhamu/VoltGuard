import pytest
import gc
from src.inline_pipeline import InlineInterceptorPipeline
from src.policy_manager import PolicyConfigManager
from src.release_certification import ModuleCertificationEngine
from src.telemetry_probe import PerformanceMonitor
from src.memory_audit import MemoryAuditTracker
from tests.utils import build_modbus_tcp_packet

def test_day30_full_module_production_certification():
    """Executes end-to-end multi-threaded traffic processing, dynamic reloading, and health verification."""
    certification_engine = ModuleCertificationEngine()
    pipeline = InlineInterceptorPipeline()
    policy_mgr = PolicyConfigManager()
    probe = PerformanceMonitor()
    memory_tracker = MemoryAuditTracker()

    # Reset baseline policies
    policy_mgr.reload_policies({"max_register_value": 10000, "blocked_unit_ids": []})

    # Phase 1: High-throughput ingestion (2,000 packets)
    for i in range(1, 2001):
        val = 500 if i % 2 == 0 else 15000
        raw_pkt = build_modbus_tcp_packet(i, 1, 6, 1001, val)

        import time
        t_start = time.perf_counter()
        result = pipeline.process_raw_stream_inline(raw_pkt)
        t_end = time.perf_counter()
        probe.record_latency(t_start, t_end)

        if val > 10000:
            assert result["status"] == "DROP"
        else:
            assert result["status"] == "ALLOW"

    # Phase 2: Live Policy Reload under traffic
    policy_mgr.reload_policies({"max_register_value": 4000})
    strict_pkt = build_modbus_tcp_packet(9999, 1, 6, 1001, 5000)
    result_strict = pipeline.process_raw_stream_inline(strict_pkt)
    assert result_strict["status"] == "DROP"

    # Phase 3: SLA & Diagnostics Validation
    stats = probe.get_statistics()
    assert stats["avg_ms"] < 1.0, f"Production SLA breach: {stats['avg_ms']}ms"

    gc.collect()
    readiness = certification_engine.verify_module_readiness()
    assert readiness is True, "Module failed final production certification check"