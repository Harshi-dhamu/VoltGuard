from typing import Callable, List, Optional
import traceback

from data.integration_event import IntegrationEvent


class EventBus:
    """
    Shared event bus for VoltGuard.

    Supports:
        subscribe(callback)

    and:
        subscribe(event_type, callback)
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
            self._subscribers.append(entry)

    def unsubscribe(
        self,
        event_type_or_callback,
        callback=None,
    ) -> None:

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
            self._subscribers.remove(entry)

    def publish(
        self,
        event: IntegrationEvent,
    ) -> None:

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
                    "\n========== EVENT SUBSCRIBER ERROR =========="
                )

                print(
                    f"Subscriber: {subscriber}"
                )

                print(
                    f"Event: {event.event_type}"
                )

                print(
                    f"Error: {exc}"
                )

                traceback.print_exc()

                print(
                    "============================================\n"
                )

    def subscriber_count(self) -> int:
        return len(
            self._subscribers
        )