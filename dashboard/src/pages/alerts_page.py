from PyQt6.QtWidgets import (
    QFrame,
    QVBoxLayout,
)

from data.mock_data import get_alerts

from widgets.alert_panel import AlertPanel

from .base_page import BasePage


class AlertsPage(BasePage):
    """Security alert management page."""

    def __init__(self, parent=None) -> None:
        super().__init__(
            "Security Alerts",
            "Detected events requiring investigation or operator attention",
            parent,
        )

        self._build_content()

    def _build_content(self) -> None:
        panel = AlertPanel(
            get_alerts()
        )

        self.add_content(panel)
        self.add_stretch()