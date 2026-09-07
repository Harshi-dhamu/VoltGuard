import time
from typing import Dict, Any, Callable, Optional
from src.inline_pipeline import InlineInterceptorPipeline
from src.event_bus_adapter import EventBusAdapter
from src.logger import setup_logger

logger = setup_logger()

class EventBusIntegrationHandler:
    """Integrated handler connecting inline pipeline, decision engine, and event bus adapter."""

    def __init__(self, event_bus_callback: Optional[Callable[[Dict[str, Any]], None]] = None):
        self.pipeline = InlineInterceptorPipeline()
        self.adapter = EventBusAdapter()
        self.event_bus_callback = event_bus_callback

    def process_and_emit(self, raw_bytes: bytes) -> Dict[str, Any]:
        """Runs raw bytes through pipeline, evaluates enforcement, and emits formatted event."""
        # 1. Process packet through pipeline using process_raw_stream_inline
        resolved = self.pipeline.process_raw_stream_inline(raw_bytes)

        # 2. Format integration event based on pipeline output
        event = self.adapter.format_integration_event(resolved)

        # 3. Emit event to callback if registered
        if self.event_bus_callback:
            self.event_bus_callback(event)

        return event