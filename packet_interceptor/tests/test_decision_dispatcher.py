import pytest
import sys
import os

# Point path directly to packet_interceptor root
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.packet_holder import PacketHoldBuffer
from src.decision_dispatcher import DecisionEngineDispatcher

def test_decision_dispatcher_allow():
    holder = PacketHoldBuffer()
    dispatcher = DecisionEngineDispatcher(hold_buffer=holder)

    pkt = {"transaction_id": 1, "value": 1000}
    token = holder.hold_packet(pkt, b"raw_bytes")

    resolved = dispatcher.process_held_token(token)
    assert resolved["status"] == "ALLOW"
    assert holder.get_held_count() == 0

def test_decision_dispatcher_drop():
    holder = PacketHoldBuffer()
    dispatcher = DecisionEngineDispatcher(hold_buffer=holder)

    pkt = {"transaction_id": 2, "value": 50000} # Exceeds threshold
    token = holder.hold_packet(pkt, b"raw_bytes")

    resolved = dispatcher.process_held_token(token)
    assert resolved["status"] == "DROP"
    assert holder.get_held_count() == 0