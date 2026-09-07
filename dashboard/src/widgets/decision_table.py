from typing import List

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QBrush, QColor, QFont
from PyQt6.QtWidgets import (
    QHeaderView,
    QTableWidget,
    QTableWidgetItem,
)

from data.decision_data import DecisionData


class DecisionTable(QTableWidget):
    """Reusable security decision table."""

    HEADERS = [
        "TIME",
        "DECISION",
        "SEVERITY",
        "CONFIDENCE",
        "ASSET",
        "SOURCE",
        "CATEGORY",
        "ACTION",
    ]

    def __init__(
        self,
        parent=None,
    ) -> None:
        super().__init__(parent)

        self.setObjectName(
            "decisionTable"
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
            120,
            90,
            100,
            145,
            115,
            140,
            110,
        ]

        for index, width in enumerate(
            widths
        ):
            self.setColumnWidth(
                index,
                width,
            )

    def set_decisions(
        self,
        decisions: List[DecisionData],
    ) -> None:
        """Replace table contents."""

        self.setRowCount(0)

        for decision in decisions:
            self.add_decision(
                decision
            )

    def add_decision(
        self,
        decision: DecisionData,
    ) -> None:
        """Add one security decision."""

        row = self.rowCount()

        self.insertRow(row)

        values = [
            decision.timestamp,
            decision.decision,
            decision.severity,
            f"{decision.confidence}%",
            decision.asset,
            decision.source,
            decision.category,
            decision.recommended_action,
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

        self._style_decision(
            row,
            decision.decision,
        )

        self._style_severity(
            row,
            decision.severity,
        )

        self._style_confidence(
            row,
            decision.confidence,
        )

    def _style_decision(
        self,
        row: int,
        decision: str,
    ) -> None:
        """Style the decision column."""

        item = self.item(
            row,
            1,
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
            "BLOCK": "#df6b6b",
            "INVESTIGATE": "#d6a84f",
            "MONITOR": "#6f9bb5",
            "ALLOW": "#55c77a",
        }

        item.setForeground(
            QBrush(
                QColor(
                    colors.get(
                        decision,
                        "#aeb8c2",
                    )
                )
            )
        )

    def _style_severity(
        self,
        row: int,
        severity: str,
    ) -> None:
        """Style the severity column."""

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

    def _style_confidence(
        self,
        row: int,
        confidence: int,
    ) -> None:
        """Style the confidence column."""

        item = self.item(
            row,
            3,
        )

        if item is None:
            return

        item.setTextAlignment(
            Qt.AlignmentFlag.AlignCenter
        )

        if confidence >= 90:
            color = "#55c77a"
        elif confidence >= 75:
            color = "#d6a84f"
        else:
            color = "#df6b6b"

        item.setForeground(
            QBrush(
                QColor(color)
            )
        )