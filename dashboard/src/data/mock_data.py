from dataclasses import dataclass
from typing import List


@dataclass(frozen=True)
class MetricData:
    """Represents a dashboard metric."""

    label: str
    value: str
    description: str
    status: str


@dataclass(frozen=True)
class AlertData:
    """Represents a security alert."""

    severity: str
    asset: str
    message: str
    timestamp: str


@dataclass(frozen=True)
class ActivityData:
    """Represents network activity."""

    timestamp: str
    source: str
    destination: str
    protocol: str
    status: str


@dataclass(frozen=True)
class DecisionData:
    """Represents a security decision."""

    timestamp: str
    asset: str
    command: str
    decision: str
    reason: str


def get_metrics() -> List[MetricData]:
    """Return mock dashboard metrics."""
    return [
        MetricData(
            "PACKETS INSPECTED",
            "12,482",
            "Last 24 hours",
            "normal",
        ),
        MetricData(
            "ALLOWED",
            "11,932",
            "95.6% of traffic",
            "normal",
        ),
        MetricData(
            "DROPPED",
            "550",
            "4.4% blocked",
            "warning",
        ),
        MetricData(
            "ACTIVE ALERTS",
            "18",
            "3 require attention",
            "critical",
        ),
    ]


def get_alerts() -> List[AlertData]:
    """Return mock security alerts."""
    return [
        AlertData(
            "CRITICAL",
            "PLC-03",
            "Unexpected write command detected",
            "10:42:17",
        ),
        AlertData(
            "HIGH",
            "PUMP-01",
            "Command exceeded configured threshold",
            "10:39:44",
        ),
        AlertData(
            "MEDIUM",
            "RTU-07",
            "Unusual communication frequency",
            "10:35:21",
        ),
    ]


def get_activity() -> List[ActivityData]:
    """Return mock packet activity."""
    return [
        ActivityData(
            "10:42:17",
            "10.10.20.15",
            "10.10.20.31",
            "Modbus/TCP",
            "BLOCKED",
        ),
        ActivityData(
            "10:41:52",
            "10.10.20.12",
            "10.10.20.21",
            "Modbus/TCP",
            "ALLOWED",
        ),
        ActivityData(
            "10:40:31",
            "10.10.20.18",
            "10.10.20.25",
            "Modbus/TCP",
            "ALLOWED",
        ),
        ActivityData(
            "10:39:44",
            "10.10.20.11",
            "10.10.20.31",
            "Modbus/TCP",
            "BLOCKED",
        ),
    ]


def get_decisions() -> List[DecisionData]:
    """Return mock decision engine results."""
    return [
        DecisionData(
            "10:42:17",
            "PLC-03",
            "WRITE_REGISTER",
            "DROP",
            "Unsafe command pattern",
        ),
        DecisionData(
            "10:41:52",
            "PUMP-01",
            "SET_SPEED",
            "ALLOW",
            "Within safe operating range",
        ),
        DecisionData(
            "10:40:31",
            "RTU-07",
            "READ_STATUS",
            "ALLOW",
            "Read-only operation",
        ),
    ]