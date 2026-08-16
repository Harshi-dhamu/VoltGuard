from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QFrame,
    QGridLayout,
    QLabel,
)

from .base_page import BasePage


class AssetsPage(BasePage):
    """Industrial asset monitoring page."""

    def __init__(self, parent=None) -> None:
        super().__init__(
            "Asset Inventory",
            "Industrial devices currently visible to VoltGuard",
            parent,
        )

        self._build_content()

    def _build_content(self) -> None:
        assets = [
            ("PLC-03", "Programmable Logic Controller", "ONLINE"),
            ("PUMP-01", "Industrial Pump", "ONLINE"),
            ("RTU-07", "Remote Terminal Unit", "ONLINE"),
            ("VALVE-02", "Control Valve", "WARNING"),
            ("TANK-02", "Tank Controller", "ONLINE"),
            ("SENSOR-11", "Pressure Sensor", "ONLINE"),
        ]

        grid = QGridLayout()

        grid.setHorizontalSpacing(14)
        grid.setVerticalSpacing(14)

        for index, asset in enumerate(assets):
            row = index // 3
            column = index % 3

            grid.addWidget(
                self._create_asset_card(*asset),
                row,
                column,
            )

        container = QFrame()
        container.setObjectName(
            "transparentContainer"
        )

        container.setLayout(grid)

        self.add_content(container)
        self.add_stretch()

    def _create_asset_card(
        self,
        name: str,
        asset_type: str,
        status: str,
    ) -> QFrame:
        card = QFrame()
        card.setObjectName("panel")

        layout = QGridLayout(card)

        layout.setContentsMargins(
            16,
            14,
            16,
            14,
        )

        name_label = QLabel(name)
        name_label.setObjectName(
            "assetName"
        )

        type_label = QLabel(asset_type)
        type_label.setObjectName(
            "assetType"
        )

        status_label = QLabel(
            f"● {status}"
        )

        status_label.setObjectName(
            "assetWarning"
            if status == "WARNING"
            else "assetOnline"
        )

        layout.addWidget(
            name_label,
            0,
            0,
        )

        layout.addWidget(
            status_label,
            0,
            1,
            alignment=Qt.AlignmentFlag.AlignRight,
        )

        layout.addWidget(
            type_label,
            1,
            0,
            1,
            2,
        )

        return card