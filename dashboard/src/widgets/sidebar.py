from typing import Dict

from PyQt6.QtCore import pyqtSignal
from PyQt6.QtWidgets import (
    QFrame,
    QLabel,
    QPushButton,
    QVBoxLayout,
)


class Sidebar(QFrame):
    """Main navigation sidebar for VoltGuard."""

    navigation_requested = pyqtSignal(str)

    def __init__(self, parent=None) -> None:
        super().__init__(parent)

        self.setObjectName("sidebar")
        self.setFixedWidth(220)

        self._buttons: Dict[str, QPushButton] = {}

        self._build_ui()

        self.set_active_page("Overview")

    def _build_ui(self) -> None:
        """Build the sidebar navigation."""

        layout = QVBoxLayout(self)

        layout.setContentsMargins(
            14,
            18,
            14,
            18,
        )

        layout.setSpacing(6)

        # -------------------------------------------------
        # BRANDING
        # -------------------------------------------------

        logo = QLabel("VOLTGUARD")

        logo.setObjectName(
            "sidebarLogo"
        )

        subtitle = QLabel(
            "OT SECURITY PLATFORM"
        )

        subtitle.setObjectName(
            "sidebarSubtitle"
        )

        layout.addWidget(logo)
        layout.addWidget(subtitle)

        # -------------------------------------------------
        # TOP SEPARATOR
        # -------------------------------------------------

        separator = QFrame()

        separator.setObjectName(
            "sidebarSeparator"
        )

        separator.setFixedHeight(1)

        layout.addSpacing(14)
        layout.addWidget(separator)
        layout.addSpacing(12)

        # -------------------------------------------------
        # MONITORING
        # -------------------------------------------------

        monitoring_title = QLabel(
            "MONITORING"
        )

        monitoring_title.setObjectName(
            "sidebarSectionTitle"
        )

        layout.addWidget(
            monitoring_title
        )

        monitoring_items = [
            ("▣", "Overview"),
            ("◉", "Traffic Monitor"),
            ("▤", "Assets"),
        ]

        self._add_navigation_items(
            layout,
            monitoring_items,
        )

        # -------------------------------------------------
        # SECURITY
        # -------------------------------------------------

        security_title = QLabel(
            "SECURITY"
        )

        security_title.setObjectName(
            "sidebarSectionTitle"
        )

        layout.addSpacing(12)

        layout.addWidget(
            security_title
        )

        security_items = [
            ("⚠", "Alerts"),
            ("✓", "Decisions"),
            ("≡", "Event Logs"),
        ]

        self._add_navigation_items(
            layout,
            security_items,
        )

        # -------------------------------------------------
        # INTEGRATION
        # -------------------------------------------------

        integration_title = QLabel(
            "INTEGRATION"
        )

        integration_title.setObjectName(
            "sidebarSectionTitle"
        )

        layout.addSpacing(12)

        layout.addWidget(
            integration_title
        )

        integration_items = [
            ("↔", "System Integration"),
            ("◌", "Live Event Monitor"),
        ]

        self._add_navigation_items(
            layout,
            integration_items,
        )

        # -------------------------------------------------
        # BOTTOM SYSTEM STATUS
        # -------------------------------------------------

        layout.addStretch()

        system_separator = QFrame()

        system_separator.setObjectName(
            "sidebarSeparator"
        )

        system_separator.setFixedHeight(1)

        layout.addWidget(
            system_separator
        )

        layout.addSpacing(10)

        system_title = QLabel(
            "SYSTEM"
        )

        system_title.setObjectName(
            "sidebarSectionTitle"
        )

        status = QLabel(
            "●  Monitoring active"
        )

        status.setObjectName(
            "sidebarSystemStatus"
        )

        layout.addWidget(
            system_title
        )

        layout.addWidget(
            status
        )

    def _add_navigation_items(
        self,
        layout: QVBoxLayout,
        items: list[tuple[str, str]],
    ) -> None:
        """Create and add navigation buttons."""

        for icon, text in items:

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

            layout.addWidget(
                button
            )

    def _navigation_clicked(
        self,
        destination: str,
    ) -> None:
        """Handle navigation button clicks."""

        self.set_active_page(
            destination
        )

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

            button.style().unpolish(
                button
            )

            button.style().polish(
                button
            )

            button.update()