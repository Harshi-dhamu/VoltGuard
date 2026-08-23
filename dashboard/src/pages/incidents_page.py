from typing import List

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QComboBox,
    QFrame,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QVBoxLayout,
)

from data.incident_data import (
    Incident,
    get_demo_incidents,
)

from widgets.incident_table import IncidentTable

from .base_page import BasePage


class IncidentsPage(BasePage):
    """VoltGuard incident investigation center."""

    def __init__(self, parent=None) -> None:
        super().__init__(
            "Incident Center",
            "Correlated security incidents and investigation workflow",
            parent,
        )

        self._all_incidents: List[Incident] = (
            get_demo_incidents()
        )

        self._selected_incident = None

        self._build_content()

        self._refresh_table(
            self._all_incidents
        )

    def _build_content(self) -> None:
        """Build incident center interface."""

        self._add_summary()
        self._add_filters()
        self._add_incident_table()
        self._add_details_panel()

    def _add_summary(self) -> None:
        """Add incident summary cards."""

        frame = QFrame()

        frame.setObjectName(
            "panel"
        )

        layout = QHBoxLayout(
            frame
        )

        layout.setContentsMargins(
            16,
            14,
            16,
            14,
        )

        layout.setSpacing(
            24
        )

        total = len(
            self._all_incidents
        )

        critical = len(
            [
                incident
                for incident in self._all_incidents
                if incident.severity == "CRITICAL"
            ]
        )

        investigating = len(
            [
                incident
                for incident in self._all_incidents
                if incident.status == "INVESTIGATING"
            ]
        )

        open_count = len(
            [
                incident
                for incident in self._all_incidents
                if incident.status == "OPEN"
            ]
        )

        self._add_summary_item(
            layout,
            "TOTAL INCIDENTS",
            str(total),
        )

        self._add_summary_item(
            layout,
            "CRITICAL",
            str(critical),
        )

        self._add_summary_item(
            layout,
            "OPEN",
            str(open_count),
        )

        self._add_summary_item(
            layout,
            "INVESTIGATING",
            str(investigating),
        )

        self.add_content(
            frame
        )

    def _add_summary_item(
        self,
        layout: QHBoxLayout,
        title: str,
        value: str,
    ) -> None:
        """Add one summary metric."""

        container = QFrame()

        container.setObjectName(
            "statCard"
        )

        card_layout = QVBoxLayout(
            container
        )

        card_layout.setContentsMargins(
            12,
            8,
            12,
            8,
        )

        title_label = QLabel(
            title
        )

        title_label.setObjectName(
            "sidebarSectionTitle"
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
            container
        )

    def _add_filters(self) -> None:
        """Add incident filtering controls."""

        frame = QFrame()

        frame.setObjectName(
            "panel"
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

        title = QLabel(
            "INCIDENT QUEUE"
        )

        title.setObjectName(
            "panelTitle"
        )

        layout.addWidget(
            title
        )

        layout.addStretch()

        severity_label = QLabel(
            "Severity"
        )

        severity_label.setObjectName(
            "alertDetailInfo"
        )

        layout.addWidget(
            severity_label
        )

        self._severity_filter = QComboBox()

        self._severity_filter.addItems(
            [
                "All",
                "CRITICAL",
                "HIGH",
                "MEDIUM",
                "LOW",
            ]
        )

        self._severity_filter.currentTextChanged.connect(
            self._apply_filters
        )

        layout.addWidget(
            self._severity_filter
        )

        status_label = QLabel(
            "Status"
        )

        status_label.setObjectName(
            "alertDetailInfo"
        )

        layout.addWidget(
            status_label
        )

        self._status_filter = QComboBox()

        self._status_filter.addItems(
            [
                "All",
                "OPEN",
                "INVESTIGATING",
                "ACKNOWLEDGED",
                "RESOLVED",
            ]
        )

        self._status_filter.currentTextChanged.connect(
            self._apply_filters
        )

        layout.addWidget(
            self._status_filter
        )

        self.add_content(
            frame
        )

    def _add_incident_table(self) -> None:
        """Add incident table."""

        self._table = IncidentTable()

        self._table.incident_selected.connect(
            self._show_incident
        )

        self.add_content(
            self._table
        )

    def _add_details_panel(self) -> None:
        """Add incident investigation details."""

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
            "INCIDENT INVESTIGATION"
        )

        title.setObjectName(
            "panelTitle"
        )

        layout.addWidget(
            title
        )

        self._detail_title = QLabel(
            "Select an incident to inspect"
        )

        self._detail_title.setObjectName(
            "alertDetailTitle"
        )

        layout.addWidget(
            self._detail_title
        )

        self._detail_meta = QLabel(
            "No incident selected."
        )

        self._detail_meta.setObjectName(
            "alertDetailInfo"
        )

        layout.addWidget(
            self._detail_meta
        )

        self._detail_description = QLabel(
            "Incident description will appear here."
        )

        self._detail_description.setObjectName(
            "alertDetailInfo"
        )

        self._detail_description.setWordWrap(
            True
        )

        layout.addWidget(
            self._detail_description
        )

        self._detail_recommendation = QLabel(
            "Recommended response will appear here."
        )

        self._detail_recommendation.setObjectName(
            "alertDetailInfo"
        )

        self._detail_recommendation.setWordWrap(
            True
        )

        layout.addWidget(
            self._detail_recommendation
        )

        self._acknowledge_button = QPushButton(
            "ACKNOWLEDGE INCIDENT"
        )

        self._acknowledge_button.setObjectName(
            "secondaryButton"
        )

        self._acknowledge_button.setEnabled(
            False
        )

        self._acknowledge_button.clicked.connect(
            self._acknowledge_selected
        )

        layout.addWidget(
            self._acknowledge_button,
            alignment=Qt.AlignmentFlag.AlignLeft,
        )

        self.add_content(
            frame
        )

    def _apply_filters(self) -> None:
        """Apply severity and status filters."""

        severity = (
            self._severity_filter.currentText()
        )

        status = (
            self._status_filter.currentText()
        )

        filtered = [
            incident
            for incident in self._all_incidents
            if (
                severity == "All"
                or incident.severity == severity
            )
            and (
                status == "All"
                or incident.status == status
            )
        ]

        self._refresh_table(
            filtered
        )

    def _refresh_table(
        self,
        incidents: List[Incident],
    ) -> None:
        """Refresh the incident table."""

        if not hasattr(
            self,
            "_table",
        ):
            return

        self._table.set_incidents(
            incidents
        )

    def _show_incident(
        self,
        incident: Incident,
    ) -> None:
        """Display selected incident details."""

        self._selected_incident = incident

        self._detail_title.setText(
            f"{incident.incident_id}  |  "
            f"{incident.title}"
        )

        self._detail_meta.setText(
            f"Severity: {incident.severity}    "
            f"Status: {incident.status}    "
            f"Asset: {incident.asset}    "
            f"Source: {incident.source_module}    "
            f"Detected: {incident.detected_at}"
        )

        self._detail_description.setText(
            f"Description: "
            f"{incident.description}"
        )

        self._detail_recommendation.setText(
            f"Recommended response: "
            f"{incident.recommendation}"
        )

        self._acknowledge_button.setEnabled(
            incident.status != "ACKNOWLEDGED"
            and incident.status != "RESOLVED"
        )

    def _acknowledge_selected(self) -> None:
        """Acknowledge the selected incident."""

        if self._selected_incident is None:
            return

        incident_id = (
            self._selected_incident.incident_id
        )

        for incident in self._all_incidents:

            if incident.incident_id == incident_id:
                incident.status = "ACKNOWLEDGED"
                break

        self._show_incident(
            self._selected_incident
        )

        self._apply_filters()