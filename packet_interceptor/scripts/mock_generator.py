import struct

def build_modbus_tcp_packet(transaction_id: int, unit_id: int, function_code: int, register: int, value: int) -> bytes:
    pdu = struct.pack(">BHH", function_code, register, value)
    length = len(pdu) + 1  # Unit ID (1B) + PDU size
    mbap = struct.pack(">HHHB", transaction_id, 0, length, unit_id)
    return mbap + pdu

def generate_expanded_traffic():
    return {
        # Valid Normal Commands
        "normal_pump": build_modbus_tcp_packet(1, 1, 6, 1001, 1000),         # 1000 RPM
        "normal_valve": build_modbus_tcp_packet(2, 1, 6, 1002, 50),           # 50%
        
        # Suspicious Commands (Day 9)
        "malicious_pump": build_modbus_tcp_packet(3, 1, 6, 1001, 50000),      # 50,000 RPM
        "malicious_pressure": build_modbus_tcp_packet(4, 1, 6, 1003, 1000),    # 1000 PSI
        
        # Invalid / Malformed Commands (Day 6 Validation)
        "invalid_function_code": build_modbus_tcp_packet(5, 1, 0x1F, 1001, 100), # FC 0x1F unsupported
        "invalid_register_address": build_modbus_tcp_packet(6, 1, 6, 9999, 100),  # Address out of range
        "invalid_unit_id": build_modbus_tcp_packet(7, 0, 6, 1001, 100),           # Unit ID 0 reserved
        "malformed_short_payload": b"\x00\x01\x00\x00\x00"                         # Truncated MBAP
    }

if __name__ == "__main__":
    traffic = generate_expanded_traffic()
    for name, raw in traffic.items():
        print(f"[{name.upper()}] Raw Hex: {raw.hex()}")