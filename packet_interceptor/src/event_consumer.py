import asyncio
import queue
import threading
import time
from typing import Dict, Any, List, Optional
from src.logger import setup_logger

logger = setup_logger()

class EventBusConsumer:
    """Asynchronous background consumer for processing emitted IntegrationEvents."""

    def __init__(self, buffer_size: int = 100):
        self.event_queue: queue.Queue = queue.Queue(maxsize=buffer_size)
        self.consumed_events: List[Dict[str, Any]] = []
        self._is_running: bool = False
        self._worker_thread: Optional[threading.Thread] = None

    def enqueue_event(self, event: Dict[str, Any]) -> bool:
        """Thread-safe enqueue operation for incoming IntegrationEvents."""
        try:
            self.event_queue.put(event, block=False)
            return True
        except queue.Full:
            logger.warning("[EVENT CONSUMER] Event queue full! Dropping event.")
            return False

    def start(self) -> None:
        """Starts background worker thread to process queued events."""
        self._is_running = True
        self._worker_thread = threading.Thread(target=self._process_queue, daemon=True)
        self._worker_thread.start()
        logger.info("[EVENT CONSUMER] Background consumer thread started.")

    def stop(self) -> None:
        """Stops background worker thread cleanly."""
        self._is_running = False
        if self._worker_thread and self._worker_thread.is_alive():
            self._worker_thread.join(timeout=2.0)
        logger.info("[EVENT CONSUMER] Background consumer thread stopped.")

    def _process_queue(self) -> None:
        """Internal worker loop consuming events from the queue."""
        while self._is_running:
            try:
                event = self.event_queue.get(timeout=0.2)
                self.consumed_events.append(event)
                logger.info(
                    f"[EVENT CONSUMED] ID: {event.get('event_id')} | "
                    f"Type: {event.get('event_type')} | Severity: {event.get('severity')}"
                )
                self.event_queue.task_done()
            except queue.Empty:
                continue