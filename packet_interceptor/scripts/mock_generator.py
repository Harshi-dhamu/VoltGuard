import struct

def build_modbus_tcp_packet(transaction_id: int, unit_id: int, function_code: int, register: int, value: int) -> bytes:
    pdu = struct.pack(">BHH", function_code, register, value)
    length = len(pdu) + 1
    mbap = struct.pack(">HHHB", transaction_id, 0, length, unit_id)
    return mbap + pdu

def generate_sample_traffic():
    return {
        "normal_pump": build_modbus_tcp_packet(1, 1, 6, 1001, 1000),      # 1000 RPM (Normal)
        "normal_valve": build_modbus_tcp_packet(2, 1, 6, 1002, 50),        # 50% Position (Normal)
        "malicious_pump": build_modbus_tcp_packet(3, 1, 6, 1001, 50000),   # 50,000 RPM (Malicious)
        "malicious_pressure": build_modbus_tcp_packet(4, 1, 6, 1003, 1000) # 1000 PSI (Malicious)
    }

if __name__ == "__main__":
    traffic = generate_sample_traffic()
    for name, raw in traffic.items():
        print(f"[{name.upper()}] Raw Hex: {raw.hex()}")