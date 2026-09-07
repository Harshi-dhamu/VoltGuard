from .event_bus import EventBus
from .integration_manager import IntegrationManager


class ApplicationContext:
    """
    Shared runtime context for the VoltGuard dashboard.

    Provides one EventBus and one IntegrationManager
    for all dashboard pages.
    """

    def __init__(self) -> None:
        self.event_bus = EventBus()

        self.integration_manager = (
            IntegrationManager(
                self.event_bus
            )
        )