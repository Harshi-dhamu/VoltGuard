from dataclasses import dataclass
from typing import List

from data.integration_data import IntegrationEvent


@dataclass(frozen=True)
class EventLogEntry:
    """Represents one event displayed in the dashboard."""

    timestamp: str
    event_type: str
    source_module: str
    severity: str
    summary: str


class EventLog:
    """Maintains a bounded collection of recent events."""

    MAX_EVENTS = 200

    def __init__(self) -> None:
        self._events: List[EventLogEntry] = []

    def add_event(
        self,
        event: IntegrationEvent,
    ) -> EventLogEntry:
        """Convert and store an integration event."""

        entry = self._create_entry(
            event
        )

        self._events.insert(
            0,
            entry,
        )

        if len(self._events) > self.MAX_EVENTS:
            self._events.pop()

        return entry

    def get_events(
        self,
    ) -> List[EventLogEntry]:
        """Return a copy of recent events."""

        return list(self._events)

    def clear(self) -> None:
        """Clear the event history."""

        self._events.clear()

    def count(self) -> int:
        """Return number of stored events."""

        return len(self._events)

    def _create_entry(
        self,
        event: IntegrationEvent,
    ) -> EventLogEntry:
        """Convert an integration event."""

        severity = self._extract_severity(
            event
        )

        summary = self._create_summary(
            event
        )

        return EventLogEntry(
            timestamp=event.timestamp,
            event_type=event.event_type.upper(),
            source_module=event.source_module,
            severity=severity,
            summary=summary,
        )

    @staticmethod
    def _extract_severity(
        event: IntegrationEvent,
    ) -> str:
        """Extract severity from event payload."""

        payload = event.payload

        severity = payload.get(
            "severity"
        )

        if severity:
            return str(
                severity
            ).upper()

        if event.event_type == "packet":
            return "INFO"

        if event.event_type == "threat":
            return "HIGH"

        if event.event_type == "decision":
            return "MEDIUM"

        return "INFO"

    @staticmethod
    def _create_summary(
        event: IntegrationEvent,
    ) -> str:
        """Create a readable event summary."""

        payload = event.payload

        if event.event_type == "packet":
            source = payload.get(
                "source_ip",
                "Unknown",
            )

            destination = payload.get(
                "destination_ip",
                "Unknown",
            )

            protocol = payload.get(
                "protocol",
                "Unknown",
            )

            return (
                f"{protocol} traffic "
                f"{source} → {destination}"
            )

        if event.event_type == "threat":
            asset = payload.get(
                "asset",
                "Unknown asset",
            )

            category = payload.get(
                "category",
                "Unknown anomaly",
            )

            return (
                f"{category} detected "
                f"on {asset}"
            )

        if event.event_type == "decision":
            decision = payload.get(
                "decision",
                "UNKNOWN",
            )

            asset = payload.get(
                "asset",
                "Unknown asset",
            )

            return (
                f"{decision} decision "
                f"for {asset}"
            )

        return (
            f"Event received from "
            f"{event.source_module}"
        )