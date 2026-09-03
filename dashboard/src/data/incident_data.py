from dataclasses import dataclass
from typing import List


@dataclass
class Incident:
    """Represents a correlated VoltGuard security incident."""

    incident_id: str
    title: str
    severity: str
    status: str
    asset: str
    source_module: str
    category: str
    detected_at: str
    description: str
    recommendation: str


def get_demo_incidents() -> List[Incident]:
    """Return development incident data."""

    return [
        Incident(
            incident_id="VG-INC-0042",
            title="Unauthorized PLC Write Command",
            severity="CRITICAL",
            status="OPEN",
            asset="PLC-03",
            source_module="Decision Engine",
            category="COMMAND ANOMALY",
            detected_at="10:42:17",
            description=(
                "A write operation was detected on PLC-03 "
                "outside the expected operational pattern."
            ),
            recommendation=(
                "Block the command, isolate the affected asset, "
                "and review the originating traffic."
            ),
        ),
        Incident(
            incident_id="VG-INC-0041",
            title="Abnormal Modbus Communication",
            severity="HIGH",
            status="INVESTIGATING",
            asset="PUMP-01",
            source_module="Packet Interceptor",
            category="NETWORK ANOMALY",
            detected_at="10:39:44",
            description=(
                "Repeated Modbus communication exceeded the "
                "configured frequency threshold."
            ),
            recommendation=(
                "Inspect the source endpoint and compare "
                "communication frequency with the baseline."
            ),
        ),
        Incident(
            incident_id="VG-INC-0040",
            title="Unexpected Process Behaviour",
            severity="HIGH",
            status="OPEN",
            asset="RTU-07",
            source_module="Physics Engine",
            category="PHYSICAL ANOMALY",
            detected_at="10:35:21",
            description=(
                "Process telemetry deviated significantly "
                "from the established operational baseline."
            ),
            recommendation=(
                "Inspect process telemetry and verify "
                "whether the deviation is operator initiated."
            ),
        ),
        Incident(
            incident_id="VG-INC-0039",
            title="Repeated Authentication Failure",
            severity="MEDIUM",
            status="ACKNOWLEDGED",
            asset="HMI-02",
            source_module="Packet Interceptor",
            category="ACCESS ANOMALY",
            detected_at="10:28:13",
            description=(
                "Multiple unsuccessful authentication attempts "
                "were observed against HMI-02."
            ),
            recommendation=(
                "Verify the account activity and review "
                "authentication logs."
            ),
        ),
        Incident(
            incident_id="VG-INC-0038",
            title="Unexpected Sensor Variation",
            severity="LOW",
            status="RESOLVED",
            asset="SENSOR-11",
            source_module="Physics Engine",
            category="TELEMETRY ANOMALY",
            detected_at="10:19:05",
            description=(
                "A short-duration sensor deviation was detected "
                "and returned to the expected operating range."
            ),
            recommendation=(
                "Continue monitoring the sensor and verify "
                "the next operational cycle."
            ),
        ),
    ]