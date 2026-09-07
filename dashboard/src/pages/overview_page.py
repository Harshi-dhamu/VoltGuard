from PyQt6.QtWidgets import (
    QFrame,
    QHBoxLayout,
    QLabel,
    QVBoxLayout,
    QWidget,
)

from data.mock_data import (
    get_activity,
    get_alerts,
    get_decisions,
    get_metrics,
)

from widgets.activity_panel import ActivityPanel
from widgets.alert_panel import AlertPanel
from widgets.decision_panel import DecisionPanel
from widgets.metric_card import MetricCard

from .base_page import BasePage


class OverviewPage(BasePage):
    """Main VoltGuard security overview."""

    def __init__(self, parent=None) -> None:
        super().__init__(
            "Security Overview",
            "Real-time operational technology security monitoring",
            parent,
        )

        self._build_content()

    def _build_content(self) -> None:
        """Build the overview page."""
        self._add_environment_status()
        self._add_metrics()
        self._add_activity()
        self._add_alerts_and_decisions()

        self.add_stretch()

    def _add_environment_status(self) -> None:
        """Add the protection status bar."""
        frame = QFrame()
        frame.setObjectName("systemBar")

        layout = QHBoxLayout(frame)
        layout.setContentsMargins(
            14,
            10,
            14,
            10,
        )

        status = QLabel(
            "●  PROTECTION ACTIVE"
        )
        status.setObjectName(
            "protectionStatus"
        )

        engine = QLabel(
            "Packet inspection operational"
        )
        engine.setObjectName("systemInfo")

        heartbeat = QLabel(
            "Last heartbeat: 10:42:19"
        )
        heartbeat.setObjectName(
            "heartbeat"
        )

        layout.addWidget(status)
        layout.addWidget(engine)
        layout.addStretch()
        layout.addWidget(heartbeat)

        self.add_content(frame)

    def _add_metrics(self) -> None:
        """Add security metric cards."""
        container = QFrame()
        container.setObjectName(
            "transparentContainer"
        )

        layout = QHBoxLayout(container)
        layout.setContentsMargins(
            0,
            0,
            0,
            0,
        )
        layout.setSpacing(12)

        for metric in get_metrics():
            card = MetricCard(
                metric.label,
                metric.value,
                metric.description,
                metric.status,
            )

            layout.addWidget(card)

        self.add_content(container)

    def _add_activity(self) -> None:
        """Add network activity panel."""
        activity_panel = ActivityPanel(
            get_activity()
        )

        self.add_content(
            activity_panel
        )

    def _add_alerts_and_decisions(self) -> None:
        """Add alerts and decision engine panels."""
        wrapper = QWidget()

        container = QHBoxLayout(wrapper)
        container.setContentsMargins(
            0,
            0,
            0,
            0,
        )

        container.setSpacing(16)

        alerts = AlertPanel(
            get_alerts()
        )

        decisions = DecisionPanel(
            get_decisions()
        )

        container.addWidget(
            alerts,
            1,
        )

        container.addWidget(
            decisions,
            1,
        )

        self.add_content(wrapper)