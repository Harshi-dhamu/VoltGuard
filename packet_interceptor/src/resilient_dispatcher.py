import time
from typing import Dict, Any, List, Callable, Optional
from collections import deque
from src.logger import setup_logger

logger = setup_logger()

class CircuitBreakerOpenException(Exception):
    """Raised when attempting to dispatch through an OPEN circuit breaker."""
    pass

class ResilientEventDispatcher:
    """Handles event routing with fault isolation, circuit breaking, and DLQ overflow management."""

    def __init__(
        self,
        max_retries: int = 3,
        failure_threshold: int = 5,
        recovery_time_sec: float = 10.0,
        dlq_capacity: int = 100
    ):
        self.max_retries = max_retries
        self.failure_threshold = failure_threshold
        self.recovery_time_sec = recovery_time_sec
        self.dlq_capacity = dlq_capacity

        self.subscribers: List[Callable[[Dict[str, Any]], None]] = []
        self.dlq: deque = deque(maxlen=dlq_capacity)

        # Circuit Breaker State: "CLOSED", "OPEN", "HALF-OPEN"
        self.state = "CLOSED"
        self.consecutive_failures = 0
        self.last_failure_time = 0.0

    def register_subscriber(self, callback: Callable[[Dict[str, Any]], None]):
        """Registers a listener callback for event distribution."""
        if callback not in self.subscribers:
            self.subscribers.append(callback)

    def _check_circuit_state(self):
        """Updates and checks circuit breaker status based on elapsed time."""
        if self.state == "OPEN":
            if time.time() - self.last_failure_time >= self.recovery_time_sec:
                self.state = "HALF-OPEN"
                logger.info("[CIRCUIT BREAKER] Transitioned to HALF-OPEN state. Testing connection...")
            else:
                raise CircuitBreakerOpenException("Circuit breaker is OPEN. Fast-failing event dispatch.")

    def _on_success(self):
        """Resets failure counts upon successful dispatch."""
        self.consecutive_failures = 0
        if self.state == "HALF-OPEN":
            self.state = "CLOSED"
            logger.info("[CIRCUIT BREAKER] Connection recovered. Transitioned to CLOSED state.")

    def _on_failure(self):
        """Increments failure counter and opens circuit if threshold is reached."""
        self.consecutive_failures += 1
        self.last_failure_time = time.time()

        if self.consecutive_failures >= self.failure_threshold:
            self.state = "OPEN"
            logger.error(f"[CIRCUIT BREAKER] Failure threshold ({self.failure_threshold}) reached. Circuit OPENED.")

    def send_to_dlq(self, event: Dict[str, Any], error_reason: str):
        """Routes failed or overflowed events into the Dead Letter Queue."""
        dlq_entry = {
            "event": event,
            "failed_at": time.time(),
            "reason": error_reason
        }
        self.dlq.append(dlq_entry)
        logger.warning(f"[DLQ] Event {event.get('event_id', 'N/A')} queued in DLQ. Reason: {error_reason}")

    def dispatch(self, event: Dict[str, Any]) -> bool:
        """Dispatches event to subscribers with isolated fault handling and retries."""
        try:
            self._check_circuit_state()
        except CircuitBreakerOpenException as err:
            self.send_to_dlq(event, str(err))
            return False

        if not self.subscribers:
            logger.info("[DISPATCHER] No subscribers registered. Skipping dispatch.")
            return True

        dispatch_successful = True

        for subscriber in self.subscribers:
            delivered = False
            for attempt in range(1, self.max_retries + 1):
                try:
                    subscriber(event)
                    delivered = True
                    break
                except Exception as ex:
                    logger.warning(f"[DISPATCHER] Attempt {attempt}/{self.max_retries} failed for subscriber: {ex}")

            if delivered:
                self._on_success()
            else:
                dispatch_successful = False
                self._on_failure()
                self.send_to_dlq(event, f"Exceeded max retries ({self.max_retries}) for subscriber callback.")

        return dispatch_successful

    def get_dlq_size(self) -> int:
        """Returns the current number of events in the Dead Letter Queue."""
        return len(self.dlq)

    def purge_dlq(self) -> List[Dict[str, Any]]:
        """Drains and returns all items currently stored in the DLQ."""
        items = list(self.dlq)
        self.dlq.clear()
        return items