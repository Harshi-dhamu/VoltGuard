import struct
from typing import Dict, Any, Tuple, Optional

class StreamModbusParser:
    """High-throughput Python Modbus TCP binary stream parser."""

    # MBAP Header Format: TxID (2B), ProtoID (2B), Length (2B), UnitID (1B) -> Big-Endian (>HHHB)
    MBAP_FORMAT = ">HHHB"
    MBAP_SIZE = struct.calcsize(MBAP_FORMAT)

    @classmethod
    def parse_stream(cls, raw_bytes: bytes) -> Tuple[bool, Dict[str, Any], str]:
        """
        Extracts Modbus TCP fields using zero-copy memoryview and struct unpacking.
        Returns: (is_valid, parsed_data_dict, error_message)
        """
        if len(raw_bytes) < cls.MBAP_SIZE + 5: # MBAP (7B) + FC (1B) + Reg (2B) + Val (2B) = 12B min
            return False, {}, "Malformed packet: Buffer smaller than minimum Modbus TCP frame (12 bytes)."

        try:
            view = memoryview(raw_bytes)
            
            # Unpack MBAP Header
            tx_id, proto_id, length, unit_id = struct.unpack_from(cls.MBAP_FORMAT, view, 0)

            if proto_id != 0:
                return False, {}, f"Invalid Protocol ID: {proto_id}. Expected 0 for Modbus TCP."

            # Unpack Payload: Function Code (1B), Register Address (2B), Value (2B)
            fc, reg_addr, reg_val = struct.unpack_from(">BHH", view, cls.MBAP_SIZE)

            parsed_payload = {
                "transaction_id": tx_id,
                "protocol_id": proto_id,
                "length": length,
                "unit_id": unit_id,
                "function_code": fc,
                "register_address": reg_addr,
                "value": reg_val
            }

            return True, parsed_payload, ""

        except struct.error as e:
            return False, {}, f"Binary unpacking error: {str(e)}"