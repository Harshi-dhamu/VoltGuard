from PyQt6.QtWidgets import (
    QFrame,
    QLabel,
    QVBoxLayout,
)


class SecurityMetricCard(QFrame):
    """Reusable security metric card."""

    def __init__(
        self,
        title: str,
        value: str = "0",
        description: str = "",
        parent=None,
    ) -> None:
        super().__init__(parent)

        self.setObjectName(
            "securityMetricCard"
        )

        layout = QVBoxLayout(self)

        layout.setContentsMargins(
            18,
            16,
            18,
            16,
        )

        layout.setSpacing(6)

        self._title = QLabel(
            title.upper()
        )

        self._title.setObjectName(
            "securityMetricTitle"
        )

        layout.addWidget(
            self._title
        )

        self._value = QLabel(
            value
        )

        self._value.setObjectName(
            "securityMetricValue"
        )

        layout.addWidget(
            self._value
        )

        self._description = QLabel(
            description
        )

        self._description.setObjectName(
            "securityMetricDescription"
        )

        self._description.setWordWrap(
            True
        )

        layout.addWidget(
            self._description
        )

    def set_value(
        self,
        value: str,
    ) -> None:
        """Update the displayed metric."""

        self._value.setText(
            value
        )

    def set_description(
        self,
        description: str,
    ) -> None:
        """Update the metric description."""

        self._description.setText(
            description
        )