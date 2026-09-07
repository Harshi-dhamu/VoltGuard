from dataclasses import dataclass
from datetime import datetime
from typing import Any, Dict


@dataclass
class IntegrationEvent:
    """
    Standard event exchanged between VoltGuard modules.

    Every module should eventually convert its output
    into this common structure before publishing it.
    """

    event_id: str
    source_module: str
    event_type: str
    timestamp: str
    severity: str
    asset: str
    message: str
    payload: Dict[str, Any]

    @classmethod
    def create(
        cls,
        event_id: str,
        source_module: str,
        event_type: str,
        severity: str,
        asset: str,
        message: str,
        payload: Dict[str, Any],
    ) -> "IntegrationEvent":
        """Create a timestamped integration event."""

        return cls(
            event_id=event_id,
            source_module=source_module,
            event_type=event_type,
            timestamp=datetime.now().strftime(
                "%Y-%m-%d %H:%M:%S"
            ),
            severity=severity,
            asset=asset,
            message=message,
            payload=payload,
        )

    def to_dict(self) -> Dict[str, Any]:
        """Convert the event into a dictionary."""

        return {
            "event_id": self.event_id,
            "source_module": self.source_module,
            "event_type": self.event_type,
            "timestamp": self.timestamp,
            "severity": self.severity,
            "asset": self.asset,
            "message": self.message,
            "payload": self.payload,
        }