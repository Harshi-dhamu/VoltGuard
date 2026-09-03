import queue
import time
import uuid
from typing import Dict, Any, Optional

class PacketHoldBuffer:
    """Thread-safe inline packet holding buffer for VoltGuard pipeline."""

    def __init__(self, default_timeout_sec: float = 2.0):
        self.default_timeout_sec = default_timeout_sec
        self._buffer: Dict[str, Dict[str, Any]] = {}

    def hold_packet(self, parsed_pkt: Dict[str, Any], raw_bytes: bytes) -> str:
        """Enqueues packet and returns a unique hold token."""
        token = str(uuid.uuid4())
        self._buffer[token] = {
            "token": token,
            "parsed_pkt": parsed_pkt,
            "raw_bytes": raw_bytes,
            "timestamp": time.time(),
            "status": "HELD"
        }
        return token

    def release_packet(self, token: str, action: str) -> Optional[Dict[str, Any]]:
        """Processes decision (ALLOW / DROP) and removes packet from hold queue."""
        if token not in self._buffer:
            return None

        pkt_data = self._buffer.pop(token)
        pkt_data["status"] = action  # "ALLOW" or "DROP"
        return pkt_data

    def get_held_count(self) -> int:
        return len(self._buffer)