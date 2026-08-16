from PyQt6.QtCore import pyqtSignal
from PyQt6.QtWidgets import (
    QFrame,
    QLabel,
    QPushButton,
    QVBoxLayout,
    QWidget,
)


class Sidebar(QFrame):
    """Main navigation sidebar."""

    navigation_requested = pyqtSignal(str)

    def __init__(self, parent=None) -> None:
        super().__init__(parent)

        self.setObjectName("sidebar")
        self.setFixedWidth(220)

        self._build_ui()

    def _build_ui(self) -> None:
        layout = QVBoxLayout(self)
        layout.setContentsMargins(14, 18, 14, 18)
        layout.setSpacing(6)

        logo = QLabel("VOLTGUARD")
        logo.setObjectName("sidebarLogo")

        subtitle = QLabel("OT SECURITY PLATFORM")
        subtitle.setObjectName("sidebarSubtitle")

        layout.addWidget(logo)
        layout.addWidget(subtitle)

        separator = QFrame()
        separator.setObjectName("sidebarSeparator")
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
            button = QPushButton(f"{icon}    {text}")
            button.setObjectName("navigationButton")
            button.setCursor(button.cursor())

            button.clicked.connect(
                lambda checked=False, item=text:
                self.navigation_requested.emit(item)
            )

            layout.addWidget(button)

        layout.addStretch()

        system_title = QLabel("SYSTEM")
        system_title.setObjectName("sidebarSectionTitle")

        status = QLabel("●  Monitoring active")
        status.setObjectName("sidebarSystemStatus")

        layout.addWidget(system_title)
        layout.addWidget(status)