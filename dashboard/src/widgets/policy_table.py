from typing import List

from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtWidgets import (
    QHeaderView,
    QTableWidget,
    QTableWidgetItem,
)

from data.policy_data import SecurityPolicy


class PolicyTable(QTableWidget):
    """Reusable security policy table."""

    policy_selected = pyqtSignal(object)

    HEADERS = [
        "POLICY ID",
        "POLICY NAME",
        "MODULE",
        "CONDITION",
        "SEVERITY",
        "ACTION",
        "STATUS",
        "UPDATED",
    ]

    def __init__(
        self,
        parent=None,
    ) -> None:
        super().__init__(parent)

        self.setObjectName(
            "policyTable"
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
            QHeaderView.ResizeMode.ResizeToContents,
        )

        header.setSectionResizeMode(
            3,
            QHeaderView.ResizeMode.Stretch,
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

        header.setSectionResizeMode(
            7,
            QHeaderView.ResizeMode.ResizeToContents,
        )

        self.verticalHeader().setVisible(
            False
        )

        self.itemSelectionChanged.connect(
            self._selection_changed
        )

    def set_policies(
        self,
        policies: List[SecurityPolicy],
    ) -> None:
        """Populate the table with policies."""

        self.setRowCount(0)

        for policy in policies:

            row = self.rowCount()

            self.insertRow(
                row
            )

            values = [
                policy.policy_id,
                policy.name,
                policy.module,
                policy.condition,
                policy.severity,
                policy.action,
                "ENABLED"
                if policy.enabled
                else "DISABLED",
                policy.last_updated,
            ]

            for column, value in enumerate(
                values
            ):

                item = QTableWidgetItem(
                    value
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

            self._apply_status_style(
                row,
                policy,
            )

            self.setRowHeight(
                row,
                46,
            )

    def _apply_status_style(
        self,
        row: int,
        policy: SecurityPolicy,
    ) -> None:
        """Apply semantic labels to policy rows."""

        severity_item = self.item(
            row,
            4,
        )

        action_item = self.item(
            row,
            5,
        )

        status_item = self.item(
            row,
            6,
        )

        if severity_item is not None:
            severity_item.setData(
                Qt.ItemDataRole.UserRole,
                policy.severity,
            )

        if action_item is not None:
            action_item.setData(
                Qt.ItemDataRole.UserRole,
                policy.action,
            )

        if status_item is not None:
            status_item.setData(
                Qt.ItemDataRole.UserRole,
                "ENABLED"
                if policy.enabled
                else "DISABLED",
            )

    def _selection_changed(self) -> None:
        """Emit the selected policy."""

        rows = self.selectionModel().selectedRows()

        if not rows:
            return

        row = rows[0].row()

        values = []

        for column in range(
            self.columnCount()
        ):
            item = self.item(
                row,
                column,
            )

            values.append(
                item.text()
                if item is not None
                else ""
            )

        self.policy_selected.emit(
            values
        )