from PyQt6.QtWidgets import QFrame, QVBoxLayout

from data.mock_data import get_decisions

from widgets.decision_panel import DecisionPanel

from .base_page import BasePage


class DecisionsPage(BasePage):
    """Decision engine monitoring page."""

    def __init__(self, parent=None) -> None:
        super().__init__(
            "Security Decisions",
            "Commands evaluated by the VoltGuard decision engine",
            parent,
        )

        self._build_content()

    def _build_content(self) -> None:
        panel = DecisionPanel(
            get_decisions()
        )

        self.add_content(panel)
        self.add_stretch()