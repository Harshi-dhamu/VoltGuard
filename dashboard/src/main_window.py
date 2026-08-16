from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QFrame,
    QGridLayout,
    QHBoxLayout,
    QLabel,
    QMainWindow,
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
from widgets.sidebar import Sidebar


class MainWindow(QMainWindow):
    """Main VoltGuard security dashboard."""

    def __init__(self) -> None:
        super().__init__()

        self.setWindowTitle("VoltGuard | OT Security Platform")
        self.setMinimumSize(1280, 780)

        self._build_ui()

    def _build_ui(self) -> None:
        central = QWidget()
        central.setObjectName("mainContainer")

        root_layout = QHBoxLayout(central)
        root_layout.setContentsMargins(0, 0, 0, 0)
        root_layout.setSpacing(0)

        sidebar = Sidebar()
        sidebar.navigation_requested.connect(
            self._handle_navigation
        )

        root_layout.addWidget(sidebar)
        root_layout.addWidget(self._build_content(), 1)

        self.setCentralWidget(central)

    def _build_content(self) -> QWidget:
        content = QWidget()

        layout = QVBoxLayout(content)
        layout.setContentsMargins(26, 22, 26, 22)
        layout.setSpacing(18)

        layout.addWidget(self._build_header())
        layout.addWidget(self._build_status_bar())
        layout.addWidget(self._build_metrics())

        middle = QGridLayout()
        middle.setHorizontalSpacing(16)
        middle.setVerticalSpacing(16)

        activity = ActivityPanel(get_activity())
        alerts = AlertPanel(get_alerts())
        decisions = DecisionPanel(get_decisions())

        middle.addWidget(activity, 0, 0, 1, 2)
        middle.addWidget(alerts, 1, 0)
        middle.addWidget(decisions, 1, 1)

        layout.addLayout(middle, 1)

        return content

    def _build_header(self) -> QWidget:
        header = QWidget()

        layout = QHBoxLayout(header)
        layout.setContentsMargins(0, 0, 0, 0)

        title_container = QVBoxLayout()
        title_container.setSpacing(2)

        title = QLabel("Security Overview")
        title.setObjectName("pageTitle")

        subtitle = QLabel(
            "Real-time operational technology security monitoring"
        )
        subtitle.setObjectName("pageSubtitle")

        title_container.addWidget(title)
        title_container.addWidget(subtitle)

        layout.addLayout(title_container)
        layout.addStretch()

        environment = QLabel("PRODUCTION ENVIRONMENT")
        environment.setObjectName("environmentBadge")

        layout.addWidget(environment)

        return header

    def _build_status_bar(self) -> QWidget:
        frame = QFrame()
        frame.setObjectName("systemBar")

        layout = QHBoxLayout(frame)
        layout.setContentsMargins(14, 10, 14, 10)

        status = QLabel("●  PROTECTION ACTIVE")
        status.setObjectName("protectionStatus")

        separator = QLabel("|")
        separator.setObjectName("systemSeparator")

        engine = QLabel("Packet inspection operational")
        engine.setObjectName("systemInfo")

        layout.addWidget(status)
        layout.addWidget(separator)
        layout.addWidget(engine)
        layout.addStretch()

        heartbeat = QLabel("Last heartbeat: 10:42:19")
        heartbeat.setObjectName("heartbeat")

        layout.addWidget(heartbeat)

        return frame

    def _build_metrics(self) -> QWidget:
        container = QWidget()

        layout = QHBoxLayout(container)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(12)

        for metric in get_metrics():
            card = MetricCard(
                metric.label,
                metric.value,
                metric.description,
                metric.status,
            )

            layout.addWidget(card, 1)

        return container

    def _handle_navigation(self, destination: str) -> None:
        """Handle sidebar navigation requests."""
        # Full page navigation will be implemented in later days.
        print(f"Navigation requested: {destination}")