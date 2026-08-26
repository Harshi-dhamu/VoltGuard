import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.parser import ModbusParser, ModbusParserError
from src.validator import PacketValidator
from src.normalizer import CommandNormalizer
from src.suspicious_detector import SuspiciousTrafficDetector
from src.physics_interface import PhysicsEngineInterface
from src.logger import setup_logger
from scripts.mock_generator import generate_expanded_traffic

def run_pipeline():
    logger = setup_logger()
    physics_interface = PhysicsEngineInterface()
    traffic = generate_expanded_traffic()

    logger.info("==================================================")
    logger.info("      VOLTGUARD PACKET INTERCEPTOR PIPELINE       ")
    logger.info("==================================================\n")

    for scenario, raw_bytes in traffic.items():
        logger.info(f"--- Processing Scenario: {scenario} ---")
        try:
            # Step 1: Parse
            packet = ModbusParser.parse_packet(raw_bytes)
            logger.info(f"Parsed TxID: {packet.transaction_id}, FC: {packet.function_code}, Register: {packet.register_address}")

            # Step 2: Validate
            is_valid, validation_msg = PacketValidator.validate(packet)
            if not is_valid:
                logger.warning(f"[REJECTED] Validation Failed: {validation_msg}\n")
                continue

            # Step 3: Normalize
            normalized = CommandNormalizer.normalize(packet)

            # Step 4: Detect Suspicious Traffic
            analyzed = SuspiciousTrafficDetector.analyze(normalized)
            if analyzed.is_suspicious:
                logger.warning(f"[SUSPICIOUS DETECTED] {analyzed.suspicious_reason}")

            # Step 5: Send to Physics Interface
            physics_interface.send_to_physics_engine(analyzed)
            logger.info(f"[DISPATCHED] {analyzed.device_id} -> {analyzed.command}: {analyzed.value} {analyzed.unit}\n")

        except ModbusParserError as e:
            logger.error(f"[PARSER ERROR] {e}\n")

if __name__ == "__main__":
    run_pipeline()