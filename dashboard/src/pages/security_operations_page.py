from PyQt6.QtCore import Qt

from PyQt6.QtWidgets import (
    QFrame,
    QGridLayout,
    QHBoxLayout,
    QLabel,
    QVBoxLayout,
)

from data.integration_event import IntegrationEvent
from data.security_metrics import SecurityMetrics

from integration.event_bus import EventBus

from widgets.security_activity_panel import (
    SecurityActivityPanel,
)

from widgets.security_metric_card import (
    SecurityMetricCard,
)

from .base_page import BasePage


class SecurityOperationsPage(BasePage):
    """Central security operations dashboard."""

    def __init__(
        self,
        event_bus: EventBus,
        parent=None,
    ) -> None:
        super().__init__(
            "Security Operations",
            "Centralized VoltGuard security intelligence and module activity",
            parent,
        )

        self._event_bus = event_bus

        self._metrics = SecurityMetrics()

        self._build_content()

        self._event_bus.subscribe(
            self._handle_event
        )

    def _build_content(self) -> None:
        """Build the security operations dashboard."""

        self._add_status_banner()

        self._add_metric_cards()

        self._add_activity_panel()

    def _add_status_banner(self) -> None:
        """Add operational status banner."""

        frame = QFrame()

        frame.setObjectName(
            "securityOperationsBanner"
        )

        layout = QHBoxLayout(
            frame
        )

        layout.setContentsMargins(
            16,
            12,
            16,
            12,
        )

        status = QLabel(
            "● SECURITY OPERATIONS ACTIVE"
        )

        status.setObjectName(
            "integrationOnline"
        )

        layout.addWidget(
            status
        )

        layout.addStretch()

        description = QLabel(
            "Monitoring network, process and decision telemetry"
        )

        description.setObjectName(
            "alertDetailInfo"
        )

        layout.addWidget(
            description
        )

        self.add_content(
            frame
        )

    def _add_metric_cards(self) -> None:
        """Create security metric cards."""

        title = QLabel(
            "SECURITY POSTURE"
        )

        title.setObjectName(
            "panelTitle"
        )

        self.add_content(
            title
        )

        grid_frame = QFrame()

        grid_frame.setObjectName(
            "metricsContainer"
        )

        grid = QGridLayout(
            grid_frame
        )

        grid.setContentsMargins(
            0,
            0,
            0,
            0,
        )

        grid.setHorizontalSpacing(
            10
        )

        grid.setVerticalSpacing(
            10
        )

        self._total_card = SecurityMetricCard(
            "Total Events",
            "0",
            "All integration events received",
        )

        self._network_card = SecurityMetricCard(
            "Network Anomalies",
            "0",
            "Packet interceptor findings",
        )

        self._process_card = SecurityMetricCard(
            "Process Anomalies",
            "0",
            "Physics engine findings",
        )

        self._decision_card = SecurityMetricCard(
            "Security Decisions",
            "0",
            "Decision engine actions",
        )

        self._critical_card = SecurityMetricCard(
            "Critical Events",
            "0",
            "Events requiring immediate attention",
        )

        self._blocked_card = SecurityMetricCard(
            "Blocked Operations",
            "0",
            "Operations blocked by policy",
        )

        grid.addWidget(
            self._total_card,
            0,
            0,
        )

        grid.addWidget(
            self._network_card,
            0,
            1,
        )

        grid.addWidget(
            self._process_card,
            0,
            2,
        )

        grid.addWidget(
            self._decision_card,
            1,
            0,
        )

        grid.addWidget(
            self._critical_card,
            1,
            1,
        )

        grid.addWidget(
            self._blocked_card,
            1,
            2,
        )

        self.add_content(
            grid_frame
        )

    def _add_activity_panel(self) -> None:
        """Add recent activity panel."""

        self._activity_panel = (
            SecurityActivityPanel()
        )

        self.add_content(
            self._activity_panel
        )

    def _handle_event(
        self,
        event: IntegrationEvent,
    ) -> None:
        """Process an incoming security event."""

        if not isinstance(
            event,
            IntegrationEvent,
        ):
            return

        decision = ""

        if isinstance(
            event.payload,
            dict,
        ):
            decision = str(
                event.payload.get(
                    "decision",
                    "",
                )
            )

        self._metrics.process_event(
            event_type=event.event_type,
            severity=event.severity,
            decision=decision,
        )

        self._update_metrics()

        self._activity_panel.add_event(
            event
        )

    def _update_metrics(self) -> None:
        """Refresh metric card values."""

        metrics = self._metrics

        self._total_card.set_value(
            str(metrics.total_events)
        )

        self._network_card.set_value(
            str(metrics.network_events)
        )

        self._process_card.set_value(
            str(metrics.process_anomalies)
        )

        self._decision_card.set_value(
            str(metrics.security_decisions)
        )

        self._critical_card.set_value(
            str(metrics.critical_events)
        )

        self._blocked_card.set_value(
            str(metrics.blocked_decisions)
        )