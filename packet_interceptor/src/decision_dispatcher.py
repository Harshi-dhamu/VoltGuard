from typing import Dict, Any
from src.policy_manager import PolicyConfigManager
from src.logger import setup_logger

logger = setup_logger()

class DecisionEngineDispatcher:
    """Dispatches decisions for held packets based on dynamic policy rules."""

    def __init__(self, hold_buffer=None):
        self.hold_buffer = hold_buffer
        self.policy_manager = PolicyConfigManager()

    def process_held_token(self, token: str) -> Dict[str, Any]:
        """Retrieves and removes held packet from buffer, evaluating dynamic policies."""
        pkt_entry = {}
        release_after_decision = False
        if self.hold_buffer:
            if hasattr(self.hold_buffer, "pop_packet"):
                pkt_entry = self.hold_buffer.pop_packet(token) or {}
            elif hasattr(self.hold_buffer, "release_packet"):
                if hasattr(self.hold_buffer, "get_packet"):
                    pkt_entry = self.hold_buffer.get_packet(token) or {}
                    release_after_decision = True
                else:
                    pkt_entry = self.hold_buffer.release_packet(token, "ALLOW") or {}
            elif hasattr(self.hold_buffer, "get_packet"):
                pkt_entry = self.hold_buffer.get_packet(token) or {}
                if hasattr(self.hold_buffer, "held_packets") and isinstance(self.hold_buffer.held_packets, dict):
                    self.hold_buffer.held_packets.pop(token, None)

        parsed_pkt = pkt_entry
        for key in ["packet", "payload", "parsed_packet", "parsed_pkt", "data"]:
            if isinstance(parsed_pkt, dict) and key in parsed_pkt and isinstance(parsed_pkt[key], dict):
                parsed_pkt = parsed_pkt[key]
                break

        if not isinstance(parsed_pkt, dict):
            parsed_pkt = {}

        value = parsed_pkt.get("value", 0)
        unit_id = parsed_pkt.get("unit_id", 1)
        is_suspicious = parsed_pkt.get("is_suspicious", False)

        # Dynamic Policy Enforcement
        exceeds_threshold = self.policy_manager.is_value_exceeded(value)
        unit_blocked = self.policy_manager.is_unit_blocked(unit_id)

        if is_suspicious or exceeds_threshold or unit_blocked:
            action = "DROP"
            status = "DROP"
            is_suspicious = True
        else:
            action = "ALLOW"
            status = "ALLOW"

        if release_after_decision:
            self.hold_buffer.release_packet(token, action)

        logger.info(f"[DECISION ENGINE] Token: {str(token)[:8]}... | Action: {action}")

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

DecisionDispatcher = DecisionEngineDispatcher
decision_dispatcher = DecisionEngineDispatcher