import queue
from typing import Dict, Any, List, Optional, Callable
from src.event_bus_adapter import EventBusAdapter
from src.event_consumer import EventBusConsumer
from src.logger import setup_logger

logger = setup_logger()

class CentralEventBusDispatcher:
    """Central routing dispatcher bridging interceptor events to synchronous listeners and async consumers."""

    def __init__(self, async_buffer_size: int = 200):
        self.adapter = EventBusAdapter()
        self.consumer = EventBusConsumer(buffer_size=async_buffer_size)
        self.sync_listeners: List[Callable[[Dict[str, Any]], None]] = []

    def register_sync_listener(self, listener: Callable[[Dict[str, Any]], None]) -> None:
        """Registers a synchronous listener (e.g., central EventBus handler)."""
        self.sync_listeners.append(listener)
        logger.info("[DISPATCHER] Sync listener registered.")

    def start_async_pipeline(self) -> None:
        """Starts the background worker thread for async consumption."""
        self.consumer.start()

    def stop_async_pipeline(self) -> None:
        """Stops the background worker thread cleanly."""
        self.consumer.stop()

    def dispatch(self, analyzed_command: Dict[str, Any]) -> Dict[str, Any]:
        """Formats an analyzed packet and dispatches it to sync listeners and async queue."""
        event = self.adapter.publish_event(analyzed_command)

        # 1. Dispatch to synchronous listeners
        for listener in self.sync_listeners:
            try:
                listener(event)
            except Exception as e:
                logger.error(f"[DISPATCHER] Error in sync listener: {e}")

        # 2. Dispatch to async background queue
        self.consumer.enqueue_event(event)

        return event