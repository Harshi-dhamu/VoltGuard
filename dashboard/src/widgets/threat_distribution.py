from typing import List
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QFrame,
    QHBoxLayout,
    QLabel,
    QProgressBar,
    QVBoxLayout,
)

from data.analytics_data import ThreatBucket


class ThreatDistribution(QFrame):
    """Reusable threat severity distribution widget."""

    def __init__(
        self,
        parent=None,
    ) -> None:
        super().__init__(parent)

        self.setObjectName(
            "panel"
        )

        self._layout = QVBoxLayout(
            self
        )

        self._layout.setContentsMargins(
            16,
            16,
            16,
            16,
        )

        self._layout.setSpacing(
            12
        )

        title = QLabel(
            "THREAT SEVERITY DISTRIBUTION"
        )

        title.setObjectName(
            "panelTitle"
        )

        self._layout.addWidget(
            title
        )

    def set_data(
        self,
        buckets: List[ThreatBucket],
    ) -> None:
        """Populate the distribution widget."""

        for bucket in buckets:
            row = QFrame()

            row_layout = QHBoxLayout(
                row
            )

            row_layout.setContentsMargins(
                0,
                0,
                0,
                0,
            )

            label = QLabel(
                bucket.label
            )

            label.setMinimumWidth(
                80
            )

            label.setObjectName(
                "alertDetailInfo"
            )

            progress = QProgressBar()

            progress.setRange(
                0,
                max(
                    1,
                    max(
                        item.count
                        for item in buckets
                    ),
                ),
            )

            progress.setValue(
                bucket.count
            )

            progress.setTextVisible(
                False
            )

            progress.setFixedHeight(
                8
            )

            value = QLabel(
                str(bucket.count)
            )

            value.setMinimumWidth(
                35
            )

            value.setAlignment(
                Qt.AlignmentFlag.AlignRight
            )

            row_layout.addWidget(
                label
            )

            row_layout.addWidget(
                progress,
                1,
            )

            row_layout.addWidget(
                value
            )

            self._layout.addWidget(
                row
            )