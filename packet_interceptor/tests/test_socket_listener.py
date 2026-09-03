import pytest
import socket
import time
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.socket_listener import ModbusSocketListener
from scripts.mock_generator import build_modbus_tcp_packet

def test_socket_listener_live_stream():
    received_packets = []

    def test_callback(pkt):
        received_packets.append(pkt)

    listener = ModbusSocketListener(host="127.0.0.1", port=5021, callback=test_callback)
    listener.start()
    time.sleep(0.2) # Allow server thread spin-up

    # Simulate client network traffic
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(("127.0.0.1", 5021))
    
    # Send test binary Modbus TCP frame
    raw_pkt = build_modbus_tcp_packet(501, 1, 6, 1001, 2200)
    client.sendall(raw_pkt)
    time.sleep(0.2)
    
    client.close()
    listener.stop()

    assert len(received_packets) == 1
    assert received_packets[0]["transaction_id"] == 501
    assert received_packets[0]["register_address"] == 1001
    assert received_packets[0]["value"] == 2200