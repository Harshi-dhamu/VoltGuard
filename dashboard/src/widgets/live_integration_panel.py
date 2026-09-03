from typing import Dict, Any

from PyQt6.QtWidgets import (
    QFrame,
    QGridLayout,
    QLabel,
    QVBoxLayout,
)


class LiveIntegrationPanel(QFrame):
    """Displays live status of integrated VoltGuard modules."""

    def __init__(
        self,
        parent=None,
    ) -> None:
        super().__init__(parent)

        self.setObjectName("liveIntegrationPanel")

        self._status_labels: Dict[str, QLabel] = {}
        self._event_labels: Dict[str, QLabel] = {}
        self._last_event_labels: Dict[str, QLabel] = {}

        self._build_ui()

    def _build_ui(self) -> None:
        """Build module status cards."""

        layout = QGridLayout(self)

        layout.setContentsMargins(
            12,
            12,
            12,
            12,
        )

        layout.setHorizontalSpacing(10)
        layout.setVerticalSpacing(10)

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

        for index, (key, title) in enumerate(modules):

            card = QFrame()
            card.setObjectName("panel")

            card_layout = QVBoxLayout(card)

            card_layout.setContentsMargins(
                14,
                12,
                14,
                12,
            )

            card_layout.setSpacing(6)

            title_label = QLabel(title)
            title_label.setObjectName("panelTitle")

            status_label = QLabel("● OFFLINE")
            status_label.setObjectName("moduleStatusOffline")

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

            card_layout.addWidget(title_label)
            card_layout.addWidget(status_label)
            card_layout.addWidget(events_label)
            card_layout.addWidget(last_event_label)

            row = index // 3
            column = index % 3

            layout.addWidget(
                card,
                row,
                column,
            )

            self._status_labels[key] = status_label
            self._event_labels[key] = events_label
            self._last_event_labels[key] = last_event_label

    def update_modules(
        self,
        statuses: Dict[str, Any],
    ) -> None:
        """Update module status cards."""

        if not statuses:
            return

        for key, module in statuses.items():

            normalized_key = (
                str(key)
                .strip()
                .lower()
                .replace(" ", "_")
            )

            status_label = self._status_labels.get(
                normalized_key
            )

            event_label = self._event_labels.get(
                normalized_key
            )

            last_event_label = (
                self._last_event_labels.get(
                    normalized_key
                )
            )

            if status_label is None:
                continue

            status = self._get_value(
                module,
                "status",
                "OFFLINE",
            )

            events_received = self._get_value(
                module,
                "events_received",
                0,
            )

            last_event = self._get_value(
                module,
                "last_event",
                None,
            )

            status_text = str(status).upper()

            if status_text in {
                "ONLINE",
                "CONNECTED",
                "ACTIVE",
                "READY",
                "RUNNING",
            }:
                display_status = "● ONLINE"
                status_object = "moduleStatus"

            elif status_text in {
                "WARNING",
                "DEGRADED",
                "PARTIAL",
            }:
                display_status = "● WARNING"
                status_object = "moduleStatusWarning"

            else:
                display_status = "● OFFLINE"
                status_object = "moduleStatusOffline"

            status_label.setText(display_status)
            status_label.setObjectName(status_object)

            event_label.setText(
                f"Events received: {events_received}"
            )

            if last_event is None:
                last_event_text = "None"
            else:
                last_event_text = str(last_event)

            last_event_label.setText(
                f"Last event: {last_event_text}"
            )

            status_label.style().unpolish(
                status_label
            )
            status_label.style().polish(
                status_label
            )
            status_label.update()

    @staticmethod
    def _get_value(
        module: Any,
        attribute: str,
        default: Any,
    ) -> Any:
        """Read a value from either an object or dictionary."""

        if isinstance(module, dict):
            return module.get(
                attribute,
                default,
            )

        return getattr(
            module,
            attribute,
            default,
        )