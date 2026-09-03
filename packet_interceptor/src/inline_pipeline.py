from typing import Dict, Any
from src.stream_parser import StreamModbusParser
from src.packet_holder import PacketHoldBuffer
from src.decision_dispatcher import DecisionEngineDispatcher
from src.logger import setup_logger

logger = setup_logger()

class InlineInterceptorPipeline:
    """Full inline holding and enforcement pipeline."""

    def __init__(self):
        self.hold_buffer = PacketHoldBuffer()
        self.dispatcher = DecisionEngineDispatcher(self.hold_buffer)

    def process_raw_stream_inline(self, raw_bytes: bytes) -> Dict[str, Any]:
        """Parses, holds, evaluates, and enforces packet inline."""
        # 1. Parse Stream
        is_valid, parsed_pkt, err = StreamModbusParser.parse_stream(raw_bytes)
        if not is_valid:
            logger.warning(f"[INLINE REJECT] {err}")
            return {"status": "REJECTED", "reason": err}

        # 2. HOLD Packet
        token = self.hold_buffer.hold_packet(parsed_pkt, raw_bytes)
        logger.info(f"[INLINE HOLD] Token {token[:8]}... created for TxID {parsed_pkt['transaction_id']}")

        # 3. Evaluate & Enforce (ALLOW / DROP)
        resolved = self.dispatcher.process_held_token(token)
        return resolved