from PyQt6.QtCore import QTimer
from PyQt6.QtWidgets import (
    QFrame,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QVBoxLayout,
)

from data.integration_event import IntegrationEvent

from widgets.live_integration_panel import (
    LiveIntegrationPanel,
)

from .base_page import BasePage


class LiveIntegrationPage(BasePage):
    """Live monitoring page for VoltGuard module integration."""

    def __init__(
        self,
        integration_manager,
        parent=None,
    ) -> None:
        super().__init__(
            "Live Module Integration",
            "Real-time communication status between VoltGuard modules",
            parent,
        )

        self._manager = integration_manager
        self._event_number = 0

        self._build_content()

        # Subscribe to the shared integration event bus.
        self._manager.event_bus.subscribe(
            self._handle_event
        )

        # Development timer.
        self._timer = QTimer(self)

        self._timer.timeout.connect(
            self._simulate_integration_event
        )

        self._timer.start(7000)

    def _build_content(self) -> None:
        """Build the live integration dashboard."""

        self._add_control_bar()
        self._add_module_panel()
        self._add_runtime_panel()

    def _add_control_bar(self) -> None:
        """Create the integration control bar."""

        frame = QFrame()
        frame.setObjectName("panel")

        layout = QHBoxLayout(frame)

        layout.setContentsMargins(
            14,
            10,
            14,
            10,
        )

        layout.setSpacing(12)

        title = QLabel(
            "LIVE INTEGRATION"
        )

        title.setObjectName(
            "panelTitle"
        )

        layout.addWidget(title)

        layout.addStretch()

        self._event_counter = QLabel(
            "Events: 0"
        )

        self._event_counter.setObjectName(
            "trafficStatValue"
        )

        layout.addWidget(
            self._event_counter
        )

        simulate_button = QPushButton(
            "SIMULATE EVENT"
        )

        simulate_button.setObjectName(
            "secondaryButton"
        )

        simulate_button.clicked.connect(
            self._simulate_integration_event
        )

        layout.addWidget(
            simulate_button
        )

        self.add_content(frame)

    def _add_module_panel(self) -> None:
        """Create the module connectivity panel."""

        title = QLabel(
            "MODULE CONNECTIVITY"
        )

        title.setObjectName(
            "panelTitle"
        )

        self.add_content(title)

        self._module_panel = LiveIntegrationPanel()

        self.add_content(
            self._module_panel
        )

    def _add_runtime_panel(self) -> None:
        """Create the latest event information panel."""

        frame = QFrame()
        frame.setObjectName("panel")

        layout = QVBoxLayout(frame)

        layout.setContentsMargins(
            16,
            16,
            16,
            16,
        )

        layout.setSpacing(10)

        title = QLabel(
            "LATEST INTEGRATION EVENT"
        )

        title.setObjectName(
            "panelTitle"
        )

        layout.addWidget(title)

        self._latest_event = QLabel(
            "Waiting for module events..."
        )

        self._latest_event.setObjectName(
            "alertDetailInfo"
        )

        self._latest_event.setWordWrap(
            True
        )

        layout.addWidget(
            self._latest_event
        )

        self.add_content(frame)

    def _simulate_integration_event(
        self,
    ) -> None:
        """Generate a development integration event."""

        self._event_number += 1

        cycle = self._event_number % 3

        if cycle == 1:

            event = IntegrationEvent.create(
                event_id=(
                    f"PKT-{self._event_number:04d}"
                ),
                source_module=(
                    "packet_interceptor"
                ),
                event_type=(
                    "NETWORK_ANOMALY"
                ),
                severity="HIGH",
                asset="PLC-01",
                message=(
                    "Suspicious Modbus traffic detected"
                ),
                payload={
                    "protocol": "MODBUS",
                    "source_ip": "10.10.20.99",
                    "destination_ip": "10.10.20.10",
                    "packet_size": 128,
                },
            )

        elif cycle == 2:

            event = IntegrationEvent.create(
                event_id=(
                    f"PHY-{self._event_number:04d}"
                ),
                source_module=(
                    "physics_engine"
                ),
                event_type=(
                    "PROCESS_ANOMALY"
                ),
                severity="CRITICAL",
                asset="MAIN-PLC",
                message=(
                    "Abnormal process behaviour detected"
                ),
                payload={
                    "anomaly_score": 0.94,
                    "category": "COMMAND ANOMALY",
                },
            )

        else:

            event = IntegrationEvent.create(
                event_id=(
                    f"DEC-{self._event_number:04d}"
                ),
                source_module=(
                    "decision_engine"
                ),
                event_type=(
                    "SECURITY_DECISION"
                ),
                severity="HIGH",
                asset="MAIN-PLC",
                message=(
                    "Decision engine blocked suspicious operation"
                ),
                payload={
                    "decision": "BLOCK",
                    "confidence": 95,
                    "reason": "Policy violation",
                },
            )

        self._manager.receive_event(event)

    def _handle_event(
        self,
        event: IntegrationEvent,
    ) -> None:
        """Update the page when an integration event arrives."""

        status = self._manager.get_status()

        total_events = status.get(
            "total_events",
            0,
        )

        self._event_counter.setText(
            f"Events: {total_events}"
        )

        self._latest_event.setText(
            f"Event ID: {event.event_id}\n"
            f"Source: {event.source_module}\n"
            f"Type: {event.event_type}\n"
            f"Severity: {event.severity}\n"
            f"Asset: {event.asset}\n"
            f"Message: {event.message}\n"
            f"Timestamp: {event.timestamp}"
        )

        self._module_panel.update_modules(
            self._manager.registry.get_statuses()
        )