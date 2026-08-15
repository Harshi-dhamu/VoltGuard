import os
import sys

# Ensure module path is accessible
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from models.modbus_packet import ModbusPacket


def main():
    print("===========================================")
    print(" VoltGuard - Packet Interceptor (Python)   ")
    print("===========================================")

    # Test data structure initialization
    sample_packet = ModbusPacket(
        transaction_id=1001,
        protocol_id=0,
        length=6,
        unit_id=1,
        function_code=0x06,  # Write Single Register
        register_address=40001,
        register_value=1000,
    )

    print("[INFO] Initialized sample Modbus packet successfully:")
    sample_packet.print_summary()


if __name__ == "__main__":
    main()