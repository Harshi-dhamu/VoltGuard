import queue
import time
from typing import Dict, Any, List, Optional, Callable
from src.event_dispatcher import CentralEventBusDispatcher
from src.logger import setup_logger

logger = setup_logger()

class ResilientEventBusDispatcher(CentralEventBusDispatcher):
    """Extended CentralEventBusDispatcher with dead-letter queue (DLQ) and fault-handling capabilities."""

    def __init__(self, async_buffer_size: int = 50, dlq_capacity: int = 500):
        super().__init__(async_buffer_size=async_buffer_size)
        self.dead_letter_queue: List[Dict[str, Any]] = []
        self.dlq_capacity = dlq_capacity
        self.dropped_event_count: int = 0

    def dispatch_safe(self, analyzed_command: Dict[str, Any]) -> Dict[str, Any]:
        """Dispatches event safely. If processing fails or buffer overflows, routes to Dead-Letter Queue."""
        try:
            event = self.adapter.publish_event(analyzed_command)

            # Route to synchronous listeners
            for listener in self.sync_listeners:
                try:
                    listener(event)
                except Exception as listener_err:
                    logger.error(f"[RESILIENT DISPATCHER] Sync listener failure: {listener_err}")
                    self._route_to_dlq(event, reason=f"ListenerError: {listener_err}")

            # Enqueue to async buffer
            enqueued = self.consumer.enqueue_event(event)
            if not enqueued:
                self._route_to_dlq(event, reason="AsyncBufferOverflow")

            return event

        except Exception as err:
            logger.error(f"[RESILIENT DISPATCHER] Core dispatch failure: {err}")
            fallback_event = {
                "source_module": "packet_interceptor",
                "event_type": "SYSTEM_FAULT",
                "severity": "CRITICAL",
                "message": f"Event dispatch failed: {str(err)}",
                "raw_command": str(analyzed_command),
                "timestamp": time.time()
            }
            self._route_to_dlq(fallback_event, reason=f"DispatchError: {err}")
            return fallback_event

    def _route_to_dlq(self, event: Dict[str, Any], reason: str) -> None:
        """Appends unhandled or overflowed events to Dead-Letter Queue for recovery inspection."""
        if len(self.dead_letter_queue) < self.dlq_capacity:
            event["dlq_reason"] = reason
            event["dlq_timestamp"] = time.time()
            self.dead_letter_queue.append(event)
            logger.warning(f"[DLQ ENQUEUE] Event routed to DLQ. Reason: {reason}")
        else:
            self.dropped_event_count += 1
            logger.error("[DLQ OVERFLOW] Dead-letter queue full! Dropping event permanently.")