from typing import Any, Dict

from data.integration_event import IntegrationEvent

from .event_bus import EventBus
from .module_registry import ModuleRegistry, ModuleStatus


class IntegrationManager:
    """
    Central integration coordinator for VoltGuard.

    Responsibilities:
    - Receive module events
    - Validate integration events
    - Update module status
    - Publish normalized events through EventBus
    - Provide runtime integration status
    """

    def __init__(
        self,
        event_bus: EventBus | None = None,
    ) -> None:
        """
        Initialize the integration manager.

        ApplicationContext supplies the shared EventBus.
        """

        self.event_bus = (
            event_bus
            if event_bus is not None
            else EventBus()
        )

        self.registry = ModuleRegistry()

        self._total_events = 0

        self._last_event: (
            IntegrationEvent | None
        ) = None

    def receive_event(
        self,
        event: IntegrationEvent,
    ) -> bool:
        """
        Receive an IntegrationEvent.

        Events are validated, recorded in the module
        registry, stored as the latest event, and then
        distributed through the shared EventBus.
        """

        if not self._validate_event(event):
            return False

        self._total_events += 1

        module_key = (
            self._normalize_module_name(
                event.source_module
            )
        )

        self.registry.record_event(
            module_key,
            event.timestamp,
        )

        self._last_event = event

        self.event_bus.publish(
            event
        )

        return True

    def publish_event(
        self,
        event: IntegrationEvent,
    ) -> bool:
        """
        Publish an IntegrationEvent.

        Kept as a compatibility method for existing
        VoltGuard modules.
        """

        return self.receive_event(
            event
        )

    def _validate_event(
        self,
        event: IntegrationEvent,
    ) -> bool:
        """
        Validate an IntegrationEvent.

        Uses the actual IntegrationEvent dataclass
        defined in data/integration_event.py.
        """

        if not isinstance(
            event,
            IntegrationEvent,
        ):
            print(
                "IntegrationManager: "
                "received unsupported event type:",
                type(event).__name__,
            )
            return False

        required_values = (
            event.event_id,
            event.source_module,
            event.event_type,
            event.timestamp,
            event.severity,
            event.asset,
            event.message,
        )

        return all(
            bool(value)
            for value in required_values
        )

    def _normalize_module_name(
        self,
        module_name: str,
    ) -> str:
        """Normalize module names for registry lookup."""

        return (
            module_name
            .strip()
            .lower()
            .replace(" ", "_")
        )

    def get_status(
        self,
    ) -> Dict[str, Any]:
        """
        Return complete integration status.
        """

        return {
            "total_events": (
                self._total_events
            ),
            "subscriber_count": (
                self.event_bus.subscriber_count()
            ),
            "modules": (
                self.registry.get_statuses()
            ),
            "last_event": (
                self._last_event.to_dict()
                if self._last_event is not None
                else None
            ),
        }

    def get_module_status(
        self,
        module_name: str,
    ) -> ModuleStatus | None:
        """Return status for one module."""

        return self.registry.get_status(
            self._normalize_module_name(
                module_name
            )
        )


__all__ = [
    "IntegrationManager",
    "ModuleStatus",
]