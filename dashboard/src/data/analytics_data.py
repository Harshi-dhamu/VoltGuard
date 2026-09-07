from dataclasses import dataclass
from typing import List


@dataclass
class AnalyticsMetric:
    """Security analytics metric."""

    name: str
    value: str
    description: str


@dataclass
class ThreatBucket:
    """Threat distribution bucket."""

    label: str
    count: int


@dataclass
class ThreatTimelinePoint:
    """Threat activity at a specific time."""

    timestamp: str
    events: int
    critical: int
    blocked: int


@dataclass
class AssetThreat:
    """Threat activity associated with an OT asset."""

    asset: str
    incidents: int
    severity: str


def get_metrics() -> List[AnalyticsMetric]:
    """Return dashboard analytics metrics."""

    return [
        AnalyticsMetric(
            "EVENTS ANALYZED",
            "18,642",
            "Last 24 hours",
        ),
        AnalyticsMetric(
            "THREATS DETECTED",
            "74",
            "Across monitored assets",
        ),
        AnalyticsMetric(
            "BLOCKED EVENTS",
            "51",
            "Preventive actions applied",
        ),
        AnalyticsMetric(
            "DETECTION RATE",
            "94.6%",
            "Correlation confidence",
        ),
    ]


def get_threat_distribution() -> List[ThreatBucket]:
    """Return threat severity distribution."""

    return [
        ThreatBucket(
            "CRITICAL",
            8,
        ),
        ThreatBucket(
            "HIGH",
            21,
        ),
        ThreatBucket(
            "MEDIUM",
            29,
        ),
        ThreatBucket(
            "LOW",
            16,
        ),
    ]


def get_timeline() -> List[ThreatTimelinePoint]:
    """Return recent threat activity."""

    return [
        ThreatTimelinePoint(
            "06:00",
            24,
            1,
            17,
        ),
        ThreatTimelinePoint(
            "08:00",
            31,
            0,
            21,
        ),
        ThreatTimelinePoint(
            "10:00",
            48,
            2,
            35,
        ),
        ThreatTimelinePoint(
            "12:00",
            37,
            1,
            29,
        ),
        ThreatTimelinePoint(
            "14:00",
            62,
            3,
            46,
        ),
        ThreatTimelinePoint(
            "16:00",
            51,
            1,
            39,
        ),
        ThreatTimelinePoint(
            "18:00",
            43,
            0,
            32,
        ),
    ]


def get_asset_threats() -> List[AssetThreat]:
    """Return the most affected OT assets."""

    return [
        AssetThreat(
            "PLC-03",
            18,
            "CRITICAL",
        ),
        AssetThreat(
            "PUMP-01",
            14,
            "HIGH",
        ),
        AssetThreat(
            "RTU-07",
            11,
            "HIGH",
        ),
        AssetThreat(
            "HMI-02",
            8,
            "MEDIUM",
        ),
        AssetThreat(
            "SENSOR-11",
            5,
            "LOW",
        ),
    ]