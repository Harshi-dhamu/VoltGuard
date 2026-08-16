import sys

from PyQt6.QtWidgets import QApplication

from main_window import MainWindow
from themes.dark_theme import DARK_THEME


def main() -> None:
    """Application entry point."""
    application = QApplication(sys.argv)

    application.setApplicationName("VoltGuard")
    application.setApplicationDisplayName(
        "VoltGuard OT Security Platform"
    )

    application.setStyleSheet(DARK_THEME)

    window = MainWindow()
    window.show()

    sys.exit(application.exec())


if __name__ == "__main__":
    main()