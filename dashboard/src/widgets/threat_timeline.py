from typing import List

from PyQt6.QtWidgets import (
    QFrame,
    QHBoxLayout,
    QLabel,
    QVBoxLayout,
)

from data.analytics_data import ThreatTimelinePoint


class ThreatTimeline(QFrame):
    """Security event timeline widget."""

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
            8
        )

        title = QLabel(
            "24-HOUR THREAT ACTIVITY"
        )

        title.setObjectName(
            "panelTitle"
        )

        self._layout.addWidget(
            title
        )

    def set_data(
        self,
        points: List[ThreatTimelinePoint],
    ) -> None:
        """Populate the threat timeline."""

        maximum = max(
            (
                point.events
                for point in points
            ),
            default=1,
        )

        for point in points:

            row = QFrame()

            row_layout = QHBoxLayout(
                row
            )

            row_layout.setContentsMargins(
                0,
                4,
                0,
                4,
            )

            time_label = QLabel(
                point.timestamp
            )

            time_label.setMinimumWidth(
                55
            )

            time_label.setObjectName(
                "alertDetailInfo"
            )

            bar = QFrame()

            bar.setObjectName(
                "timelineBar"
            )

            bar.setMinimumHeight(
                18
            )

            bar.setMaximumWidth(
                500
            )

            bar_width = max(
                30,
                int(
                    420
                    * point.events
                    / maximum
                ),
            )

            bar.setFixedWidth(
                bar_width
            )

            count_label = QLabel(
                f"{point.events} events"
            )

            count_label.setObjectName(
                "alertDetailInfo"
            )

            row_layout.addWidget(
                time_label
            )

            row_layout.addWidget(
                bar
            )

            row_layout.addWidget(
                count_label
            )

            row_layout.addStretch()

            self._layout.addWidget(
                row
            )