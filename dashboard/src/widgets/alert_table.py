from typing import List

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QBrush, QColor, QFont
from PyQt6.QtWidgets import (
    QHeaderView,
    QTableWidget,
    QTableWidgetItem,
)

from data.alert_data import AlertData


class AlertTable(QTableWidget):
    """Reusable security alert table."""

    HEADERS = [
        "TIME",
        "ALERT",
        "SEVERITY",
        "STATUS",
        "ASSET",
        "SOURCE",
        "PROTOCOL",
        "CATEGORY",
    ]

    def __init__(
        self,
        parent=None,
    ) -> None:
        super().__init__(parent)

        self.setObjectName(
            "alertTable"
        )

        self.setColumnCount(
            len(self.HEADERS)
        )

        self.setHorizontalHeaderLabels(
            self.HEADERS
        )

        self._configure_table()

    def _configure_table(self) -> None:
        """Configure table behaviour."""

        self.setSelectionBehavior(
            QTableWidget.SelectionBehavior.SelectRows
        )

        self.setSelectionMode(
            QTableWidget.SelectionMode.SingleSelection
        )

        self.setEditTriggers(
            QTableWidget.EditTrigger.NoEditTriggers
        )

        self.setFocusPolicy(
            Qt.FocusPolicy.NoFocus
        )

        self.verticalHeader().setVisible(
            False
        )

        header = self.horizontalHeader()

        header.setSectionResizeMode(
            QHeaderView.ResizeMode.Interactive
        )

        header.setStretchLastSection(
            True
        )

        widths = [
            75,
            180,
            95,
            110,
            145,
            115,
            110,
            150,
        ]

        for index, width in enumerate(
            widths
        ):
            self.setColumnWidth(
                index,
                width,
            )

    def set_alerts(
        self,
        alerts: List[AlertData],
    ) -> None:
        """Replace table contents."""

        self.setRowCount(0)

        for alert in alerts:
            self.add_alert(alert)

    def add_alert(
        self,
        alert: AlertData,
    ) -> None:
        """Add one security alert."""

        row = self.rowCount()

        self.insertRow(row)

        values = [
            alert.timestamp,
            alert.title,
            alert.severity,
            alert.status,
            alert.asset,
            alert.source_ip,
            alert.protocol,
            alert.category,
        ]

        for column, value in enumerate(
            values
        ):
            item = QTableWidgetItem(
                value
            )

            item.setFont(
                QFont(
                    "Segoe UI",
                    9,
                )
            )

            item.setTextAlignment(
                Qt.AlignmentFlag.AlignVCenter
                | Qt.AlignmentFlag.AlignLeft
            )

            self.setItem(
                row,
                column,
                item,
            )

        self._style_severity(
            row,
            alert.severity,
        )

        self._style_status(
            row,
            alert.status,
        )

    def _style_severity(
        self,
        row: int,
        severity: str,
    ) -> None:
        """Apply severity styling."""

        item = self.item(
            row,
            2,
        )

        if item is None:
            return

        item.setTextAlignment(
            Qt.AlignmentFlag.AlignCenter
        )

        item.setFont(
            QFont(
                "Segoe UI",
                9,
                QFont.Weight.Bold,
            )
        )

        colors = {
            "CRITICAL": "#ef5252",
            "HIGH": "#df6b6b",
            "MEDIUM": "#d6a84f",
            "LOW": "#55c77a",
        }

        color = colors.get(
            severity,
            "#aeb8c2",
        )

        item.setForeground(
            QBrush(
                QColor(color)
            )
        )

    def _style_status(
        self,
        row: int,
        status: str,
    ) -> None:
        """Apply alert status styling."""

        item = self.item(
            row,
            3,
        )

        if item is None:
            return

        item.setTextAlignment(
            Qt.AlignmentFlag.AlignCenter
        )

        colors = {
            "OPEN": "#df6b6b",
            "INVESTIGATING": "#d6a84f",
            "ACKNOWLEDGED": "#6f9bb5",
            "RESOLVED": "#55c77a",
        }

        color = colors.get(
            status,
            "#aeb8c2",
        )

        item.setForeground(
            QBrush(
                QColor(color)
            )
        )