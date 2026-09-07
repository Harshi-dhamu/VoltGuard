from typing import Any, Dict

from data.integration_event import IntegrationEvent
from integration.integration_manager import IntegrationManager


class PacketInterceptorAdapter:
    """
    Adapter between the Packet Interceptor module and
    VoltGuard's central IntegrationManager.

    Converts the Packet Interceptor's event dictionary
    into the common IntegrationEvent dataclass.
    """

    def __init__(
        self,
        integration_manager: IntegrationManager,
    ) -> None:
        self._integration_manager = integration_manager

    def publish_event(
        self,
        event_data: Dict[str, Any],
    ) -> bool:
        """
        Convert a Packet Interceptor event dictionary
        into IntegrationEvent and publish it centrally.
        """

        if not isinstance(event_data, dict):
            raise TypeError(
                "Packet Interceptor event must be a dictionary."
            )

        required_fields = (
            "event_id",
            "source_module",
            "event_type",
            "severity",
            "asset",
            "message",
        )

        missing_fields = [
            field
            for field in required_fields
            if not event_data.get(field)
        ]

        if missing_fields:
            raise ValueError(
                "Packet Interceptor event is missing "
                f"required fields: {missing_fields}"
            )

        event = IntegrationEvent(
            event_id=str(
                event_data["event_id"]
            ),
            source_module=str(
                event_data["source_module"]
            ),
            event_type=str(
                event_data["event_type"]
            ),
            timestamp=str(
                event_data.get(
                    "timestamp",
                    "",
                )
            ),
            severity=str(
                event_data["severity"]
            ),
            asset=str(
                event_data["asset"]
            ),
            message=str(
                event_data["message"]
            ),
            payload=dict(
                event_data.get(
                    "payload",
                    {},
                )
            ),
        )

        # If the Packet Interceptor doesn't provide a
        # timestamp, create one using the standard factory.
        if not event.timestamp:
            event = IntegrationEvent.create(
                event_id=event.event_id,
                source_module=event.source_module,
                event_type=event.event_type,
                severity=event.severity,
                asset=event.asset,
                message=event.message,
                payload=event.payload,
            )

        return self._integration_manager.receive_event(
            event
        )


__all__ = [
    "PacketInterceptorAdapter",
]