from dataclasses import dataclass
from typing import List


@dataclass
class SecurityPolicy:
    """Represents a VoltGuard security policy."""

    policy_id: str
    name: str
    module: str
    condition: str
    severity: str
    action: str
    enabled: bool
    last_updated: str


def get_security_policies() -> List[SecurityPolicy]:
    """Return the current dashboard policy set."""

    return [
        SecurityPolicy(
            policy_id="VG-POL-001",
            name="Unauthorized PLC Write",
            module="Packet Interceptor",
            condition="WRITE_REGISTER from untrusted source",
            severity="CRITICAL",
            action="BLOCK",
            enabled=True,
            last_updated="Today 10:42",
        ),
        SecurityPolicy(
            policy_id="VG-POL-002",
            name="Excessive Command Rate",
            module="Physics Engine",
            condition="Command rate > 100/min",
            severity="HIGH",
            action="ALERT",
            enabled=True,
            last_updated="Today 10:31",
        ),
        SecurityPolicy(
            policy_id="VG-POL-003",
            name="Unknown Modbus Source",
            module="Packet Interceptor",
            condition="Source not present in trusted zone",
            severity="HIGH",
            action="BLOCK",
            enabled=True,
            last_updated="Today 10:18",
        ),
        SecurityPolicy(
            policy_id="VG-POL-004",
            name="Abnormal Motor Speed",
            module="Physics Engine",
            condition="RPM exceeds configured threshold",
            severity="MEDIUM",
            action="ALERT",
            enabled=True,
            last_updated="Today 09:54",
        ),
        SecurityPolicy(
            policy_id="VG-POL-005",
            name="Trusted HMI Communication",
            module="Decision Engine",
            condition="Approved HMI to PLC communication",
            severity="LOW",
            action="ALLOW",
            enabled=True,
            last_updated="Today 09:32",
        ),
        SecurityPolicy(
            policy_id="VG-POL-006",
            name="Repeated Authentication Failure",
            module="Decision Engine",
            condition="More than 5 failures in 60 seconds",
            severity="HIGH",
            action="BLOCK",
            enabled=True,
            last_updated="Today 08:47",
        ),
        SecurityPolicy(
            policy_id="VG-POL-007",
            name="Unexpected Protocol",
            module="Packet Interceptor",
            condition="Protocol not allowed for asset",
            severity="CRITICAL",
            action="BLOCK",
            enabled=True,
            last_updated="Yesterday 18:24",
        ),
        SecurityPolicy(
            policy_id="VG-POL-008",
            name="Low Risk Telemetry Drift",
            module="Physics Engine",
            condition="Telemetry deviation > 10%",
            severity="LOW",
            action="MONITOR",
            enabled=False,
            last_updated="Yesterday 16:11",
        ),
    ]