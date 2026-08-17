from typing import List

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QBrush, QColor, QFont
from PyQt6.QtWidgets import (
    QHeaderView,
    QTableWidget,
    QTableWidgetItem,
)

from data.asset_data import AssetData


class AssetTable(QTableWidget):
    """Reusable table for displaying OT assets."""

    HEADERS = [
        "ASSET",
        "TYPE",
        "IP ADDRESS",
        "PROTOCOL",
        "ZONE",
        "STATUS",
        "RISK",
        "LAST SEEN",
    ]

    def __init__(
        self,
        parent=None,
    ) -> None:
        super().__init__(parent)

        self.setObjectName(
            "assetTable"
        )

        self.setColumnCount(
            len(self.HEADERS)
        )

        self.setHorizontalHeaderLabels(
            self.HEADERS
        )

        self._configure_table()

    def _configure_table(self) -> None:
        """Configure table appearance."""

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
            150,
            100,
            125,
            115,
            110,
            100,
            90,
            100,
        ]

        for index, width in enumerate(
            widths
        ):
            self.setColumnWidth(
                index,
                width,
            )

    def set_assets(
        self,
        assets: List[AssetData],
    ) -> None:
        """Replace the table contents with assets."""

        self.setRowCount(0)

        for asset in assets:
            self.add_asset(asset)

    def add_asset(
        self,
        asset: AssetData,
    ) -> None:
        """Add an asset to the table."""

        row = self.rowCount()

        self.insertRow(row)

        values = [
            asset.name,
            asset.asset_type,
            asset.ip_address,
            asset.protocol,
            asset.zone,
            asset.status,
            asset.risk,
            asset.last_seen,
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

        self._style_status(
            row,
            asset.status,
        )

        self._style_risk(
            row,
            asset.risk,
        )

    def _style_status(
        self,
        row: int,
        status: str,
    ) -> None:
        """Style the asset status."""

        item = self.item(
            row,
            5,
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

        if status == "ONLINE":
            item.setForeground(
                QBrush(
                    QColor("#55c77a")
                )
            )
        else:
            item.setForeground(
                QBrush(
                    QColor("#d6a84f")
                )
            )

    def _style_risk(
        self,
        row: int,
        risk: str,
    ) -> None:
        """Style the asset risk level."""

        item = self.item(
            row,
            6,
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

        risk_colors = {
            "LOW": "#55c77a",
            "MEDIUM": "#d6a84f",
            "HIGH": "#df6b6b",
            "CRITICAL": "#ef5252",
        }

        color = risk_colors.get(
            risk,
            "#aeb8c2",
        )

        item.setForeground(
            QBrush(
                QColor(color)
            )
        )