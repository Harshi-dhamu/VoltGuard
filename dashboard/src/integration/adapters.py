from typing import Any, Dict

from data.integration_event import IntegrationEvent


class PacketInterceptorAdapter:
    """Normalize Packet Interceptor output into VoltGuard events."""

    def normalize(
        self,
        data: Dict[str, Any],
    ) -> IntegrationEvent:
        """Convert packet interceptor data into an IntegrationEvent."""

        return IntegrationEvent.create(
            event_id=(
                f"PKT-"
                f"{data.get('source_ip', 'UNKNOWN')}-"
                f"{data.get('packet_size', 0)}"
            ),
            source_module="packet_interceptor",
            event_type="NETWORK_ANOMALY",
            severity=data.get(
                "severity",
                "HIGH",
            ),
            asset=data.get(
                "asset",
                "Network Segment",
            ),
            message=(
                "Suspicious network traffic detected"
            ),
            payload=data,
        )


class PhysicsEngineAdapter:
    """Normalize Physics Engine output into VoltGuard events."""

    def normalize(
        self,
        data: Dict[str, Any],
    ) -> IntegrationEvent:
        """Convert physics engine data into an IntegrationEvent."""

        anomaly_score = float(
            data.get(
                "anomaly_score",
                0.0,
            )
        )

        severity = (
            "CRITICAL"
            if anomaly_score >= 0.90
            else "HIGH"
            if anomaly_score >= 0.70
            else "MEDIUM"
        )

        return IntegrationEvent.create(
            event_id=(
                f"PHY-"
                f"{data.get('asset', 'UNKNOWN')}-"
                f"{int(anomaly_score * 100)}"
            ),
            source_module="physics_engine",
            event_type="PROCESS_ANOMALY",
            severity=data.get(
                "severity",
                severity,
            ),
            asset=data.get(
                "asset",
                "Unknown Asset",
            ),
            message=(
                "Abnormal process behaviour detected"
            ),
            payload=data,
        )


class DecisionEngineAdapter:
    """Normalize Decision Engine output into VoltGuard events."""

    def normalize(
        self,
        data: Dict[str, Any],
    ) -> IntegrationEvent:
        """Convert decision engine data into an IntegrationEvent."""

        decision = str(
            data.get(
                "decision",
                "UNKNOWN",
            )
        ).upper()

        severity = str(
            data.get(
                "severity",
                "MEDIUM",
            )
        ).upper()

        return IntegrationEvent.create(
            event_id=(
                f"DEC-"
                f"{data.get('asset', 'UNKNOWN')}-"
                f"{decision}"
            ),
            source_module="decision_engine",
            event_type="SECURITY_DECISION",
            severity=severity,
            asset=data.get(
                "asset",
                "Unknown Asset",
            ),
            message=(
                f"Security decision: {decision}"
            ),
            payload=data,
        )


__all__ = [
    "PacketInterceptorAdapter",
    "PhysicsEngineAdapter",
    "DecisionEngineAdapter",
]