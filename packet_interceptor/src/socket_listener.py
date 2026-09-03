import socket
import threading
import time
from typing import Callable, Optional
from src.stream_parser import StreamModbusParser
from src.normalizer import CommandNormalizer
from src.suspicious_detector import SuspiciousTrafficDetector
from src.logger import setup_logger

logger = setup_logger()

class ModbusSocketListener:
    """Real-time TCP Socket Listener for Modbus Interceptor Pipeline."""

    def __init__(self, host: str = "127.0.0.1", port: int = 5020, callback: Optional[Callable] = None):
        self.host = host
        self.port = port
        self.callback = callback
        self.server_socket: Optional[socket.socket] = None
        self.is_running = False
        self._thread: Optional[threading.Thread] = None

    def start(self):
        """Start socket listener in background thread."""
        self.is_running = True
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen(5)
        self.server_socket.settimeout(1.0)

        self._thread = threading.Thread(target=self._listen_loop, daemon=True)
        self._thread.start()
        logger.info(f"[NETWORK LISTENER] Interceptor active on {self.host}:{self.port}")

    def _listen_loop(self):
        while self.is_running:
            try:
                client_sock, addr = self.server_socket.accept()
                logger.info(f"[CONNECTION] Accepted traffic from {addr}")
                client_thread = threading.Thread(target=self._handle_client, args=(client_sock,), daemon=True)
                client_thread.start()
            except socket.timeout:
                continue
            except Exception as e:
                if self.is_running:
                    logger.error(f"[NETWORK ERROR] Socket exception: {e}")

    def _handle_client(self, client_sock: socket.socket):
        with client_sock:
            while self.is_running:
                try:
                    data = client_sock.recv(1024)
                    if not data:
                        break

                    # Step 1: Parse Stream
                    is_valid, parsed_pkt, err = StreamModbusParser.parse_stream(data)
                    if not is_valid:
                        logger.warning(f"[REJECTED] {err}")
                        continue

                    # Step 2: Extract normalized & suspicious indicators
                    logger.info(f"[STREAM RECV] TxID: {parsed_pkt['transaction_id']} | Reg: {parsed_pkt['register_address']} | Val: {parsed_pkt['value']}")

                    if self.callback:
                        self.callback(parsed_pkt)

                except Exception as e:
                    logger.error(f"[CLIENT HANDLER ERROR] {e}")
                    break

    def stop(self):
        """Safely shut down the socket server."""
        self.is_running = False
        if self._thread:
            self._thread.join(timeout=2.0)
        if self.server_socket:
            self.server_socket.close()
        logger.info("[NETWORK LISTENER] Socket server cleanly stopped.")