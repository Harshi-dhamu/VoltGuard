from typing import List

from PyQt6.QtWidgets import (
    QFrame,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QVBoxLayout,
)

from data.analytics_data import (
    AssetThreat,
    get_asset_threats,
    get_metrics,
    get_threat_distribution,
    get_timeline,
)

from widgets.analytics_metric import AnalyticsMetricCard
from widgets.threat_distribution import ThreatDistribution
from widgets.threat_timeline import ThreatTimeline

from .base_page import BasePage


class AnalyticsPage(BasePage):
    """VoltGuard security analytics center."""

    def __init__(
        self,
        parent=None,
    ) -> None:
        super().__init__(
            "Security Analytics",
            "Threat intelligence, activity trends and operational risk",
            parent,
        )

        self._build_content()

        self._load_data()

    def _build_content(self) -> None:
        """Build analytics interface."""

        self._add_header()
        self._add_metrics()
        self._add_analysis_panels()
        self._add_asset_panel()

    def _add_header(self) -> None:
        """Add analytics control header."""

        frame = QFrame()

        frame.setObjectName(
            "panel"
        )

        layout = QHBoxLayout(
            frame
        )

        layout.setContentsMargins(
            16,
            12,
            16,
            12,
        )

        label = QLabel(
            "SECURITY POSTURE"
        )

        label.setObjectName(
            "panelTitle"
        )

        layout.addWidget(
            label
        )

        layout.addStretch()

        self._refresh_button = QPushButton(
            "REFRESH ANALYTICS"
        )

        self._refresh_button.setObjectName(
            "secondaryButton"
        )

        self._refresh_button.clicked.connect(
            self._load_data
        )

        layout.addWidget(
            self._refresh_button
        )

        self.add_content(
            frame
        )

    def _add_metrics(self) -> None:
        """Add analytics metric cards."""

        container = QFrame()

        layout = QHBoxLayout(
            container
        )

        layout.setContentsMargins(
            0,
            0,
            0,
            0,
        )

        layout.setSpacing(
            12
        )

        self._metric_layout = layout

        self.add_content(
            container
        )

    def _add_analysis_panels(self) -> None:
        """Add threat distribution and timeline."""

        container = QFrame()

        layout = QHBoxLayout(
            container
        )

        layout.setContentsMargins(
            0,
            0,
            0,
            0,
        )

        layout.setSpacing(
            12
        )

        self._distribution = (
            ThreatDistribution()
        )

        self._timeline = (
            ThreatTimeline()
        )

        layout.addWidget(
            self._distribution,
            1,
        )

        layout.addWidget(
            self._timeline,
            1,
        )

        self.add_content(
            container
        )

    def _add_asset_panel(self) -> None:
        """Add affected asset ranking."""

        frame = QFrame()

        frame.setObjectName(
            "panel"
        )

        layout = QVBoxLayout(
            frame
        )

        layout.setContentsMargins(
            16,
            16,
            16,
            16,
        )

        title = QLabel(
            "MOST AFFECTED ASSETS"
        )

        title.setObjectName(
            "panelTitle"
        )

        layout.addWidget(
            title
        )

        self._asset_layout = layout

        self.add_content(
            frame
        )

    def _load_data(self) -> None:
        """Load analytics data."""

        self._clear_metrics()
        self._clear_assets()

        metrics = get_metrics()

        for metric in metrics:

            card = AnalyticsMetricCard(
                metric.name,
                metric.value,
                metric.description,
            )

            self._metric_layout.addWidget(
                card
            )

        self._distribution.set_data(
            get_threat_distribution()
        )

        self._timeline.set_data(
            get_timeline()
        )

        self._load_assets(
            get_asset_threats()
        )

    def _clear_metrics(self) -> None:
        """Remove existing metric cards."""

        while self._metric_layout.count():

            item = (
                self._metric_layout.takeAt(
                    0
                )
            )

            widget = item.widget()

            if widget is not None:
                widget.deleteLater()

    def _clear_assets(self) -> None:
        """Remove existing asset rows."""

        while self._asset_layout.count() > 1:

            item = (
                self._asset_layout.takeAt(
                    1
                )
            )

            widget = item.widget()

            if widget is not None:
                widget.deleteLater()

    def _load_assets(
        self,
        assets: List[AssetThreat],
    ) -> None:
        """Display affected asset ranking."""

        for index, asset in enumerate(
            assets,
            start=1,
        ):

            row = QFrame()

            row_layout = QHBoxLayout(
                row
            )

            row_layout.setContentsMargins(
                8,
                6,
                8,
                6,
            )

            rank = QLabel(
                f"{index:02d}"
            )

            rank.setMinimumWidth(
                35
            )

            rank.setObjectName(
                "alertDetailInfo"
            )

            asset_label = QLabel(
                asset.asset
            )

            asset_label.setMinimumWidth(
                140
            )

            count_label = QLabel(
                f"{asset.incidents} incidents"
            )

            count_label.setObjectName(
                "alertDetailInfo"
            )

            severity = QLabel(
                asset.severity
            )

            severity.setMinimumWidth(
                90
            )

            row_layout.addWidget(
                rank
            )

            row_layout.addWidget(
                asset_label
            )

            row_layout.addWidget(
                count_label
            )

            row_layout.addStretch()

            row_layout.addWidget(
                severity
            )

            self._asset_layout.addWidget(
                row
            )