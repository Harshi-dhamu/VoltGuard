from dataclasses import dataclass
from typing import Dict

from data.integration_data import (
    IntegrationEvent,
)

from .event_bus import EventBus


@dataclass
class ModuleStatus:
    """Runtime status of a VoltGuard module."""

    name: str
    connected: bool = False
    events_received: int = 0
    last_event: str = "Never"


class IntegrationManager:
    """
    Coordinates communication between VoltGuard modules
    and the dashboard.
    """

    MODULES = (
        "Packet Interceptor",
        "Physics Engine",
        "Decision Engine",
    )

    def __init__(
        self,
        event_bus: EventBus,
    ) -> None:
        self.event_bus = event_bus

        self._modules: Dict[
            str,
            ModuleStatus,
        ] = {
            name: ModuleStatus(name=name)
            for name in self.MODULES
        }

        self._register_event_handlers()

    def _register_event_handlers(self) -> None:
        """Register module event listeners."""

        self.event_bus.subscribe(
            "packet",
            self._handle_packet,
        )

        self.event_bus.subscribe(
            "threat",
            self._handle_threat,
        )

        self.event_bus.subscribe(
            "decision",
            self._handle_decision,
        )

    def _handle_packet(
        self,
        event: IntegrationEvent,
    ) -> None:
        """Process packet interceptor events."""

        self._record_module_event(
            "Packet Interceptor",
            event,
        )

    def _handle_threat(
        self,
        event: IntegrationEvent,
    ) -> None:
        """Process physics engine events."""

        self._record_module_event(
            "Physics Engine",
            event,
        )

    def _handle_decision(
        self,
        event: IntegrationEvent,
    ) -> None:
        """Process decision engine events."""

        self._record_module_event(
            "Decision Engine",
            event,
        )

    def _record_module_event(
        self,
        module_name: str,
        event: IntegrationEvent,
    ) -> None:
        """Update module runtime information."""

        module = self._modules.get(
            module_name
        )

        if module is None:
            return

        module.connected = True
        module.events_received += 1
        module.last_event = event.timestamp

    def get_status(
        self,
    ) -> Dict[str, ModuleStatus]:
        """Return current module statuses."""

        return {
            name: ModuleStatus(
                name=status.name,
                connected=status.connected,
                events_received=status.events_received,
                last_event=status.last_event,
            )
            for name, status
            in self._modules.items()
        }

    def mark_connected(
        self,
        module_name: str,
    ) -> None:
        """Mark a module as connected."""

        module = self._modules.get(
            module_name
        )

        if module is not None:
            module.connected = True