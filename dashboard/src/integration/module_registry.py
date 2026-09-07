from dataclasses import dataclass
from typing import Dict


@dataclass
class ModuleStatus:
    """Runtime status of a VoltGuard module."""

    name: str
    display_name: str
    status: str = "OFFLINE"
    events_received: int = 0
    last_event: str = "No events received"


class ModuleRegistry:
    """Tracks runtime status of VoltGuard modules."""

    def __init__(self) -> None:
        self._modules: Dict[
            str,
            ModuleStatus,
        ] = {}

        self.register(
            "packet_interceptor",
            "Packet Interceptor",
        )

        self.register(
            "physics_engine",
            "Physics Engine",
        )

        self.register(
            "decision_engine",
            "Decision Engine",
        )

    def register(
        self,
        name: str,
        display_name: str,
    ) -> None:
        """Register a module."""

        self._modules[name] = ModuleStatus(
            name=name,
            display_name=display_name,
        )

    def record_event(
        self,
        module_name: str,
        timestamp: str,
    ) -> None:
        """Record an event received from a module."""

        module = self._modules.get(
            module_name
        )

        if module is None:
            return

        module.events_received += 1
        module.last_event = timestamp
        module.status = "ONLINE"

    def set_status(
        self,
        module_name: str,
        status: str,
    ) -> None:
        """Manually update module status."""

        module = self._modules.get(
            module_name
        )

        if module is not None:
            module.status = status

    def get_statuses(
        self,
    ) -> Dict[str, ModuleStatus]:
        """Return all module statuses."""

        return dict(
            self._modules
        )

    def get_status(
        self,
        module_name: str,
    ) -> ModuleStatus | None:
        """Return one module status."""

        return self._modules.get(
            module_name
        )