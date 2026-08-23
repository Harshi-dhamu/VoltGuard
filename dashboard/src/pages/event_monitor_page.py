from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QFrame,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

from data.event_log import EventLog

from data.integration_data import (
    IntegrationEvent,
)

from integration.event_bus import EventBus

from widgets.event_monitor import (
    EventMonitor,
)

from .base_page import BasePage


class EventMonitorPage(BasePage):
    """Real-time VoltGuard security event monitor."""

    def __init__(
        self,
        event_bus: EventBus,
        parent=None,
    ) -> None:
        super().__init__(
            "Live Event Monitor",
            "Real-time security telemetry from VoltGuard modules",
            parent,
        )

        self._event_bus = event_bus

        self._event_log = EventLog()

        self._build_content()

        self._register_event_handlers()

    def _build_content(self) -> None:
        """Build event monitor interface."""

        self._add_status_bar()
        self._add_event_table()

    def _add_status_bar(self) -> None:
        """Create runtime status bar."""

        frame = QFrame()

        frame.setObjectName(
            "trafficToolbar"
        )

        layout = QHBoxLayout(
            frame
        )

        layout.setContentsMargins(
            14,
            10,
            14,
            10,
        )

        layout.setSpacing(
            14
        )

        self._status = QLabel(
            "● LIVE"
        )

        self._status.setObjectName(
            "integrationOnline"
        )

        layout.addWidget(
            self._status
        )

        self._event_count = QLabel(
            "Events: 0"
        )

        self._event_count.setObjectName(
            "trafficStatTitle"
        )

        layout.addWidget(
            self._event_count
        )

        layout.addStretch()

        clear_button = QPushButton(
            "CLEAR EVENTS"
        )

        clear_button.setObjectName(
            "secondaryButton"
        )

        clear_button.clicked.connect(
            self._clear_events
        )

        layout.addWidget(
            clear_button
        )

        self.add_content(
            frame
        )

    def _add_event_table(self) -> None:
        """Create event monitor table."""

        frame = QFrame()

        frame.setObjectName(
            "panel"
        )

        layout = QVBoxLayout(
            frame
        )

        layout.setContentsMargins(
            14,
            14,
            14,
            14,
        )

        title = QLabel(
            "SECURITY TELEMETRY"
        )

        title.setObjectName(
            "panelTitle"
        )

        layout.addWidget(
            title
        )

        self._table = EventMonitor()

        layout.addWidget(
            self._table
        )

        self.add_content(
            frame
        )

    def _register_event_handlers(self) -> None:
        """Subscribe to all integration events."""

        self._event_bus.subscribe(
            "packet",
            self._handle_event,
        )

        self._event_bus.subscribe(
            "threat",
            self._handle_event,
        )

        self._event_bus.subscribe(
            "decision",
            self._handle_event,
        )

    def _handle_event(
        self,
        event: IntegrationEvent,
    ) -> None:
        """Process an incoming event."""

        entry = (
            self._event_log.add_event(
                event
            )
        )

        self._table.insertRow(
            0
        )

        self._table.add_event_at_row(
            entry,
            0,
        )

        self._event_count.setText(
            f"Events: "
            f"{self._event_log.count()}"
        )

    def _clear_events(self) -> None:
        """Clear event history."""

        self._event_log.clear()

        self._table.setRowCount(
            0
        )

        self._event_count.setText(
            "Events: 0"
        )