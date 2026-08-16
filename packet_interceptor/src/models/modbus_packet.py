from dataclasses import dataclass, asdict
import json

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

    def to_json(self) -> str:
        return json.dumps(asdict(self), indent=2)