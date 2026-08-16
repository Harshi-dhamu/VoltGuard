from PyQt6.QtWidgets import (
    QFrame,
    QLabel,
    QVBoxLayout,
)

from data.mock_data import get_activity

from widgets.activity_panel import ActivityPanel

from .base_page import BasePage


class TrafficPage(BasePage):
    """Network traffic monitoring page."""

    def __init__(self, parent=None) -> None:
        super().__init__(
            "Traffic Monitor",
            "Industrial network packet inspection and communication activity",
            parent,
        )

        self._build_content()

    def _build_content(self) -> None:
        self._add_monitor_status()

        activity = ActivityPanel(
            get_activity()
        )

        self.add_content(activity)
        self.add_stretch()

    def _add_monitor_status(self) -> None:
        frame = QFrame()
        frame.setObjectName("systemBar")

        layout = QVBoxLayout(frame)
        layout.setContentsMargins(
            16,
            14,
            16,
            14,
        )

        title = QLabel(
            "PACKET INSPECTION ENGINE"
        )
        title.setObjectName(
            "panelTitle"
        )

        status = QLabel(
            "●  ACTIVE"
        )
        status.setObjectName(
            "protectionStatus"
        )

        layout.addWidget(title)
        layout.addWidget(status)

        self.add_content(frame)