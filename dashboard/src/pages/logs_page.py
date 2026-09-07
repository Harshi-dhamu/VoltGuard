from PyQt6.QtWidgets import (
    QFrame,
    QHBoxLayout,
    QLabel,
    QVBoxLayout,
)

from .base_page import BasePage


class LogsPage(BasePage):
    """System and security event log page."""

    def __init__(self, parent=None) -> None:
        super().__init__(
            "Event Logs",
            "Security, packet inspection, and system activity history",
            parent,
        )

        self._build_content()

    def _build_content(self) -> None:
        events = [
            (
                "10:42:17",
                "SECURITY",
                "PLC-03 write command blocked",
            ),
            (
                "10:41:52",
                "TRAFFIC",
                "Modbus communication allowed",
            ),
            (
                "10:40:31",
                "DECISION",
                "Command evaluated as safe",
            ),
            (
                "10:39:44",
                "SECURITY",
                "Threshold violation detected",
            ),
        ]

        for timestamp, category, message in events:
            self.add_content(
                self._create_log_row(
                    timestamp,
                    category,
                    message,
                )
            )

        self.add_stretch()

    def _create_log_row(
        self,
        timestamp: str,
        category: str,
        message: str,
    ) -> QFrame:
        row = QFrame()
        row.setObjectName("logRow")

        layout = QHBoxLayout(row)

        layout.setContentsMargins(
            12,
            9,
            12,
            9,
        )

        time_label = QLabel(timestamp)
        time_label.setObjectName(
            "logTime"
        )

        category_label = QLabel(category)
        category_label.setObjectName(
            "logCategory"
        )

        message_label = QLabel(message)
        message_label.setObjectName(
            "logMessage"
        )

        layout.addWidget(time_label)
        layout.addWidget(category_label)
        layout.addWidget(message_label)

        return row