from dataclasses import dataclass
from typing import Dict


@dataclass
class SecurityMetrics:
    """Aggregated security metrics for the VoltGuard dashboard."""

    total_events: int = 0
    network_events: int = 0
    process_anomalies: int = 0
    security_decisions: int = 0
    critical_events: int = 0
    high_events: int = 0
    blocked_decisions: int = 0

    def process_event(
        self,
        event_type: str,
        severity: str,
        decision: str = "",
    ) -> None:
        """Update metrics from an integration event."""

        self.total_events += 1

        normalized_type = (
            event_type.strip().upper()
        )

        normalized_severity = (
            severity.strip().upper()
        )

        normalized_decision = (
            decision.strip().upper()
        )

        if normalized_type == "NETWORK_ANOMALY":
            self.network_events += 1

        elif normalized_type == "PROCESS_ANOMALY":
            self.process_anomalies += 1

        elif normalized_type == "SECURITY_DECISION":
            self.security_decisions += 1

        if normalized_severity == "CRITICAL":
            self.critical_events += 1

        elif normalized_severity == "HIGH":
            self.high_events += 1

        if normalized_decision == "BLOCK":
            self.blocked_decisions += 1

    def to_dict(self) -> Dict[str, int]:
        """Return metrics as a dictionary."""

        return {
            "total_events": self.total_events,
            "network_events": self.network_events,
            "process_anomalies": self.process_anomalies,
            "security_decisions": self.security_decisions,
            "critical_events": self.critical_events,
            "high_events": self.high_events,
            "blocked_decisions": self.blocked_decisions,
        }