from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QComboBox,
    QFrame,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

from data.alert_data import (
    AlertData,
    MockAlertProvider,
)

from widgets.alert_table import AlertTable

from .base_page import BasePage


class AlertsPage(BasePage):
    """Security alert and incident center."""

    def __init__(
        self,
        parent=None,
    ) -> None:
        super().__init__(
            "Security Alerts",
            "Security events, anomalies and incident investigation",
            parent,
        )

        self._provider = (
            MockAlertProvider()
        )

        self._all_alerts = (
            self._provider.get_alerts()
        )

        self._build_content()

        self._refresh_table()

    def _build_content(self) -> None:
        """Build alert center."""

        self._add_summary()
        self._add_filters()
        self._add_alert_table()
        self._add_detail_panel()

    def _add_summary(self) -> None:
        """Add alert statistics."""

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

        critical = sum(
            alert.severity == "CRITICAL"
            and alert.status == "OPEN"
            for alert in self._all_alerts
        )

        high = sum(
            alert.severity == "HIGH"
            and alert.status == "OPEN"
            for alert in self._all_alerts
        )

        investigating = sum(
            alert.status == "INVESTIGATING"
            for alert in self._all_alerts
        )

        total = len(
            self._all_alerts
        )

        self._critical_value = (
            self._create_stat_card(
                layout,
                "CRITICAL",
                str(critical),
            )
        )

        self._high_value = (
            self._create_stat_card(
                layout,
                "HIGH",
                str(high),
            )
        )

        self._investigating_value = (
            self._create_stat_card(
                layout,
                "INVESTIGATING",
                str(investigating),
            )
        )

        self._total_value = (
            self._create_stat_card(
                layout,
                "TOTAL EVENTS",
                str(total),
            )
        )

        self.add_content(
            container
        )

    def _create_stat_card(
        self,
        layout: QHBoxLayout,
        title: str,
        value: str,
    ) -> QLabel:
        """Create alert statistic card."""

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

        title_label = QLabel(
            title
        )

        title_label.setObjectName(
            "trafficStatTitle"
        )

        value_label = QLabel(
            value
        )

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

    def _add_filters(self) -> None:
        """Add alert filters."""

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

        layout.setSpacing(10)

        search_label = QLabel(
            "SEARCH"
        )

        search_label.setObjectName(
            "trafficStatTitle"
        )

        layout.addWidget(
            search_label
        )

        self._search = QLineEdit()

        self._search.setPlaceholderText(
            "Alert title, asset or source IP..."
        )

        self._search.setObjectName(
            "assetSearch"
        )

        self._search.setClearButtonEnabled(
            True
        )

        self._search.textChanged.connect(
            self._refresh_table
        )

        layout.addWidget(
            self._search,
            1,
        )

        severity_label = QLabel(
            "SEVERITY"
        )

        severity_label.setObjectName(
            "trafficStatTitle"
        )

        layout.addWidget(
            severity_label
        )

        self._severity_filter = (
            QComboBox()
        )

        self._severity_filter.addItems(
            [
                "ALL",
                "CRITICAL",
                "HIGH",
                "MEDIUM",
                "LOW",
            ]
        )

        self._severity_filter.setObjectName(
            "assetFilter"
        )

        self._severity_filter.currentTextChanged.connect(
            self._refresh_table
        )

        layout.addWidget(
            self._severity_filter
        )

        status_label = QLabel(
            "STATUS"
        )

        status_label.setObjectName(
            "trafficStatTitle"
        )

        layout.addWidget(
            status_label
        )

        self._status_filter = (
            QComboBox()
        )

        self._status_filter.addItems(
            [
                "ALL",
                "OPEN",
                "INVESTIGATING",
                "ACKNOWLEDGED",
                "RESOLVED",
            ]
        )

        self._status_filter.setObjectName(
            "assetFilter"
        )

        self._status_filter.currentTextChanged.connect(
            self._refresh_table
        )

        layout.addWidget(
            self._status_filter
        )

        refresh_button = QPushButton(
            "REFRESH"
        )

        refresh_button.setObjectName(
            "secondaryButton"
        )

        refresh_button.clicked.connect(
            self._refresh_alerts
        )

        layout.addWidget(
            refresh_button
        )

        self.add_content(
            frame
        )

    def _add_alert_table(self) -> None:
        """Add alert table."""

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
            "SECURITY EVENTS"
        )

        title.setObjectName(
            "panelTitle"
        )

        layout.addWidget(
            title
        )

        self._table = AlertTable()

        self._table.itemSelectionChanged.connect(
            self._show_selected_alert
        )

        layout.addWidget(
            self._table,
            1,
        )

        self.add_content(
            frame
        )

    def _add_detail_panel(self) -> None:
        """Add selected alert details."""

        self._detail_frame = QFrame()

        self._detail_frame.setObjectName(
            "alertDetailPanel"
        )

        layout = QVBoxLayout(
            self._detail_frame
        )

        layout.setContentsMargins(
            16,
            14,
            16,
            14,
        )

        title = QLabel(
            "ALERT DETAILS"
        )

        title.setObjectName(
            "panelTitle"
        )

        layout.addWidget(
            title
        )

        self._detail_title = QLabel(
            "Select an alert to investigate"
        )

        self._detail_title.setObjectName(
            "alertDetailTitle"
        )

        layout.addWidget(
            self._detail_title
        )

        self._detail_info = QLabel(
            "No alert selected."
        )

        self._detail_info.setWordWrap(
            True
        )

        self._detail_info.setObjectName(
            "alertDetailInfo"
        )

        layout.addWidget(
            self._detail_info
        )

        self._ack_button = QPushButton(
            "ACKNOWLEDGE ALERT"
        )

        self._ack_button.setObjectName(
            "secondaryButton"
        )

        self._ack_button.setEnabled(
            False
        )

        self._ack_button.clicked.connect(
            self._acknowledge_selected
        )

        layout.addWidget(
            self._ack_button,
            alignment=Qt.AlignmentFlag.AlignLeft,
        )

        self.add_content(
            self._detail_frame
        )

    def _refresh_alerts(self) -> None:
        """Reload alert data."""

        self._all_alerts = (
            self._provider.get_alerts()
        )

        self._update_summary()
        self._refresh_table()

    def _refresh_table(
        self,
        *_args,
    ) -> None:
        """Apply current filters."""

        search = (
            self._search.text()
            .strip()
            .lower()
            if hasattr(
                self,
                "_search",
            )
            else ""
        )

        severity = (
            self._severity_filter.currentText()
            if hasattr(
                self,
                "_severity_filter",
            )
            else "ALL"
        )

        status = (
            self._status_filter.currentText()
            if hasattr(
                self,
                "_status_filter",
            )
            else "ALL"
        )

        filtered = []

        for alert in self._all_alerts:

            searchable_text = (
                f"{alert.title} "
                f"{alert.asset} "
                f"{alert.source_ip} "
                f"{alert.alert_id}"
            ).lower()

            matches_search = (
                not search
                or search in searchable_text
            )

            matches_severity = (
                severity == "ALL"
                or alert.severity
                == severity
            )

            matches_status = (
                status == "ALL"
                or alert.status
                == status
            )

            if (
                matches_search
                and matches_severity
                and matches_status
            ):
                filtered.append(
                    alert
                )

        self._table.set_alerts(
            filtered
        )

    def _show_selected_alert(self) -> None:
        """Display details for selected alert."""

        row = self._table.currentRow()

        if row < 0:
            return

        alert_title = (
            self._table.item(
                row,
                1,
            )
        )

        if alert_title is None:
            return

        title = alert_title.text()

        alert = next(
            (
                item
                for item in self._all_alerts
                if item.title == title
            ),
            None,
        )

        if alert is None:
            return

        self._selected_alert = alert

        self._detail_title.setText(
            f"{alert.severity}  |  {alert.title}"
        )

        details = (
            f"<b>Alert ID:</b> {alert.alert_id}<br>"
            f"<b>Asset:</b> {alert.asset} "
            f"({alert.asset_ip})<br>"
            f"<b>Source:</b> {alert.source_ip}<br>"
            f"<b>Protocol:</b> {alert.protocol}<br>"
            f"<b>Category:</b> {alert.category}<br>"
            f"<b>Status:</b> {alert.status}<br><br>"
            f"<b>Detection:</b> "
            f"{alert.detection_reason}<br><br>"
            f"<b>Recommended Action:</b> "
            f"{alert.recommended_action}"
        )

        self._detail_info.setText(
            details
        )

        self._ack_button.setEnabled(
            alert.status == "OPEN"
        )

    def _acknowledge_selected(self) -> None:
        """Acknowledge the selected alert."""

        if not hasattr(
            self,
            "_selected_alert",
        ):
            return

        alert_id = (
            self._selected_alert.alert_id
        )

        updated = []

        for alert in self._all_alerts:
            if alert.alert_id == alert_id:
                updated.append(
                    AlertData(
                        alert_id=alert.alert_id,
                        timestamp=alert.timestamp,
                        title=alert.title,
                        severity=alert.severity,
                        status="ACKNOWLEDGED",
                        asset=alert.asset,
                        asset_ip=alert.asset_ip,
                        source_ip=alert.source_ip,
                        protocol=alert.protocol,
                        category=alert.category,
                        description=alert.description,
                        detection_reason=alert.detection_reason,
                        recommended_action=alert.recommended_action,
                    )
                )
            else:
                updated.append(
                    alert
                )

        self._all_alerts = updated

        self._update_summary()
        self._refresh_table()

        self._detail_info.setText(
            "Alert acknowledged successfully."
        )

        self._ack_button.setEnabled(
            False
        )

    def _update_summary(self) -> None:
        """Update alert counters."""

        critical = sum(
            alert.severity == "CRITICAL"
            and alert.status == "OPEN"
            for alert in self._all_alerts
        )

        high = sum(
            alert.severity == "HIGH"
            and alert.status == "OPEN"
            for alert in self._all_alerts
        )

        investigating = sum(
            alert.status == "INVESTIGATING"
            for alert in self._all_alerts
        )

        total = len(
            self._all_alerts
        )

        self._critical_value.setText(
            str(critical)
        )

        self._high_value.setText(
            str(high)
        )

        self._investigating_value.setText(
            str(investigating)
        )

        self._total_value.setText(
            str(total)
        )