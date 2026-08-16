import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.parser import ModbusParser, ModbusParserError
from src.validator import PacketValidator
from src.normalizer import CommandNormalizer
from src.suspicious_detector import SuspiciousTrafficDetector
from src.physics_interface import PhysicsEngineInterface
from scripts.mock_generator import generate_expanded_traffic

def run_pipeline():
    physics_interface = PhysicsEngineInterface()
    traffic = generate_expanded_traffic()

    print("==================================================")
    print("      VOLTGUARD PACKET INTERCEPTOR PIPELINE       ")
    print("==================================================\n")

    for scenario, raw_bytes in traffic.items():
        print(f"--- Scenario: {scenario} ---")
        try:
            # Step 1: Parse
            packet = ModbusParser.parse_packet(raw_bytes)
            
            # Step 2: Validate (Day 6)
            is_valid, validation_msg = PacketValidator.validate(packet)
            if not is_valid:
                print(f"[REJECTED] Validation Failed: {validation_msg}\n")
                continue

            # Step 3: Normalize (Day 5)
            normalized = CommandNormalizer.normalize(packet)

            # Step 4: Analyze Suspicious Parameters (Day 9)
            analyzed = SuspiciousTrafficDetector.analyze(normalized)
            if analyzed.is_suspicious:
                print(f"[WARNING] Suspicious Parameter Pre-Flagged: {analyzed.suspicious_reason}")

            # Step 5: Interface to Physics Engine (Day 8)
            physics_interface.send_to_physics_engine(analyzed)
            print()

        except ModbusParserError as e:
            print(f"[ERROR] Parsing Failed: {e}\n")

if __name__ == "__main__":
    run_pipeline()