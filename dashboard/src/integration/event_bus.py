from typing import Callable, List, Optional

from data.integration_event import IntegrationEvent


class EventBus:
    """
    Shared event bus for VoltGuard.

    Supports both:
        subscribe(callback)

    and the older:
        subscribe(event_type, callback)

    This keeps the existing dashboard pages compatible
    while allowing the new integration architecture to
    use the same event bus.
    """

    def __init__(self) -> None:
        self._subscribers: List[
            tuple[
                Optional[str],
                Callable[[IntegrationEvent], None],
            ]
        ] = []

    def subscribe(
        self,
        event_type_or_callback,
        callback=None,
    ) -> None:
        """
        Register an event listener.

        Supported forms:

        subscribe(callback)

        subscribe(event_type, callback)
        """

        if callback is None:
            event_type = None
            subscriber = event_type_or_callback

        else:
            event_type = str(
                event_type_or_callback
            )
            subscriber = callback

        if not callable(subscriber):
            raise TypeError(
                "EventBus subscriber must be callable."
            )

        entry = (
            event_type,
            subscriber,
        )

        if entry not in self._subscribers:
            self._subscribers.append(
                entry
            )

    def unsubscribe(
        self,
        event_type_or_callback,
        callback=None,
    ) -> None:
        """
        Remove an event listener.

        Supports:

        unsubscribe(callback)

        unsubscribe(event_type, callback)
        """

        if callback is None:
            event_type = None
            subscriber = event_type_or_callback

        else:
            event_type = str(
                event_type_or_callback
            )
            subscriber = callback

        entry = (
            event_type,
            subscriber,
        )

        if entry in self._subscribers:
            self._subscribers.remove(
                entry
            )

    def publish(
        self,
        event: IntegrationEvent,
    ) -> None:
        """
        Publish an event to matching subscribers.
        """

        for (
            subscribed_type,
            subscriber,
        ) in list(self._subscribers):

            if (
                subscribed_type is not None
                and subscribed_type.lower()
                != event.event_type.lower()
            ):
                continue

            try:
                subscriber(event)

            except Exception as exc:
                print(
                    "Event subscriber error:",
                    exc,
                )

    def subscriber_count(self) -> int:
        """Return the number of active subscribers."""

        return len(
            self._subscribers
        )