from PyQt6.QtWidgets import QFrame, QLabel, QVBoxLayout


class MetricCard(QFrame):
    """Reusable security metric card."""

    def __init__(
        self,
        label: str,
        value: str,
        description: str,
        status: str = "normal",
        parent=None,
    ) -> None:
        super().__init__(parent)

        self.setObjectName(f"metricCard_{status}")

        layout = QVBoxLayout(self)
        layout.setContentsMargins(18, 16, 18, 16)
        layout.setSpacing(5)

        label_widget = QLabel(label)
        label_widget.setObjectName("metricLabel")

        value_widget = QLabel(value)
        value_widget.setObjectName("metricValue")

        description_widget = QLabel(description)
        description_widget.setObjectName("metricDescription")

        layout.addWidget(label_widget)
        layout.addWidget(value_widget)
        layout.addWidget(description_widget)
        layout.addStretch()