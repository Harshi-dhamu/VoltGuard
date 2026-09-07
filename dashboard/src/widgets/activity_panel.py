from typing import List

from PyQt6.QtWidgets import (
    QFrame,
    QGridLayout,
    QLabel,
    QVBoxLayout,
)

from data.mock_data import ActivityData


class ActivityPanel(QFrame):
    """Displays recent network traffic activity."""

    def __init__(
        self,
        activity: List[ActivityData],
        parent=None,
    ) -> None:
        super().__init__(parent)

        self.setObjectName("panel")

        layout = QVBoxLayout(self)
        layout.setContentsMargins(18, 16, 18, 16)
        layout.setSpacing(10)

        title = QLabel("NETWORK ACTIVITY")
        title.setObjectName("panelTitle")

        layout.addWidget(title)

        grid = QGridLayout()
        grid.setHorizontalSpacing(16)
        grid.setVerticalSpacing(8)

        headers = [
            "TIME",
            "SOURCE",
            "DESTINATION",
            "PROTOCOL",
            "STATUS",
        ]

        for column, header in enumerate(headers):
            label = QLabel(header)
            label.setObjectName("tableHeader")
            grid.addWidget(label, 0, column)

        for row, item in enumerate(activity, start=1):
            values = [
                item.timestamp,
                item.source,
                item.destination,
                item.protocol,
                item.status,
            ]

            for column, value in enumerate(values):
                label = QLabel(value)

                if column == 4:
                    label.setObjectName(
                        "statusBlocked"
                        if value == "BLOCKED"
                        else "statusAllowed"
                    )
                else:
                    label.setObjectName("tableValue")

                grid.addWidget(label, row, column)

        layout.addLayout(grid)