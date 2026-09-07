from typing import List

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QBrush, QColor, QFont
from PyQt6.QtWidgets import (
    QHeaderView,
    QTableWidget,
    QTableWidgetItem,
)

from data.traffic_data import PacketData


class TrafficTable(QTableWidget):
    """Reusable table for displaying network traffic."""

    HEADERS = [
        "TIME",
        "SOURCE",
        "DESTINATION",
        "PROTOCOL",
        "TYPE",
        "SIZE",
        "STATUS",
    ]

    MAX_ROWS = 100

    def __init__(self, parent=None) -> None:
        super().__init__(parent)

        self.setObjectName(
            "trafficTable"
        )

        self.setColumnCount(
            len(self.HEADERS)
        )

        self.setHorizontalHeaderLabels(
            self.HEADERS
        )

        self._configure_table()

    def _configure_table(self) -> None:
        """Configure table appearance and behaviour."""

        self.setAlternatingRowColors(False)

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

        self.verticalHeader().setVisible(False)

        header = self.horizontalHeader()

        header.setSectionResizeMode(
            QHeaderView.ResizeMode.Interactive
        )

        header.setStretchLastSection(True)

        widths = [
            80,
            110,
            110,
            110,
            90,
            70,
            90,
        ]

        for index, width in enumerate(widths):
            self.setColumnWidth(
                index,
                width,
            )

    def add_packet(
        self,
        packet: PacketData,
    ) -> None:
        """Add a packet to the top of the table."""

        self.insertRow(0)

        values = [
            packet.timestamp,
            packet.source,
            packet.destination,
            packet.protocol,
            packet.packet_type,
            f"{packet.size} B",
            packet.status,
        ]

        for column, value in enumerate(values):
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
                0,
                column,
                item,
            )

        self._apply_status_style(
            0,
            packet.status,
        )

        while self.rowCount() > self.MAX_ROWS:
            self.removeRow(
                self.rowCount() - 1
            )

    def add_packets(
        self,
        packets: List[PacketData],
    ) -> None:
        """Add multiple packets."""

        for packet in reversed(packets):
            self.add_packet(packet)

    def _apply_status_style(
        self,
        row: int,
        status: str,
    ) -> None:
        """Apply status styling to a traffic row."""

        status_item = self.item(
            row,
            6,
        )

        if status_item is None:
            return

        status_item.setTextAlignment(
            Qt.AlignmentFlag.AlignCenter
        )

        status_item.setFont(
            QFont(
                "Segoe UI",
                9,
                QFont.Weight.Bold,
            )
        )

        if status == "BLOCKED":
            status_item.setForeground(
                QBrush(
                    QColor("#df6b6b")
                )
            )
        else:
            status_item.setForeground(
                QBrush(
                    QColor("#55c77a")
                )
            )

    def clear_packets(self) -> None:
        """Remove all traffic records."""

        self.setRowCount(0)