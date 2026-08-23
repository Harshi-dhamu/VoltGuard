import time
from typing import Dict, Any, Callable, Optional
from src.packet_holder import PacketHoldBuffer
from src.logger import setup_logger

logger = setup_logger()

class DecisionEngineDispatcher:
    """Dispatches held packets to Decision Engine and routes action."""

    def __init__(self, hold_buffer: PacketHoldBuffer, decision_callback: Optional[Callable] = None):
        self.hold_buffer = hold_buffer
        # Default mock callback simulating Akhina's Decision Engine
        self.decision_callback = decision_callback or self._default_mock_decision_engine

    def _default_mock_decision_engine(self, parsed_pkt: Dict[str, Any]) -> str:
        """Mock decision logic: DROPs if suspicious/high value, ALLOWs otherwise."""
        if parsed_pkt.get("value", 0) > 5000:
            return "DROP"
        return "ALLOW"

    def process_held_token(self, token: str) -> Optional[Dict[str, Any]]:
        """Evaluates token through decision callback and executes action."""
        if token not in self.hold_buffer._buffer:
            logger.warning(f"[DISPATCHER] Token {token} not found in buffer.")
            return None

        pkt_data = self.hold_buffer._buffer[token]
        parsed_pkt = pkt_data["parsed_pkt"]

        # Request decision
        decision = self.decision_callback(parsed_pkt)
        logger.info(f"[DECISION ENGINE] Token: {token[:8]}... | Action: {decision}")

        # Execute release or drop
        resolved_pkt = self.hold_buffer.release_packet(token, action=decision)
        return resolved_pkt