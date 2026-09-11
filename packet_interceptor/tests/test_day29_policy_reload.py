import pytest
from src.inline_pipeline import InlineInterceptorPipeline
from src.policy_manager import PolicyConfigManager
from scripts.mock_generator import build_modbus_tcp_packet

def test_day29_dynamic_policy_threshold_reload():
    """Validates that updating register thresholds dynamically changes inline DROP decisions without restarting."""
    pipeline = InlineInterceptorPipeline()
    policy_mgr = PolicyConfigManager()

    # Reset policy to default baseline (max_value = 10000)
    policy_mgr.reload_policies({"max_register_value": 10000, "blocked_unit_ids": []})

    # Test packet with value 8000 -> Should be ALLOWED
    pkt_bytes_8k = build_modbus_tcp_packet(1, 1, 6, 1001, 8000)
    res_before = pipeline.process_raw_stream_inline(pkt_bytes_8k)
    assert res_before["status"] == "ALLOW"

    # Dynamic Hot-Reload: Tighten security policy threshold to 5000
    policy_mgr.reload_policies({"max_register_value": 5000})

    # Same packet with value 8000 -> Should now be DROPPED
    res_after = pipeline.process_raw_stream_inline(pkt_bytes_8k)
    assert res_after["status"] == "DROP"

def test_day29_dynamic_unit_id_blacklist_reload():
    """Validates that dynamically blacklisting a Unit ID drops incoming traffic for that unit."""
    pipeline = InlineInterceptorPipeline()
    policy_mgr = PolicyConfigManager()

    policy_mgr.reload_policies({"max_register_value": 10000, "blocked_unit_ids": []})

    # Packet for Unit ID 5 -> Allowed
    pkt_unit5 = build_modbus_tcp_packet(2, 5, 6, 1001, 1000)
    assert pipeline.process_raw_stream_inline(pkt_unit5)["status"] == "ALLOW"

    # Dynamically block Unit ID 5
    policy_mgr.reload_policies({"blocked_unit_ids": [5]})

    # Packet for Unit ID 5 -> Dropped
    assert pipeline.process_raw_stream_inline(pkt_unit5)["status"] == "DROP"