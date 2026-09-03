from dataclasses import dataclass
from typing import List


@dataclass(frozen=True)
class AlertData:
    """Represents a VoltGuard security alert."""

    alert_id: str
    timestamp: str
    title: str
    severity: str
    status: str
    asset: str
    asset_ip: str
    source_ip: str
    protocol: str
    category: str
    description: str
    detection_reason: str
    recommended_action: str


class MockAlertProvider:
    """Temporary alert provider for dashboard development."""

    def get_alerts(self) -> List[AlertData]:
        """Return simulated security alerts."""

        return [
            AlertData(
                alert_id="VG-0001",
                timestamp="21:41:32",
                title="Unauthorized PLC Write",
                severity="CRITICAL",
                status="OPEN",
                asset="Main Process PLC",
                asset_ip="10.10.20.11",
                source_ip="10.10.20.99",
                protocol="Modbus/TCP",
                category="COMMAND INJECTION",
                description=(
                    "A write operation was detected "
                    "from an unrecognized source."
                ),
                detection_reason=(
                    "Source address is outside the "
                    "approved control network."
                ),
                recommended_action=(
                    "Block source and investigate "
                    "the originating workstation."
                ),
            ),
            AlertData(
                alert_id="VG-0002",
                timestamp="21:39:18",
                title="Repeated Modbus Requests",
                severity="HIGH",
                status="OPEN",
                asset="Packaging PLC",
                asset_ip="10.10.20.12",
                source_ip="10.10.20.80",
                protocol="Modbus/TCP",
                category="ANOMALOUS TRAFFIC",
                description=(
                    "Unusual frequency of Modbus "
                    "requests was observed."
                ),
                detection_reason=(
                    "Request rate exceeded the "
                    "established baseline."
                ),
                recommended_action=(
                    "Inspect the source host and "
                    "compare against normal traffic."
                ),
            ),
            AlertData(
                alert_id="VG-0003",
                timestamp="21:35:07",
                title="Engineering Host Communication",
                severity="MEDIUM",
                status="INVESTIGATING",
                asset="Engineering Workstation",
                asset_ip="10.10.20.30",
                source_ip="10.10.20.30",
                protocol="TCP",
                category="POLICY VIOLATION",
                description=(
                    "Engineering workstation contacted "
                    "a field-zone device."
                ),
                detection_reason=(
                    "Communication crossed a restricted "
                    "network boundary."
                ),
                recommended_action=(
                    "Verify whether the connection "
                    "was authorized."
                ),
            ),
            AlertData(
                alert_id="VG-0004",
                timestamp="21:31:55",
                title="Sensor Communication Lost",
                severity="LOW",
                status="ACKNOWLEDGED",
                asset="Pressure Sensor",
                asset_ip="10.10.20.42",
                source_ip="10.10.20.42",
                protocol="UDP",
                category="AVAILABILITY",
                description=(
                    "The monitored sensor stopped "
                    "responding to network requests."
                ),
                detection_reason=(
                    "No communication received within "
                    "the expected interval."
                ),
                recommended_action=(
                    "Check sensor availability and "
                    "physical connectivity."
                ),
            ),
            AlertData(
                alert_id="VG-0005",
                timestamp="21:28:42",
                title="Unexpected DNP3 Command",
                severity="HIGH",
                status="OPEN",
                asset="Water Treatment RTU",
                asset_ip="10.10.20.50",
                source_ip="10.10.20.70",
                protocol="DNP3",
                category="COMMAND ANOMALY",
                description=(
                    "An unexpected control command "
                    "was observed on a field RTU."
                ),
                detection_reason=(
                    "Command does not match the "
                    "configured operational profile."
                ),
                recommended_action=(
                    "Investigate the command source "
                    "and validate the RTU state."
                ),
            ),
            AlertData(
                alert_id="VG-0006",
                timestamp="21:22:10",
                title="New Network Device Detected",
                severity="MEDIUM",
                status="ACKNOWLEDGED",
                asset="Unknown Device",
                asset_ip="10.10.20.77",
                source_ip="10.10.20.77",
                protocol="TCP",
                category="ASSET DISCOVERY",
                description=(
                    "A previously unknown device "
                    "appeared on the control network."
                ),
                detection_reason=(
                    "Device was not present in the "
                    "known asset inventory."
                ),
                recommended_action=(
                    "Identify the device and verify "
                    "whether it is authorized."
                ),
            ),
        ]