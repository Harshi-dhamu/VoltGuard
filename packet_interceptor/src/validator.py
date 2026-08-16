from .models.modbus_packet import ModbusPacket

class PacketValidator:
    SUPPORTED_FUNCTION_CODES = {0x03, 0x06, 0x10}

    @staticmethod
    def validate(packet: ModbusPacket) -> tuple[bool, str]:
        if packet.function_code not in PacketValidator.SUPPORTED_FUNCTION_CODES:
            return False, f"Unsupported function code: {hex(packet.function_code)}"
        
        if packet.unit_id == 0:
            return False, "Invalid Unit ID (0 is reserved for broadcast)."

        return True, "Valid Packet"