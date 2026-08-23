from typing import Callable, Dict, List

from data.integration_data import IntegrationEvent


class EventBus:
    """
    Lightweight application event bus.

    Allows independent VoltGuard modules to publish
    events without directly depending on dashboard pages.
    """

    def __init__(self) -> None:
        self._subscribers: Dict[
            str,
            List[Callable[[IntegrationEvent], None]],
        ] = {}

    def subscribe(
        self,
        event_type: str,
        callback: Callable[
            [IntegrationEvent],
            None,
        ],
    ) -> None:
        """Subscribe to an event type."""

        if event_type not in self._subscribers:
            self._subscribers[event_type] = []

        if callback not in self._subscribers[event_type]:
            self._subscribers[event_type].append(
                callback
            )

    def unsubscribe(
        self,
        event_type: str,
        callback: Callable[
            [IntegrationEvent],
            None,
        ],
    ) -> None:
        """Remove an event subscription."""

        subscribers = self._subscribers.get(
            event_type,
            [],
        )

        if callback in subscribers:
            subscribers.remove(callback)

    def publish(
        self,
        event: IntegrationEvent,
    ) -> None:
        """Publish an event to all subscribers."""

        subscribers = self._subscribers.get(
            event.event_type,
            [],
        )

        for callback in list(subscribers):
            callback(event)

    def clear(self) -> None:
        """Remove all subscriptions."""

        self._subscribers.clear()