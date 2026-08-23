from typing import List

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QBrush, QColor, QFont
from PyQt6.QtWidgets import (
    QHeaderView,
    QTableWidget,
    QTableWidgetItem,
)

from data.event_log import EventLogEntry


class EventMonitor(QTableWidget):
    """Reusable real-time security event monitor."""

    HEADERS = [
        "TIME",
        "TYPE",
        "SOURCE MODULE",
        "SEVERITY",
        "EVENT",
    ]

    def __init__(
        self,
        parent=None,
    ) -> None:
        super().__init__(
            parent
        )

        self.setObjectName(
            "eventMonitor"
        )

        self.setColumnCount(
            len(self.HEADERS)
        )

        self.setHorizontalHeaderLabels(
            self.HEADERS
        )

        self._configure_table()

    def _configure_table(self) -> None:
        """Configure event table."""

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
            80,
            90,
            170,
            100,
            400,
        ]

        for index, width in enumerate(
            widths
        ):
            self.setColumnWidth(
                index,
                width,
            )

    def set_events(
        self,
        events: List[EventLogEntry],
    ) -> None:
        """Replace displayed events."""

        self.setRowCount(0)

        for event in events:
            self.add_event(
                event
            )

    def add_event(
        self,
        event: EventLogEntry,
    ) -> None:
        """Add an event to the table."""

        row = self.rowCount()

        self.insertRow(
            row
        )

        values = [
            event.timestamp,
            event.event_type,
            event.source_module,
            event.severity,
            event.summary,
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

        self._style_type(
            row,
            event.event_type,
        )

        self._style_severity(
            row,
            event.severity,
        )

    def add_event_at_row(
            self,
            event: EventLogEntry,
            row: int,
            ) -> None:
        """Insert an event at a specific row."""
        values = [
            event.timestamp,
            event.event_type,
            event.source_module,
            event.severity,
            event.summary,
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
                    QFont.Weight.Bold,
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

            self._style_type(
                row,
                event.event_type,
                )

            self._style_severity(
                row,
                event.severity,
                )
    
    def _style_type(
        self,
        row: int,
        event_type: str,
    ) -> None:
        """Style event type."""

        item = self.item(
            row,
            1,
        )

        if item is None:
            return

        item.setTextAlignment(
            Qt.AlignmentFlag.AlignCenter
        )

        colors = {
            "PACKET": "#6f9bb5",
            "THREAT": "#df6b6b",
            "DECISION": "#d6a84f",
        }

        item.setForeground(
            QBrush(
                QColor(
                    colors.get(
                        event_type,
                        "#aeb8c2",
                    )
                )
            )
        )

        item.setFont(
            QFont(
                "Segoe UI",
                9,
                QFont.Weight.Bold,
            )
        )

    def _style_severity(
        self,
        row: int,
        severity: str,
    ) -> None:
        """Style severity."""

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
            "CRITICAL": "#ef5252",
            "HIGH": "#df6b6b",
            "MEDIUM": "#d6a84f",
            "LOW": "#55c77a",
            "INFO": "#6f9bb5",
        }

        item.setForeground(
            QBrush(
                QColor(
                    colors.get(
                        severity,
                        "#aeb8c2",
                    )
                )
            )
        )

        item.setFont(
            QFont(
                "Segoe UI",
                9,
                QFont.Weight.Bold,
            )
        )