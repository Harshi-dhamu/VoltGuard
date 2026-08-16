from typing import Tuple
from .models.modbus_packet import ModbusPacket

class PacketValidator:
    SUPPORTED_FUNCTION_CODES = {0x03, 0x06, 0x10}  # Read Holding, Write Single, Write Multiple
    VALID_REGISTER_RANGES = range(1000, 2000)      # Valid industrial control register block

    @staticmethod
    def validate(packet: ModbusPacket) -> Tuple[bool, str]:
        # 1. Validate Protocol ID
        if packet.protocol_id != 0:
            return False, f"Invalid Modbus TCP Protocol ID: {packet.protocol_id} (Expected 0)"

        # 2. Validate Length field
        if packet.length < 2 or packet.length > 255:
            return False, f"Invalid length field: {packet.length} bytes"

        # 3. Validate Unit ID
        if packet.unit_id == 0 or packet.unit_id > 247:
            return False, f"Invalid or reserved Unit ID: {packet.unit_id}"

        # 4. Validate Function Code
        if packet.function_code not in PacketValidator.SUPPORTED_FUNCTION_CODES:
            return False, f"Unsupported function code: {hex(packet.function_code)}"

        # 5. Validate Register Address bounds
        if packet.register_address not in PacketValidator.VALID_REGISTER_RANGES:
            return False, f"Register address {packet.register_address} out of operational block range (1000-1999)"

        # 6. Validate value range (16-bit register limit)
        if packet.value < 0 or packet.value > 65535:
            return False, f"Value {packet.value} exceeds 16-bit unsigned integer bounds (0-65535)"

        return True, "Valid Packet"