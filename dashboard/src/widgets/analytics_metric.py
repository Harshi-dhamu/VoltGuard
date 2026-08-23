from PyQt6.QtWidgets import (
    QFrame,
    QLabel,
    QVBoxLayout,
)


class AnalyticsMetricCard(QFrame):
    """Reusable analytics metric card."""

    def __init__(
        self,
        title: str,
        value: str,
        description: str,
        parent=None,
    ) -> None:
        super().__init__(parent)

        self.setObjectName(
            "panel"
        )

        layout = QVBoxLayout(
            self
        )

        layout.setContentsMargins(
            16,
            14,
            16,
            14,
        )

        layout.setSpacing(
            4
        )

        title_label = QLabel(
            title
        )

        title_label.setObjectName(
            "sidebarSectionTitle"
        )

        value_label = QLabel(
            value
        )

        value_label.setObjectName(
            "trafficStatValue"
        )

        description_label = QLabel(
            description
        )

        description_label.setObjectName(
            "alertDetailInfo"
        )

        layout.addWidget(
            title_label
        )

        layout.addWidget(
            value_label
        )

        layout.addWidget(
            description_label
        )