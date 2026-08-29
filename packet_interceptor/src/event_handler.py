from typing import Dict, Any, Callable, Optional
from src.inline_pipeline import InlineInterceptorPipeline
from src.event_bus_adapter import EventBusAdapter
from src.logger import setup_logger

logger = setup_logger()

class EventBusIntegrationHandler:
    """End-to-end handler bridging Inline Pipeline and VoltGuard EventBus."""

    def __init__(self, event_bus_callback: Optional[Callable[[Dict[str, Any]], None]] = None):
        self.pipeline = InlineInterceptorPipeline()
        self.adapter = EventBusAdapter()
        self.event_bus_callback = event_bus_callback or self._default_event_bus_listener

    def _default_event_bus_listener(self, event: Dict[str, Any]) -> None:
        """Default listener logging generated IntegrationEvents."""
        logger.info(f"[EVENT BUS DISPATCH] Event ID: {event.get('event_id')} | Type: {event.get('event_type')}")

    def process_and_emit(self, raw_bytes: bytes) -> Dict[str, Any]:
        """Processes raw bytes inline and emits structured IntegrationEvent to EventBus."""
        resolved_pkt = self.pipeline.process_raw_stream_inline(raw_bytes)

        if resolved_pkt.get("status") == "REJECTED":
            return resolved_pkt

        parsed_data = resolved_pkt.get("parsed_pkt", {}).copy()
        parsed_data["status"] = resolved_pkt.get("status")

        integration_event = self.adapter.publish_event(parsed_data)

        if self.event_bus_callback:
            self.event_bus_callback(integration_event)

        return integration_event