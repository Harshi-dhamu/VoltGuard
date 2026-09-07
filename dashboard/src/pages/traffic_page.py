from PyQt6.QtCore import QTimer
from PyQt6.QtWidgets import (
    QFrame,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

from data.traffic_data import MockTrafficProvider

from widgets.traffic_table import TrafficTable

from .base_page import BasePage


class TrafficPage(BasePage):
    """Network traffic monitoring page."""

    def __init__(
        self,
        parent=None,
    ) -> None:
        super().__init__(
            "Traffic Monitor",
            "Industrial network packet inspection and communication activity",
            parent,
        )

        self._provider = (
            MockTrafficProvider()
        )

        self._monitoring = True

        self._total_packets = 0
        self._allowed_packets = 0
        self._blocked_packets = 0

        self._build_content()
        self._load_initial_data()
        self._start_monitoring()

    def _build_content(self) -> None:
        """Build traffic monitoring interface."""

        self._add_monitor_toolbar()
        self._add_statistics()
        self._add_traffic_table()

    def _add_monitor_toolbar(self) -> None:
        """Create monitoring controls."""

        frame = QFrame()
        frame.setObjectName(
            "trafficToolbar"
        )

        layout = QHBoxLayout(frame)

        layout.setContentsMargins(
            14,
            12,
            14,
            12,
        )

        layout.setSpacing(14)

        status = QLabel(
            "●  PACKET MONITORING ACTIVE"
        )

        status.setObjectName(
            "monitoringStatus"
        )

        self._monitor_status = status

        layout.addWidget(status)

        engine = QLabel(
            "Interface: OT-NETWORK"
        )

        engine.setObjectName(
            "monitoringInfo"
        )

        layout.addWidget(engine)

        layout.addStretch()

        self._toggle_button = QPushButton(
            "PAUSE MONITORING"
        )

        self._toggle_button.setObjectName(
            "secondaryButton"
        )

        self._toggle_button.clicked.connect(
            self._toggle_monitoring
        )

        layout.addWidget(
            self._toggle_button
        )

        clear_button = QPushButton(
            "CLEAR"
        )

        clear_button.setObjectName(
            "secondaryButton"
        )

        clear_button.clicked.connect(
            self._clear_traffic
        )

        layout.addWidget(
            clear_button
        )

        self.add_content(frame)

    def _add_statistics(self) -> None:
        """Create traffic statistics."""

        container = QWidget()

        layout = QHBoxLayout(
            container
        )

        layout.setContentsMargins(
            0,
            0,
            0,
            0,
        )

        layout.setSpacing(12)

        self._total_label = self._create_stat_card(
            layout,
            "PACKETS OBSERVED",
        )

        self._allowed_label = self._create_stat_card(
            layout,
            "ALLOWED",
        )

        self._blocked_label = self._create_stat_card(
            layout,
            "BLOCKED",
        )

        self._rate_label = self._create_stat_card(
            layout,
            "MONITORING",
        )

        self.add_content(
            container
        )

    def _create_stat_card(
        self,
        layout: QHBoxLayout,
        title: str,
    ) -> QLabel:
        """Create one traffic statistic card."""

        frame = QFrame()

        frame.setObjectName(
            "trafficStatCard"
        )

        card_layout = QVBoxLayout(
            frame
        )

        card_layout.setContentsMargins(
            16,
            13,
            16,
            13,
        )

        title_label = QLabel(title)

        title_label.setObjectName(
            "trafficStatTitle"
        )

        value_label = QLabel("0")

        value_label.setObjectName(
            "trafficStatValue"
        )

        card_layout.addWidget(
            title_label
        )

        card_layout.addWidget(
            value_label
        )

        layout.addWidget(
            frame,
            1,
        )

        return value_label

    def _add_traffic_table(self) -> None:
        """Create traffic table."""

        frame = QFrame()

        frame.setObjectName(
            "panel"
        )

        layout = QVBoxLayout(frame)

        layout.setContentsMargins(
            14,
            14,
            14,
            14,
        )

        title = QLabel(
            "RECENT NETWORK ACTIVITY"
        )

        title.setObjectName(
            "panelTitle"
        )

        layout.addWidget(title)

        self._table = TrafficTable()

        layout.addWidget(
            self._table,
            1,
        )

        self.add_content(
            frame
        )

    def _load_initial_data(self) -> None:
        """Load initial simulated traffic."""

        packets = (
            self._provider
            .get_initial_packets(12)
        )

        for packet in packets:
            self._record_packet(
                packet,
                update_table=True,
            )

    def _start_monitoring(self) -> None:
        """Start simulated packet monitoring."""

        self._timer = QTimer(self)

        self._timer.setInterval(
            1200
        )

        self._timer.timeout.connect(
            self._receive_packet
        )

        self._timer.start()

    def _receive_packet(self) -> None:
        """Receive a simulated packet."""

        if not self._monitoring:
            return

        packet = (
            self._provider
            .generate_packet()
        )

        self._record_packet(
            packet,
            update_table=True,
        )

    def _record_packet(
        self,
        packet,
        update_table: bool = True,
    ) -> None:
        """Update packet counters and table."""

        self._total_packets += 1

        if packet.status == "BLOCKED":
            self._blocked_packets += 1
        else:
            self._allowed_packets += 1

        if update_table:
            self._table.add_packet(
                packet
            )

        self._update_statistics()

    def _update_statistics(self) -> None:
        """Update traffic statistics."""

        self._total_label.setText(
            f"{self._total_packets:,}"
        )

        self._allowed_label.setText(
            f"{self._allowed_packets:,}"
        )

        self._blocked_label.setText(
            f"{self._blocked_packets:,}"
        )

        status = (
            "ACTIVE"
            if self._monitoring
            else "PAUSED"
        )

        self._rate_label.setText(
            status
        )

    def _toggle_monitoring(self) -> None:
        """Pause or resume monitoring."""

        self._monitoring = (
            not self._monitoring
        )

        if self._monitoring:
            self._timer.start()

            self._toggle_button.setText(
                "PAUSE MONITORING"
            )

            self._monitor_status.setText(
                "●  PACKET MONITORING ACTIVE"
            )

            self._monitor_status.setObjectName(
                "monitoringStatus"
            )

        else:
            self._timer.stop()

            self._toggle_button.setText(
                "RESUME MONITORING"
            )

            self._monitor_status.setText(
                "●  PACKET MONITORING PAUSED"
            )

            self._monitor_status.setObjectName(
                "monitoringPaused"
            )

        self._refresh_style(
            self._monitor_status
        )

        self._update_statistics()

    def _clear_traffic(self) -> None:
        """Clear packet history."""

        self._table.clear_packets()

        self._total_packets = 0
        self._allowed_packets = 0
        self._blocked_packets = 0

        self._update_statistics()

    @staticmethod
    def _refresh_style(
        widget: QWidget,
    ) -> None:
        """Refresh Qt stylesheet properties."""

        widget.style().unpolish(
            widget
        )

        widget.style().polish(
            widget
        )

        widget.update()