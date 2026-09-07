from PyQt6.QtWidgets import (
    QLabel,
    QVBoxLayout,
    QWidget,
)


class BasePage(QWidget):
    """Base class for all VoltGuard dashboard pages."""

    def __init__(
        self,
        title: str,
        subtitle: str,
        parent=None,
    ) -> None:
        super().__init__(parent)

        self.page_title = title
        self.page_subtitle = subtitle

        self._build_base_layout()

    def _build_base_layout(self) -> None:
        """Create the standard page layout."""
        self.main_layout = QVBoxLayout(self)

        self.main_layout.setContentsMargins(
            26,
            22,
            26,
            22,
        )

        self.main_layout.setSpacing(18)

        self.title_label = QLabel(self.page_title)
        self.title_label.setObjectName("pageTitle")

        self.subtitle_label = QLabel(
            self.page_subtitle
        )
        self.subtitle_label.setObjectName("pageSubtitle")

        self.main_layout.addWidget(
            self.title_label
        )

        self.main_layout.addWidget(
            self.subtitle_label
        )

    def add_content(self, widget: QWidget) -> None:
        """Add page-specific content."""
        self.main_layout.addWidget(widget)

    def add_stretch(self) -> None:
        """Add stretch at the bottom of the page."""
        self.main_layout.addStretch()