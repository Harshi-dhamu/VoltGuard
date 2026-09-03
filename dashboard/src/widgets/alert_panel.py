from typing import List

from PyQt6.QtWidgets import (
    QFrame,
    QHBoxLayout,
    QLabel,
    QVBoxLayout,
)

from data.mock_data import AlertData


class AlertPanel(QFrame):
    """Displays active security alerts."""

    def __init__(
        self,
        alerts: List[AlertData],
        parent=None,
    ) -> None:
        super().__init__(parent)

        self.setObjectName("panel")

        layout = QVBoxLayout(self)
        layout.setContentsMargins(18, 16, 18, 16)
        layout.setSpacing(10)

        title = QLabel("ACTIVE SECURITY ALERTS")
        title.setObjectName("panelTitle")

        layout.addWidget(title)

        for alert in alerts:
            layout.addWidget(self._create_alert(alert))

    def _create_alert(self, alert: AlertData) -> QFrame:
        frame = QFrame()
        frame.setObjectName("alertRow")

        layout = QHBoxLayout(frame)
        layout.setContentsMargins(10, 9, 10, 9)

        severity = QLabel(alert.severity)
        severity.setObjectName(
            f"severity_{alert.severity.lower()}"
        )

        details = QVBoxLayout()
        details.setSpacing(2)

        message = QLabel(alert.message)
        message.setObjectName("alertMessage")

        asset = QLabel(f"{alert.asset}  •  {alert.timestamp}")
        asset.setObjectName("alertAsset")

        details.addWidget(message)
        details.addWidget(asset)

        layout.addWidget(severity)
        layout.addLayout(details)

        return frame