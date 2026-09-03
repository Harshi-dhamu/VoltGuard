import pytest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.packet_holder import PacketHoldBuffer

def test_packet_hold_and_release():
    holder = PacketHoldBuffer()
    sample_pkt = {"transaction_id": 101, "register_address": 1001, "value": 1200}
    raw_bin = b"\x00\x65\x00\x00\x00\x06\x01\x06\x03\xE9\x04\xB0"

    # Step 1: Hold packet
    token = holder.hold_packet(sample_pkt, raw_bin)
    assert token is not None
    assert holder.get_held_count() == 1

    # Step 2: Release with ALLOW decision
    released = holder.release_packet(token, "ALLOW")
    assert released["status"] == "ALLOW"
    assert released["parsed_pkt"]["transaction_id"] == 101
    assert holder.get_held_count() == 0