from typing import Any, Dict

from data.integration_event import IntegrationEvent
from integration.integration_manager import IntegrationManager


class PhysicsEngineAdapter:
    """
    Dashboard-side bridge for Physics Engine events.

    Converts the Physics Engine's IntegrationEvent-compatible
    dictionary into the common VoltGuard IntegrationEvent
    dataclass and publishes it through the existing
    IntegrationManager.

    This adapter does NOT create another EventBus.
    """

    SOURCE_MODULE = "physics_engine"
    EVENT_TYPE = "PROCESS_ANOMALY"

    def __init__(
        self,
        integration_manager: IntegrationManager,
    ) -> None:
        self.integration_manager = integration_manager

    def convert_to_integration_event(
        self,
        event_data: Dict[str, Any],
    ) -> IntegrationEvent:
        """
        Convert a Physics Engine event dictionary into
        the common VoltGuard IntegrationEvent object.
        """

        required_fields = (
            "event_id",
            "source_module",
            "event_type",
            "timestamp",
            "severity",
            "asset",
            "message",
            "payload",
        )

        missing_fields = [
            field
            for field in required_fields
            if field not in event_data
        ]

        if missing_fields:
            raise ValueError(
                "Physics Engine event is missing required fields: "
                + ", ".join(missing_fields)
            )

        if event_data["source_module"] != self.SOURCE_MODULE:
            raise ValueError(
                "Invalid source_module: "
                f"{event_data['source_module']}"
            )

        if event_data["event_type"] != self.EVENT_TYPE:
            raise ValueError(
                "Invalid event_type: "
                f"{event_data['event_type']}"
            )

        return IntegrationEvent(
            event_id=str(event_data["event_id"]),
            source_module=str(event_data["source_module"]),
            event_type=str(event_data["event_type"]),
            timestamp=str(event_data["timestamp"]),
            severity=str(event_data["severity"]),
            asset=str(event_data["asset"]),
            message=str(event_data["message"]),
            payload=dict(event_data["payload"]),
        )

    def publish_event(
        self,
        event_data: Dict[str, Any],
    ) -> bool:
        """
        Convert and publish a Physics Engine event
        through the central IntegrationManager/EventBus.
        """

        event = self.convert_to_integration_event(
            event_data
        )

        return self.integration_manager.receive_event(
            event
        )