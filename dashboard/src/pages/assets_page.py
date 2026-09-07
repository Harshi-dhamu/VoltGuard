from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QComboBox,
    QFrame,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

from data.asset_data import (
    AssetData,
    MockAssetProvider,
)

from widgets.asset_table import AssetTable

from .base_page import BasePage


class AssetsPage(BasePage):
    """OT asset inventory and monitoring page."""

    def __init__(
        self,
        parent=None,
    ) -> None:
        super().__init__(
            "Asset Inventory",
            "Industrial asset discovery, health and risk monitoring",
            parent,
        )

        self._provider = (
            MockAssetProvider()
        )

        self._all_assets = (
            self._provider.get_assets()
        )

        self._build_content()

        self._refresh_table()

    def _build_content(self) -> None:
        """Build the asset inventory interface."""

        self._add_summary()
        self._add_filters()
        self._add_asset_table()

    def _add_summary(self) -> None:
        """Add asset statistics."""

        container = QWidget()

        layout = QHBoxLayout(
            container
        )

        layout.setContentsMargins(
            0,
            0,
            0,
            0,
        )

        layout.setSpacing(12)

        total = len(
            self._all_assets
        )

        online = sum(
            asset.status == "ONLINE"
            for asset in self._all_assets
        )

        high_risk = sum(
            asset.risk in {
                "HIGH",
                "CRITICAL",
            }
            for asset in self._all_assets
        )

        offline = sum(
            asset.status == "OFFLINE"
            for asset in self._all_assets
        )

        self._total_value = (
            self._create_stat_card(
                layout,
                "DISCOVERED ASSETS",
                str(total),
            )
        )

        self._online_value = (
            self._create_stat_card(
                layout,
                "ONLINE",
                str(online),
            )
        )

        self._risk_value = (
            self._create_stat_card(
                layout,
                "HIGH RISK",
                str(high_risk),
            )
        )

        self._offline_value = (
            self._create_stat_card(
                layout,
                "OFFLINE",
                str(offline),
            )
        )

        self.add_content(
            container
        )

    def _create_stat_card(
        self,
        layout: QHBoxLayout,
        title: str,
        value: str,
    ) -> QLabel:
        """Create one asset statistic card."""

        frame = QFrame()

        frame.setObjectName(
            "trafficStatCard"
        )

        card_layout = QVBoxLayout(
            frame
        )

        card_layout.setContentsMargins(
            16,
            13,
            16,
            13,
        )

        title_label = QLabel(
            title
        )

        title_label.setObjectName(
            "trafficStatTitle"
        )

        value_label = QLabel(
            value
        )

        value_label.setObjectName(
            "trafficStatValue"
        )

        card_layout.addWidget(
            title_label
        )

        card_layout.addWidget(
            value_label
        )

        layout.addWidget(
            frame,
            1,
        )

        return value_label

    def _add_filters(self) -> None:
        """Add search and filtering controls."""

        frame = QFrame()

        frame.setObjectName(
            "trafficToolbar"
        )

        layout = QHBoxLayout(
            frame
        )

        layout.setContentsMargins(
            14,
            10,
            14,
            10,
        )

        layout.setSpacing(10)

        search_label = QLabel(
            "SEARCH"
        )

        search_label.setObjectName(
            "trafficStatTitle"
        )

        layout.addWidget(
            search_label
        )

        self._search = QLineEdit()

        self._search.setPlaceholderText(
            "Asset name, IP address or ID..."
        )

        self._search.setObjectName(
            "assetSearch"
        )

        self._search.setClearButtonEnabled(
            True
        )

        self._search.textChanged.connect(
            self._refresh_table
        )

        layout.addWidget(
            self._search,
            1,
        )

        type_label = QLabel(
            "TYPE"
        )

        type_label.setObjectName(
            "trafficStatTitle"
        )

        layout.addWidget(
            type_label
        )

        self._type_filter = (
            QComboBox()
        )

        self._type_filter.addItems(
            [
                "ALL",
                "PLC",
                "RTU",
                "HMI",
                "SENSOR",
                "ENGINEERING",
            ]
        )

        self._type_filter.setObjectName(
            "assetFilter"
        )

        self._type_filter.currentTextChanged.connect(
            self._refresh_table
        )

        layout.addWidget(
            self._type_filter
        )

        risk_label = QLabel(
            "RISK"
        )

        risk_label.setObjectName(
            "trafficStatTitle"
        )

        layout.addWidget(
            risk_label
        )

        self._risk_filter = (
            QComboBox()
        )

        self._risk_filter.addItems(
            [
                "ALL",
                "LOW",
                "MEDIUM",
                "HIGH",
                "CRITICAL",
            ]
        )

        self._risk_filter.setObjectName(
            "assetFilter"
        )

        self._risk_filter.currentTextChanged.connect(
            self._refresh_table
        )

        layout.addWidget(
            self._risk_filter
        )

        refresh_button = QPushButton(
            "REFRESH"
        )

        refresh_button.setObjectName(
            "secondaryButton"
        )

        refresh_button.clicked.connect(
            self._refresh_assets
        )

        layout.addWidget(
            refresh_button
        )

        self.add_content(
            frame
        )

    def _add_asset_table(self) -> None:
        """Add the asset inventory table."""

        frame = QFrame()

        frame.setObjectName(
            "panel"
        )

        layout = QVBoxLayout(
            frame
        )

        layout.setContentsMargins(
            14,
            14,
            14,
            14,
        )

        title = QLabel(
            "DISCOVERED INDUSTRIAL ASSETS"
        )

        title.setObjectName(
            "panelTitle"
        )

        layout.addWidget(
            title
        )

        self._table = AssetTable()

        layout.addWidget(
            self._table,
            1,
        )

        self.add_content(
            frame
        )

    def _refresh_assets(self) -> None:
        """Reload assets from the provider."""

        self._all_assets = (
            self._provider.get_assets()
        )

        self._update_summary()
        self._refresh_table()

    def _refresh_table(
        self,
        *_args,
    ) -> None:
        """Apply active filters."""

        search = (
            self._search.text()
            .strip()
            .lower()
            if hasattr(
                self,
                "_search",
            )
            else ""
        )

        selected_type = (
            self._type_filter.currentText()
            if hasattr(
                self,
                "_type_filter",
            )
            else "ALL"
        )

        selected_risk = (
            self._risk_filter.currentText()
            if hasattr(
                self,
                "_risk_filter",
            )
            else "ALL"
        )

        filtered = []

        for asset in self._all_assets:
            matches_search = (
                not search
                or search in asset.name.lower()
                or search in asset.ip_address.lower()
                or search in asset.asset_id.lower()
            )

            matches_type = (
                selected_type == "ALL"
                or asset.asset_type
                == selected_type
            )

            matches_risk = (
                selected_risk == "ALL"
                or asset.risk
                == selected_risk
            )

            if (
                matches_search
                and matches_type
                and matches_risk
            ):
                filtered.append(
                    asset
                )

        self._table.set_assets(
            filtered
        )

    def _update_summary(self) -> None:
        """Update summary statistics."""

        total = len(
            self._all_assets
        )

        online = sum(
            asset.status == "ONLINE"
            for asset in self._all_assets
        )

        high_risk = sum(
            asset.risk in {
                "HIGH",
                "CRITICAL",
            }
            for asset in self._all_assets
        )

        offline = sum(
            asset.status == "OFFLINE"
            for asset in self._all_assets
        )

        self._total_value.setText(
            str(total)
        )

        self._online_value.setText(
            str(online)
        )

        self._risk_value.setText(
            str(high_risk)
        )

        self._offline_value.setText(
            str(offline)
        )