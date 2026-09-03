from typing import List

from PyQt6.QtWidgets import (
    QFrame,
    QHBoxLayout,
    QLabel,
    QVBoxLayout,
)

from data.mock_data import DecisionData


class DecisionPanel(QFrame):
    """Displays recent security decisions."""

    def __init__(
        self,
        decisions: List[DecisionData],
        parent=None,
    ) -> None:
        super().__init__(parent)

        self.setObjectName("panel")

        layout = QVBoxLayout(self)
        layout.setContentsMargins(18, 16, 18, 16)
        layout.setSpacing(8)

        title = QLabel("DECISION ENGINE")
        title.setObjectName("panelTitle")

        layout.addWidget(title)

        for decision in decisions:
            layout.addWidget(self._create_decision(decision))

    def _create_decision(self, decision: DecisionData) -> QFrame:
        row = QFrame()
        row.setObjectName("decisionRow")

        layout = QHBoxLayout(row)
        layout.setContentsMargins(8, 7, 8, 7)

        time = QLabel(decision.timestamp)
        time.setObjectName("decisionTime")

        asset = QLabel(decision.asset)
        asset.setObjectName("decisionAsset")

        command = QLabel(decision.command)
        command.setObjectName("decisionCommand")

        result = QLabel(decision.decision)
        result.setObjectName(
            "decisionDrop"
            if decision.decision == "DROP"
            else "decisionAllow"
        )

        layout.addWidget(time)
        layout.addWidget(asset)
        layout.addWidget(command)
        layout.addStretch()
        layout.addWidget(result)

        return row