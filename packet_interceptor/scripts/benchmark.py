import time
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.parser import ModbusParser
from src.validator import PacketValidator
from src.normalizer import CommandNormalizer
from src.suspicious_detector import SuspiciousTrafficDetector
from scripts.mock_generator import build_modbus_tcp_packet

def run_benchmark(num_packets: int = 10000):
    print(f"Starting performance benchmark with {num_packets:,} packets...")
    
    # Generate test binary payload
    raw_packet = build_modbus_tcp_packet(1, 1, 6, 1001, 2500)
    
    start_time = time.perf_counter()
    
    for i in range(num_packets):
        pkt = ModbusParser.parse_packet(raw_packet)
        is_valid, _ = PacketValidator.validate(pkt)
        if is_valid:
            norm = CommandNormalizer.normalize(pkt)
            _ = SuspiciousTrafficDetector.analyze(norm)

    end_time = time.perf_counter()
    duration = end_time - start_time
    throughput = num_packets / duration

    print("==================================================")
    print("           BENCHMARK RESULTS SUMMARY              ")
    print("==================================================")
    print(f"Total Packets Processed : {num_packets:,}")
    print(f"Total Time Taken        : {duration:.4f} seconds")
    print(f"Throughput Rate         : {throughput:,.2f} packets/second")
    print(f"Average Latency         : {(duration / num_packets) * 1000:.4f} ms/packet")
    print("==================================================")

if __name__ == "__main__":
    run_benchmark(10000)