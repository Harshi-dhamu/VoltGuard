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

        # Fixed width keeps the navigation stable
        # when the application enters fullscreen mode.
        self.setFixedWidth(240)

        self._buttons: Dict[str, QPushButton] = {}

        self._build_ui()

        # Default page
        self.set_active_page("Overview")

    # ==========================================================
    # BUILD UI
    # ==========================================================

    def _build_ui(self) -> None:
        """Build the sidebar navigation."""

        layout = QVBoxLayout(self)

        layout.setContentsMargins(
            14,
            18,
            14,
            18,
        )

        layout.setSpacing(5)

        # ======================================================
        # BRANDING
        # ======================================================

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

        # ======================================================
        # TOP SEPARATOR
        # ======================================================

        separator = QFrame()

        separator.setObjectName(
            "sidebarSeparator"
        )

        separator.setFixedHeight(1)

        layout.addSpacing(14)
        layout.addWidget(separator)
        layout.addSpacing(12)

        # ======================================================
        # MONITORING
        # ======================================================

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

        # ======================================================
        # SECURITY
        # ======================================================

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
            ("◈", "Security Operations"),
            ("◌", "Incident Center"),
            ("⌁", "Security Analytics"),
            ("▰", "Security Policies"),
        ]

        self._add_navigation_items(
            layout,
            security_items,
        )

        # ======================================================
        # INTEGRATION
        # ======================================================

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
            ("◈", "Live Module Integration"),
        ]

        self._add_navigation_items(
            layout,
            integration_items,
        )

        # ======================================================
        # BOTTOM SYSTEM STATUS
        # ======================================================

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

    # ==========================================================
    # NAVIGATION BUTTON CREATION
    # ==========================================================

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

            # Capture the current text correctly.
            button.clicked.connect(
                lambda checked=False,
                item=text:
                self._navigation_clicked(item)
            )

            self._buttons[text] = button

            layout.addWidget(
                button
            )

    # ==========================================================
    # NAVIGATION EVENT
    # ==========================================================

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

    # ==========================================================
    # ACTIVE PAGE
    # ==========================================================

    def set_active_page(
        self,
        page_name: str,
    ) -> None:
        """Update the highlighted navigation item."""

        for name, button in self._buttons.items():

            is_active = (
                name == page_name
            )

            button.setProperty(
                "active",
                is_active,
            )

            # Refresh stylesheet after changing
            # the dynamic property.
            button.style().unpolish(
                button
            )

            button.style().polish(
                button
            )

            button.update()