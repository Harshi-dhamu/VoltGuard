from dataclasses import dataclass, asdict
import json
from typing import Optional, Dict, Any

@dataclass
class ModbusPacket:
    transaction_id: int
    protocol_id: int
    length: int
    unit_id: int
    function_code: int
    register_address: int
    value: int
    raw_payload: bytes

@dataclass
class NormalizedCommand:
    device_id: str
    command: str
    value: float
    unit: str
    transaction_id: int
    timestamp: float
    is_suspicious: bool = False
    suspicious_reason: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

    def to_json(self) -> str:
        return json.dumps(self.to_dict(), indent=2)