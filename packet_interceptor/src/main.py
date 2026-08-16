import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.parser import ModbusParser, ModbusParserError
from src.validator import PacketValidator
from src.normalizer import CommandNormalizer
from scripts.mock_generator import generate_sample_traffic

def process_raw_stream(raw_data: bytes):
    try:
        packet = ModbusParser.parse_packet(raw_data)
        is_valid, msg = PacketValidator.validate(packet)
        if not is_valid:
            print(f"[WARNING] Packet Rejected: {msg}")
            return None

        normalized = CommandNormalizer.normalize(packet)
        print(f"[INFO] Processed Device: {normalized.device_id} | Command: {normalized.command} | Value: {normalized.value} {normalized.unit}")
        return normalized.to_json()
    except ModbusParserError as e:
        print(f"[ERROR] Parsing Failed: {e}")
        return None

if __name__ == "__main__":
    print("=== VoltGuard Packet Interceptor ===")
    traffic = generate_sample_traffic()
    for name, raw_bytes in traffic.items():
        print(f"\nScenario: {name}")
        json_output = process_raw_stream(raw_bytes)
        if json_output:
            print("Normalized Payload for Physics Engine (Dhruti):")
            print(json_output)