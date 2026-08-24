from typing import Dict

from PyQt6.QtWidgets import (
    QGridLayout,
    QLabel,
    QFrame,
    QVBoxLayout,
)


class LiveIntegrationPanel(QFrame):
    """Displays live status of integrated VoltGuard modules."""

    def __init__(
        self,
        parent=None,
    ) -> None:
        super().__init__(parent)

        self.setObjectName(
            "panel"
        )

        self._status_labels: Dict[
            str,
            QLabel,
        ] = {}

        self._event_labels: Dict[
            str,
            QLabel,
        ] = {}

        self._last_event_labels: Dict[
            str,
            QLabel,
        ] = {}

        self._build_ui()

    def _build_ui(self) -> None:
        """Build module status cards."""

        layout = QGridLayout(
            self
        )

        layout.setContentsMargins(
            12,
            12,
            12,
            12,
        )

        layout.setHorizontalSpacing(
            10
        )

        layout.setVerticalSpacing(
            10
        )

        modules = [
            (
                "packet_interceptor",
                "PACKET INTERCEPTOR",
            ),
            (
                "physics_engine",
                "PHYSICS ENGINE",
            ),
            (
                "decision_engine",
                "DECISION ENGINE",
            ),
        ]

        for index, (
            key,
            title,
        ) in enumerate(modules):

            card = QFrame()

            card.setObjectName(
                "panel"
            )

            card_layout = QVBoxLayout(
                card
            )

            card_layout.setContentsMargins(
                14,
                12,
                14,
                12,
            )

            title_label = QLabel(
                title
            )

            title_label.setObjectName(
                "panelTitle"
            )

            status_label = QLabel(
                "● OFFLINE"
            )

            status_label.setObjectName(
                "sidebarSystemStatus"
            )

            events_label = QLabel(
                "Events received: 0"
            )

            events_label.setObjectName(
                "alertDetailInfo"
            )

            last_event_label = QLabel(
                "Last event: None"
            )

            last_event_label.setObjectName(
                "alertDetailInfo"
            )

            card_layout.addWidget(
                title_label
            )

            card_layout.addWidget(
                status_label
            )

            card_layout.addWidget(
                events_label
            )

            card_layout.addWidget(
                last_event_label
            )

            row = index // 3
            column = index % 3

            layout.addWidget(
                card,
                row,
                column,
            )

            self._status_labels[key] = (
                status_label
            )

            self._event_labels[key] = (
                events_label
            )

            self._last_event_labels[key] = (
                last_event_label
            )

    def update_modules(
        self,
        statuses,
    ) -> None:
        """Update module status cards."""

        for key, module in statuses.items():

            status_label = (
                self._status_labels.get(
                    key
                )
            )

            event_label = (
                self._event_labels.get(
                    key
                )
            )

            last_event_label = (
                self._last_event_labels.get(
                    key
                )
            )

            if status_label is not None:
                status_label.setText(
                    f"● {module.status}"
                )

            if event_label is not None:
                event_label.setText(
                    f"Events received: "
                    f"{module.events_received}"
                )

            if last_event_label is not None:
                last_event_label.setText(
                    f"Last event: "
                    f"{module.last_event}"
                )