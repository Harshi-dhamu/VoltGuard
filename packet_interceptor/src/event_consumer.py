import asyncio
import queue
import threading
from typing import Dict, Any, Callable, Optional
from src.logger import setup_logger

logger = setup_logger()

class AsyncEventConsumer:
    """Asynchronously consumes packet events and passes them to risk/analytics channels."""

    def __init__(self, handler_callback: Optional[Callable[[Dict[str, Any]], None]] = None):
        self.handler_callback = handler_callback
        self.queue = asyncio.Queue()
        self.is_running = False

    async def enqueue_event(self, event: Dict[str, Any]):
        """Queues an event for non-blocking asynchronous processing."""
        await self.queue.put(event)

    async def start_consumer(self):
        """Worker loop processing incoming pipeline events."""
        self.is_running = True
        logger.info("[ASYNC CONSUMER] Event processing worker started.")
        try:
            while self.is_running:
                event = await self.queue.get()
                if event is None:  # Shutdown signal
                    break
                try:
                    if self.handler_callback:
                        if asyncio.iscoroutinefunction(self.handler_callback):
                            await self.handler_callback(event)
                        else:
                            self.handler_callback(event)
                except Exception as err:
                    logger.error(f"[ASYNC CONSUMER] Processing error for event {event.get('event_id')}: {err}")
                finally:
                    self.queue.task_done()
        except asyncio.CancelledError:
            pass

    def stop_consumer(self):
        """Stops the worker loop cleanly."""
        self.is_running = False


class EventBusConsumer:
    """Consumes events on a background thread for the synchronous dispatcher."""

    def __init__(self, buffer_size: int = 200):
        self.queue = queue.Queue(maxsize=buffer_size)
        self.consumed_events = []
        self.is_running = False
        self._worker = None

    def _consume(self):
        while self.is_running:
            try:
                event = self.queue.get(timeout=0.1)
            except queue.Empty:
                continue
            try:
                self.consumed_events.append(event)
            finally:
                self.queue.task_done()

    def start(self):
        if self.is_running:
            return
        self.is_running = True
        self._worker = threading.Thread(target=self._consume, daemon=True)
        self._worker.start()

    def enqueue_event(self, event: Dict[str, Any]) -> bool:
        try:
            self.queue.put_nowait(event)
            return True
        except queue.Full:
            logger.warning("[EVENT CONSUMER] Event queue is full.")
            return False

    def stop(self):
        self.is_running = False
        if self._worker:
            self._worker.join(timeout=1.0)
            self._worker = None