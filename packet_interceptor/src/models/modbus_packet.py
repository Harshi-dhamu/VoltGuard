from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class ModbusPacket:
    """Represents a Modbus/TCP Application Protocol (MBAP) Header + PDU structure."""

    transaction_id: int = 0  # Identifies request/response transaction
    protocol_id: int = 0  # 0 = Modbus Protocol
    length: int = 0  # Number of following bytes
    unit_id: int = 0  # Target remote server / slave address
    function_code: int = 0  # Modbus function code (e.g., 0x03, 0x06, 0x10)
    register_address: int = 0  # Target register address
    register_value: int = 0  # Value to read/write
    timestamp: str = field(
        default_factory=lambda: datetime.now().isoformat()
    )

    def print_summary(self) -> None:
        """Prints a formatted summary of the packet details."""
        print(
            f"[ModbusPacket] TransID: {self.transaction_id} | "
            f"ProtoID: {self.protocol_id} | "
            f"Length: {self.length} | "
            f"UnitID: {self.unit_id} | "
            f"FuncCode: 0x{self.function_code:02X} | "
            f"Register: {self.register_address} | "
            f"Value: {self.register_value} | "
            f"Timestamp: {self.timestamp}"
        )