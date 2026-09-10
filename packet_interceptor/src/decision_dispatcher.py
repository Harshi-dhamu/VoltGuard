from typing import Dict, Any
from src.logger import setup_logger

logger = setup_logger()

class DecisionEngineDispatcher:
    """Dispatches decisions for held packets based on pipeline analysis."""

    def __init__(self, hold_buffer=None):
        self.hold_buffer = hold_buffer

    def process_held_token(self, token: str) -> Dict[str, Any]:
        """Retrieves and removes held packet from buffer, evaluating security policies."""
        pkt_entry = {}
        release_after_decision = False
        if self.hold_buffer:
            # Pop/release from hold buffer so held count goes to 0
            if hasattr(self.hold_buffer, "pop_packet"):
                pkt_entry = self.hold_buffer.pop_packet(token) or {}
            elif hasattr(self.hold_buffer, "release_packet"):
                if hasattr(self.hold_buffer, "get_packet"):
                    pkt_entry = self.hold_buffer.get_packet(token) or {}
                    release_after_decision = True
            elif hasattr(self.hold_buffer, "get_packet"):
                pkt_entry = self.hold_buffer.get_packet(token) or {}
                if hasattr(self.hold_buffer, "held_packets") and isinstance(self.hold_buffer.held_packets, dict):
                    self.hold_buffer.held_packets.pop(token, None)

        # Unwrap packet payload structure
        parsed_pkt = pkt_entry
        for key in ["packet", "payload", "parsed_packet", "parsed_pkt", "data"]:
            if isinstance(parsed_pkt, dict) and key in parsed_pkt and isinstance(parsed_pkt[key], dict):
                parsed_pkt = parsed_pkt[key]
                break

        if not isinstance(parsed_pkt, dict):
            parsed_pkt = {}

        value = parsed_pkt.get("value", 0)
        is_suspicious = parsed_pkt.get("is_suspicious", False)

        # Evaluate threshold (> 10000 -> DROP)
        if is_suspicious or value > 10000:
            action = "DROP"
            status = "DROP"
            is_suspicious = True
        else:
            action = "ALLOW"
            status = "ALLOW"

        if release_after_decision:
            self.hold_buffer.release_packet(token, action)

        logger.debug(f"[DECISION ENGINE] Token: {str(token)[:8]}... | Action: {action}")

        result = dict(parsed_pkt)
        result.update({
            "token": token,
            "status": status,
            "action": action,
            "inline_action": action,
            "is_suspicious": is_suspicious,
            "payload": parsed_pkt
        })
        return result

    def dispatch_decision(self, hold_token: str, packet_data: Dict[str, Any]) -> Dict[str, Any]:
        """Direct evaluation method."""
        is_suspicious = packet_data.get("is_suspicious", False)
        value = packet_data.get("value", 0)

        action = "DROP" if (is_suspicious or value > 10000) else "ALLOW"
        logger.info(f"[DECISION ENGINE] Token: {str(hold_token)[:8]}... | Action: {action}")
        return {
            "token": hold_token, 
            "status": action, 
            "action": action, 
            "inline_action": action, 
            "is_suspicious": action == "DROP"
        }

DecisionDispatcher = DecisionEngineDispatcher
decision_dispatcher = DecisionEngineDispatcher