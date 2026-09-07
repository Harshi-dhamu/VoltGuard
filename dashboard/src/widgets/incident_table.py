from typing import List, Optional

from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtWidgets import (
    QHeaderView,
    QTableWidget,
    QTableWidgetItem,
)

from data.incident_data import Incident


class IncidentTable(QTableWidget):
    """Reusable security incident table."""

    incident_selected = pyqtSignal(object)

    HEADERS = [
        "ID",
        "SEVERITY",
        "INCIDENT",
        "ASSET",
        "SOURCE",
        "STATUS",
        "DETECTED",
    ]

    def __init__(self, parent=None) -> None:
        super().__init__(parent)

        self.setObjectName(
            "incidentTable"
        )

        self.setColumnCount(
            len(self.HEADERS)
        )

        self.setHorizontalHeaderLabels(
            self.HEADERS
        )

        self.setSelectionBehavior(
            QTableWidget.SelectionBehavior.SelectRows
        )

        self.setSelectionMode(
            QTableWidget.SelectionMode.SingleSelection
        )

        self.setEditTriggers(
            QTableWidget.EditTrigger.NoEditTriggers
        )

        self.setAlternatingRowColors(
            False
        )

        self.setShowGrid(
            False
        )

        self.verticalHeader().setVisible(
            False
        )

        header = self.horizontalHeader()

        header.setSectionResizeMode(
            0,
            QHeaderView.ResizeMode.ResizeToContents,
        )

        header.setSectionResizeMode(
            1,
            QHeaderView.ResizeMode.ResizeToContents,
        )

        header.setSectionResizeMode(
            2,
            QHeaderView.ResizeMode.Stretch,
        )

        header.setSectionResizeMode(
            3,
            QHeaderView.ResizeMode.ResizeToContents,
        )

        header.setSectionResizeMode(
            4,
            QHeaderView.ResizeMode.ResizeToContents,
        )

        header.setSectionResizeMode(
            5,
            QHeaderView.ResizeMode.ResizeToContents,
        )

        header.setSectionResizeMode(
            6,
            QHeaderView.ResizeMode.ResizeToContents,
        )

        self.itemSelectionChanged.connect(
            self._selection_changed
        )

    def set_incidents(
        self,
        incidents: List[Incident],
    ) -> None:
        """Replace table contents."""

        self.setRowCount(0)

        for incident in incidents:
            self.add_incident(
                incident
            )

    def add_incident(
        self,
        incident: Incident,
    ) -> None:
        """Add one incident to the table."""

        row = self.rowCount()

        self.insertRow(
            row
        )

        values = [
            incident.incident_id,
            incident.severity,
            incident.title,
            incident.asset,
            incident.source_module,
            incident.status,
            incident.detected_at,
        ]

        for column, value in enumerate(values):

            item = QTableWidgetItem(
                str(value)
            )

            item.setTextAlignment(
                Qt.AlignmentFlag.AlignVCenter
                | Qt.AlignmentFlag.AlignLeft
            )

            item.setData(
                Qt.ItemDataRole.UserRole,
                incident,
            )

            self.setItem(
                row,
                column,
                item,
            )

        self.setRowHeight(
            row,
            44,
        )

        self._apply_severity_style(
            row,
            incident.severity,
        )

        self._apply_status_style(
            row,
            incident.status,
        )

    def _apply_severity_style(
        self,
        row: int,
        severity: str,
    ) -> None:
        """Apply semantic severity styling."""

        item = self.item(
            row,
            1,
        )

        if item is None:
            return

        item.setData(
            Qt.ItemDataRole.UserRole + 1,
            severity,
        )

        item.setText(
            severity
        )

    def _apply_status_style(
        self,
        row: int,
        status: str,
    ) -> None:
        """Apply semantic status styling."""

        item = self.item(
            row,
            5,
        )

        if item is None:
            return

        item.setData(
            Qt.ItemDataRole.UserRole + 2,
            status,
        )

    def _selection_changed(self) -> None:
        """Emit the selected incident."""

        rows = self.selectionModel().selectedRows()

        if not rows:
            return

        row = rows[0].row()

        item = self.item(
            row,
            0,
        )

        if item is None:
            return

        incident = item.data(
            Qt.ItemDataRole.UserRole
        )

        if incident is not None:
            self.incident_selected.emit(
                incident
            )

    def selected_incident(self) -> Optional[Incident]:
        """Return the currently selected incident."""

        rows = self.selectionModel().selectedRows()

        if not rows:
            return None

        row = rows[0].row()

        item = self.item(
            row,
            0,
        )

        if item is None:
            return None

        return item.data(
            Qt.ItemDataRole.UserRole
        )