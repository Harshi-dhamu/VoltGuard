import asyncio
import logging
from typing import Dict, Any, Optional

from .socket_listener import ModbusSocketListener
from .stream_parser import StreamModbusParser
from .validator import PacketValidator
from .normalizer import CommandNormalizer
from .physics_interface import PhysicsEngineInterface
from .logger import setup_logger

logger = setup_logger()


class InterceptorEngine:
    """
    Day 25 Engine: Bridges the threaded SocketListener with an async processing queue
    and dispatches normalized events to Dhruti's Physics Interface.
    """
    def __init__(
        self,
        host: str = "127.0.0.1",
        port: int = 5020,
        max_queue_size: int = 1000,
        physics_interface: Optional[PhysicsEngineInterface] = None
    ):
        self.host = host
        self.port = port
        self.packet_queue: asyncio.Queue = asyncio.Queue(maxsize=max_queue_size)
        self.is_running = False

        # Core Pipeline Components
        self.validator = PacketValidator() if hasattr(PacketValidator, 'validate') else None
        self.normalizer = CommandNormalizer()
        self.physics_interface = physics_interface or PhysicsEngineInterface()
        self.listener = ModbusSocketListener(self.host, self.port, callback=self._on_raw_packet_received)

        self._worker_task: Optional[asyncio.Task] = None
        self._loop: Optional[asyncio.AbstractEventLoop] = None

    def _on_raw_packet_received(self, parsed_pkt: Dict[str, Any]):
        """Thread-safe callback invoked by ModbusSocketListener."""
        if self._loop and self.is_running:
            asyncio.run_coroutine_threadsafe(
                self.enqueue_packet(parsed_pkt), self._loop
            )

    async def enqueue_packet(self, packet_data: Dict[str, Any]) -> bool:
        """Producer callback: Enqueues incoming parsed stream dict with backpressure handling."""
        try:
            self.packet_queue.put_nowait(packet_data)
            return True
        except asyncio.QueueFull:
            logger.error("Queue limit reached! Dropping packet to prevent pipeline memory exhaustion.")
            return False

    async def _process_queue_worker(self):
        """Consumer worker: Pulls queued packets, normalizes, and dispatches to Physics Engine."""
        logger.info("Async queue consumer worker started.")
        while self.is_running:
            try:
                packet = await self.packet_queue.get()

                # Step 1: Normalize
                if hasattr(self.normalizer, 'normalize'):
                    normalized_cmd = self.normalizer.normalize(packet)
                else:
                    normalized_cmd = packet

                # Step 2: Dispatch to Physics Interface
                if hasattr(self.physics_interface, 'send_to_physics_engine'):
                    self.physics_interface.send_to_physics_engine(normalized_cmd)

                self.packet_queue.task_done()

            except asyncio.CancelledError:
                break
            except Exception as e:
                logger.error(f"Error processing packet in engine loop: {e}", exc_info=True)

    async def start(self):
        """Starts the worker task and network socket listener."""
        self.is_running = True
        self._loop = asyncio.get_running_loop()

        # Start Async Worker Task
        self._worker_task = asyncio.create_task(self._process_queue_worker())

        # Start Threaded Socket Listener
        self.listener.start()
        logger.info(f"Interceptor Engine running on {self.host}:{self.port}")

    async def stop(self):
        """Gracefully shuts down listener and queue worker."""
        self.is_running = False
        self.listener.stop()

        if self._worker_task:
            self._worker_task.cancel()
            await asyncio.gather(self._worker_task, return_exceptions=True)

        logger.info("Interceptor Engine cleanly stopped.")