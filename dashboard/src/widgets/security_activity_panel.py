from typing import List

from PyQt6.QtWidgets import (
    QFrame,
    QHBoxLayout,
    QLabel,
    QVBoxLayout,
)


class SecurityActivityPanel(QFrame):
    """Displays the latest security activity."""

    def __init__(
        self,
        parent=None,
    ) -> None:
        super().__init__(parent)

        self.setObjectName(
            "panel"
        )

        # Entries contain QFrame activity rows.
        self._entries: List[QFrame] = []

        self._build_ui()

    def _build_ui(self) -> None:
        """Build activity panel."""

        layout = QVBoxLayout(self)

        layout.setContentsMargins(
            16,
            16,
            16,
            16,
        )

        layout.setSpacing(8)

        title = QLabel(
            "RECENT SECURITY ACTIVITY"
        )

        title.setObjectName(
            "panelTitle"
        )

        layout.addWidget(
            title
        )

        self._container = QVBoxLayout()

        self._container.setSpacing(
            4
        )

        layout.addLayout(
            self._container
        )

        self._show_empty_state()

    def _show_empty_state(self) -> None:
        """Display empty state."""

        label = QLabel(
            "Waiting for security events..."
        )

        label.setObjectName(
            "alertDetailInfo"
        )

        self._container.addWidget(
            label
        )

        # Empty-state QLabel is kept separately.
        self._empty_state = label

    def add_event(
        self,
        event,
    ) -> None:
        """Add an event to the activity stream."""

        # Remove the empty-state message
        # when the first real event arrives.
        if self._empty_state is not None:

            self._empty_state.deleteLater()

            self._empty_state = None

        # Create activity row.
        row = QFrame()

        row.setObjectName(
            "securityActivityRow"
        )

        row_layout = QHBoxLayout(
            row
        )

        row_layout.setContentsMargins(
            8,
            7,
            8,
            7,
        )

        row_layout.setSpacing(
            10
        )

        # Source.
        source = QLabel(
            str(
                event.source_module
            ).upper()
        )

        source.setObjectName(
            "securityActivitySource"
        )

        row_layout.addWidget(
            source
        )

        # Message.
        message = QLabel(
            str(
                event.message
            )
        )

        message.setObjectName(
            "securityActivityMessage"
        )

        message.setWordWrap(
            True
        )

        row_layout.addWidget(
            message,
            1,
        )

        # Severity.
        severity = QLabel(
            str(
                event.severity
            ).upper()
        )

        severity.setObjectName(
            "securityActivitySeverity"
        )

        row_layout.addWidget(
            severity
        )

        # Add newest event at the top.
        self._container.insertWidget(
            0,
            row,
        )

        self._entries.insert(
            0,
            row,
        )

        # Keep only the latest 8 events.
        while len(self._entries) > 8:

            old_entry = self._entries.pop()

            old_entry.deleteLater()