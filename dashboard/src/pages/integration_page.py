from PyQt6.QtCore import QTimer
from PyQt6.QtWidgets import (
    QFrame,
    QLabel,
    QPushButton,
    QVBoxLayout,
)

from data.integration_event import IntegrationEvent

from integration.adapters import (
    DecisionEngineAdapter,
    PacketInterceptorAdapter,
    PhysicsEngineAdapter,
)

from widgets.integration_status import IntegrationStatusPanel

from .base_page import BasePage


class IntegrationPage(BasePage):
    """VoltGuard module integration monitor."""

    def __init__(
        self,
        event_bus,
        integration_manager,
        parent=None,
    ) -> None:
        super().__init__(
            "System Integration",
            "Runtime connectivity and module communication",
            parent,
        )

        # Shared services supplied by ApplicationContext.
        self._event_bus = event_bus
        self._integration_manager = integration_manager

        # Module adapters.
        self._packet_adapter = (
            PacketInterceptorAdapter()
        )

        self._physics_adapter = (
            PhysicsEngineAdapter()
        )

        self._decision_adapter = (
            DecisionEngineAdapter()
        )

        self._event_count = 0

        self._build_content()
        self._start_demo_timer()

    def _build_content(self) -> None:
        """Build integration interface."""

        self._add_status_section()
        self._add_runtime_section()

    def _add_status_section(self) -> None:
        """Add module status cards."""

        title = QLabel(
            "MODULE CONNECTIVITY"
        )

        title.setObjectName(
            "panelTitle"
        )

        self.add_content(
            title
        )

        self._status_panel = (
            IntegrationStatusPanel()
        )

        self.add_content(
            self._status_panel
        )

        # Show the current integration state immediately.
        self._refresh_status()

    def _add_runtime_section(self) -> None:
        """Add runtime integration panel."""

        frame = QFrame()

        frame.setObjectName(
            "panel"
        )

        layout = QVBoxLayout(
            frame
        )

        layout.setContentsMargins(
            16,
            16,
            16,
            16,
        )

        title = QLabel(
            "INTEGRATION RUNTIME"
        )

        title.setObjectName(
            "panelTitle"
        )

        layout.addWidget(
            title
        )

        self._runtime_status = QLabel(
            "Integration bus initialized."
        )

        self._runtime_status.setObjectName(
            "alertDetailInfo"
        )

        self._runtime_status.setWordWrap(
            True
        )

        layout.addWidget(
            self._runtime_status
        )

        self._event_counter = QLabel(
            "Events processed: 0"
        )

        self._event_counter.setObjectName(
            "trafficStatValue"
        )

        layout.addWidget(
            self._event_counter
        )

        simulate_button = QPushButton(
            "SIMULATE MODULE EVENT"
        )

        simulate_button.setObjectName(
            "secondaryButton"
        )

        simulate_button.clicked.connect(
            self._simulate_event
        )

        layout.addWidget(
            simulate_button
        )

        self.add_content(
            frame
        )

    def _start_demo_timer(self) -> None:
        """Start development-only event simulation."""

        self._timer = QTimer(
            self
        )

        self._timer.timeout.connect(
            self._simulate_event
        )

        self._timer.start(
            8000
        )

    def _simulate_event(self) -> None:
        """Generate a development integration event."""

        self._event_count += 1

        event_number = (
            self._event_count % 3
        )

        if event_number == 1:
            event = self._packet_adapter.normalize(
                {
                    "source_ip": "10.10.20.99",
                    "destination_ip": "10.10.20.10",
                    "protocol": "MODBUS",
                    "packet_size": 128,
                }
            )

        elif event_number == 2:
            event = self._physics_adapter.normalize(
                {
                    "asset": "Main Process PLC",
                    "anomaly_score": 0.91,
                    "category": "COMMAND ANOMALY",
                }
            )

        else:
            event = self._decision_adapter.normalize(
                {
                    "decision": "BLOCK",
                    "severity": "HIGH",
                    "confidence": 93,
                    "asset": "Main Process PLC",
                }
            )

        # Send the normalized event through the
        # shared EventBus.
        self._integration_manager.receive_event(
            event
        )

        self._update_interface(
            event
        )

    def _refresh_status(self) -> None:
        """Refresh module connectivity status."""

        if self._integration_manager is None:
            return

        self._status_panel.update_status(
            self._integration_manager.get_status()
        )

    def _update_interface(
        self,
        event: IntegrationEvent,
    ) -> None:
        """Refresh runtime information."""

        self._refresh_status()

        self._event_counter.setText(
            f"Events processed: "
            f"{self._event_count}"
        )

        self._runtime_status.setText(
            f"Last event: "
            f"{event.event_type.upper()} "
            f"from {event.source_module} "
            f"at {event.timestamp}"
        )