import struct
from .models.modbus_packet import ModbusPacket

class ModbusParserError(Exception):
    pass

class ModbusParser:
    MBAP_HEADER_SIZE = 7

    @staticmethod
    def parse_packet(raw_bytes: bytes) -> ModbusPacket:
        if not raw_bytes or len(raw_bytes) < ModbusParser.MBAP_HEADER_SIZE + 1:
            raise ModbusParserError("Incomplete or malformed MBAP header/payload.")

        transaction_id, protocol_id, length, unit_id = struct.unpack(">HHHB", raw_bytes[:7])

        if protocol_id != 0:
            raise ModbusParserError(f"Invalid Modbus Protocol ID: {protocol_id}")

        pdu = raw_bytes[7:]
        if len(pdu) < 1:
            raise ModbusParserError("Empty PDU received.")

        function_code = pdu[0]
        register_address = 0
        value = 0

        if len(pdu) >= 5:
            register_address, value = struct.unpack(">HH", pdu[1:5])
        elif len(pdu) >= 3:
            register_address = struct.unpack(">H", pdu[1:3])[0]

        return ModbusPacket(
            transaction_id=transaction_id,
            protocol_id=protocol_id,
            length=length,
            unit_id=unit_id,
            function_code=function_code,
            register_address=register_address,
            value=value,
            raw_payload=raw_bytes
        )