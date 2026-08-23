from typing import Any, Dict

from data.integration_data import (
    IntegrationEvent,
)


class ModuleAdapter:
    """
    Base adapter for external VoltGuard modules.

    External modules should communicate through
    this boundary instead of directly manipulating
    dashboard widgets.
    """

    module_name = "Unknown Module"

    def normalize(
        self,
        data: Dict[str, Any],
    ) -> IntegrationEvent:
        """
        Convert external module output into
        a standard VoltGuard event.
        """

        raise NotImplementedError


class PacketInterceptorAdapter(
    ModuleAdapter
):
    """Adapter for Tanvi's Packet Interceptor."""

    module_name = "Packet Interceptor"

    def normalize(
        self,
        data: Dict[str, Any],
    ) -> IntegrationEvent:

        return IntegrationEvent.create(
            event_type="packet",
            source_module=self.module_name,
            payload=data,
        )


class PhysicsEngineAdapter(
    ModuleAdapter
):
    """Adapter for Dhruti's Physics Engine."""

    module_name = "Physics Engine"

    def normalize(
        self,
        data: Dict[str, Any],
    ) -> IntegrationEvent:

        return IntegrationEvent.create(
            event_type="threat",
            source_module=self.module_name,
            payload=data,
        )


class DecisionEngineAdapter(
    ModuleAdapter
):
    """Adapter for Akhina's Decision Engine."""

    module_name = "Decision Engine"

    def normalize(
        self,
        data: Dict[str, Any],
    ) -> IntegrationEvent:

        return IntegrationEvent.create(
            event_type="decision",
            source_module=self.module_name,
            payload=data,
        )