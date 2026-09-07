from typing import Dict

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QFrame,
    QHBoxLayout,
    QLabel,
    QVBoxLayout,
    QWidget,
)

from integration.integration_manager import (
    ModuleStatus,
)


class IntegrationStatusCard(QFrame):
    """Reusable module connection status card."""

    def __init__(
        self,
        module_name: str,
        parent=None,
    ) -> None:
        super().__init__(parent)

        self.setObjectName(
            "integrationStatusCard"
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

        layout.setSpacing(7)

        header = QHBoxLayout()

        self._name = QLabel(
            module_name.upper()
        )

        self._name.setObjectName(
            "panelTitle"
        )

        header.addWidget(
            self._name
        )

        header.addStretch()

        self._indicator = QLabel(
            "● OFFLINE"
        )

        self._indicator.setObjectName(
            "integrationOffline"
        )

        header.addWidget(
            self._indicator
        )

        layout.addLayout(
            header
        )

        self._events = QLabel(
            "Events received: 0"
        )

        self._events.setObjectName(
            "alertDetailInfo"
        )

        layout.addWidget(
            self._events
        )

        self._last_event = QLabel(
            "Last event: Never"
        )

        self._last_event.setObjectName(
            "alertDetailInfo"
        )

        layout.addWidget(
            self._last_event
        )

    def update_status(
        self,
        status: ModuleStatus,
    ) -> None:
        """Update the card."""

        if status.connected:
            self._indicator.setText(
                "● ONLINE"
            )

            self._indicator.setObjectName(
                "integrationOnline"
            )
        else:
            self._indicator.setText(
                "● OFFLINE"
            )

            self._indicator.setObjectName(
                "integrationOffline"
            )

        self._indicator.style().unpolish(
            self._indicator
        )

        self._indicator.style().polish(
            self._indicator
        )

        self._events.setText(
            f"Events received: "
            f"{status.events_received}"
        )

        self._last_event.setText(
            f"Last event: "
            f"{status.last_event}"
        )


class IntegrationStatusPanel(QWidget):
    """Container for all module connection cards."""

    def __init__(
        self,
        parent=None,
    ) -> None:
        super().__init__(parent)

        self._cards: Dict[
            str,
            IntegrationStatusCard,
        ] = {}

        layout = QHBoxLayout(
            self
        )

        layout.setContentsMargins(
            0,
            0,
            0,
            0,
        )

        layout.setSpacing(12)

        modules = (
            "Packet Interceptor",
            "Physics Engine",
            "Decision Engine",
        )

        for module in modules:
            card = IntegrationStatusCard(
                module
            )

            self._cards[module] = card

            layout.addWidget(
                card,
                1,
            )

    def update_status(
        self,
        statuses: Dict[
            str,
            ModuleStatus,
        ],
    ) -> None:
        """Update all module cards."""

        for module_name, status in statuses.items():
            card = self._cards.get(
                module_name
            )

            if card is not None:
                card.update_status(
                    status
                )