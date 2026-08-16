from typing import Dict

from PyQt6.QtCore import pyqtSignal
from PyQt6.QtWidgets import (
    QFrame,
    QLabel,
    QPushButton,
    QVBoxLayout,
)


class Sidebar(QFrame):
    """Main navigation sidebar."""

    navigation_requested = pyqtSignal(str)

    def __init__(self, parent=None) -> None:
        super().__init__(parent)

        self.setObjectName("sidebar")
        self.setFixedWidth(220)

        self._buttons: Dict[str, QPushButton] = {}

        self._build_ui()

        self.set_active_page("Overview")

    def _build_ui(self) -> None:
        layout = QVBoxLayout(self)

        layout.setContentsMargins(
            14,
            18,
            14,
            18,
        )

        layout.setSpacing(6)

        logo = QLabel("VOLTGUARD")
        logo.setObjectName("sidebarLogo")

        subtitle = QLabel(
            "OT SECURITY PLATFORM"
        )
        subtitle.setObjectName(
            "sidebarSubtitle"
        )

        layout.addWidget(logo)
        layout.addWidget(subtitle)

        separator = QFrame()
        separator.setObjectName(
            "sidebarSeparator"
        )

        separator.setFixedHeight(1)

        layout.addSpacing(14)
        layout.addWidget(separator)
        layout.addSpacing(12)

        navigation_items = [
            ("▣", "Overview"),
            ("◉", "Traffic Monitor"),
            ("▤", "Assets"),
            ("⚠", "Alerts"),
            ("✓", "Decisions"),
            ("≡", "Event Logs"),
        ]

        for icon, text in navigation_items:
            button = QPushButton(
                f"{icon}    {text}"
            )

            button.setObjectName(
                "navigationButton"
            )

            button.setCursor(
                button.cursor()
            )

            button.clicked.connect(
                lambda checked=False,
                item=text:
                self._navigation_clicked(item)
            )

            self._buttons[text] = button

            layout.addWidget(button)

        layout.addStretch()

        system_title = QLabel("SYSTEM")
        system_title.setObjectName(
            "sidebarSectionTitle"
        )

        status = QLabel(
            "●  Monitoring active"
        )
        status.setObjectName(
            "sidebarSystemStatus"
        )

        layout.addWidget(system_title)
        layout.addWidget(status)

    def _navigation_clicked(
        self,
        destination: str,
    ) -> None:
        self.set_active_page(destination)
        self.navigation_requested.emit(
            destination
        )

    def set_active_page(
        self,
        page_name: str,
    ) -> None:
        """Update the highlighted navigation item."""
        for name, button in self._buttons.items():
            button.setProperty(
                "active",
                name == page_name,
            )

            button.style().unpolish(button)
            button.style().polish(button)
            button.update()