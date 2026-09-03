import json
from typing import Any, Dict

from data.integration_event import IntegrationEvent
from integration.integration_manager import IntegrationManager


class DecisionEngineAdapter:
    """
    Converts Decision Engine output into the common
    VoltGuard IntegrationEvent format.

    The adapter uses the existing IntegrationManager
    and central EventBus.

    No new EventBus is created here.
    """

    SOURCE_MODULE = "decision_engine"
    EVENT_TYPE = "SECURITY_DECISION"

    def __init__(
        self,
        integration_manager: IntegrationManager,
    ) -> None:
        self.integration_manager = integration_manager

    def parse_event(
        self,
        decision_json: str,
    ) -> IntegrationEvent:
        """
        Convert Decision Engine JSON into IntegrationEvent.
        """

        try:
            data: Dict[str, Any] = json.loads(
                decision_json
            )
        except json.JSONDecodeError as exc:
            raise ValueError(
                "Invalid Decision Engine JSON"
            ) from exc

        return self.from_dict(data)

    def from_dict(
        self,
        data: Dict[str, Any],
    ) -> IntegrationEvent:
        """
        Convert Decision Engine event dictionary
        into the common IntegrationEvent.
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
            if field not in data
        ]

        if missing_fields:
            raise ValueError(
                "Missing required fields: "
                + ", ".join(missing_fields)
            )

        if data["source_module"] != self.SOURCE_MODULE:
            raise ValueError(
                "Unexpected source_module: "
                f"{data['source_module']}"
            )

        if data["event_type"] != self.EVENT_TYPE:
            raise ValueError(
                "Unexpected event_type: "
                f"{data['event_type']}"
            )

        if not isinstance(
            data["payload"],
            dict,
        ):
            raise ValueError(
                "Decision Engine payload must be a dictionary"
            )

        return IntegrationEvent(
            event_id=str(data["event_id"]),
            source_module=str(
                data["source_module"]
            ),
            event_type=str(
                data["event_type"]
            ),
            timestamp=str(
                data["timestamp"]
            ),
            severity=str(
                data["severity"]
            ),
            asset=str(
                data["asset"]
            ),
            message=str(
                data["message"]
            ),
            payload=data["payload"],
        )

    def publish_json(
        self,
        decision_json: str,
    ) -> bool:
        """
        Convert Decision Engine JSON into an
        IntegrationEvent and publish it through
        the existing IntegrationManager.
        """

        event = self.parse_event(
            decision_json
        )

        return self.integration_manager.receive_event(
            event
        )

    def publish_dict(
        self,
        decision_data: Dict[str, Any],
    ) -> bool:
        """
        Convert a Decision Engine dictionary into
        IntegrationEvent and publish it.
        """

        event = self.from_dict(
            decision_data
        )

        return self.integration_manager.receive_event(
            event
        )