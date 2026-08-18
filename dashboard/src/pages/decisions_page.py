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

from data.decision_data import (
    DecisionData,
    MockDecisionProvider,
)

from widgets.decision_table import (
    DecisionTable,
)

from .base_page import BasePage


class DecisionsPage(BasePage):
    """Decision Engine intelligence interface."""

    def __init__(
        self,
        parent=None,
    ) -> None:
        super().__init__(
            "Decision Center",
            "Risk intelligence and automated security decisions",
            parent,
        )

        self._provider = (
            MockDecisionProvider()
        )

        self._all_decisions = (
            self._provider.get_decisions()
        )

        self._selected_decision = None

        self._build_content()

        self._refresh_table()

    def _build_content(self) -> None:
        """Build the decision center."""

        self._add_risk_overview()
        self._add_filters()
        self._add_decision_table()
        self._add_detail_panel()

    def _add_risk_overview(self) -> None:
        """Create risk overview cards."""

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

        risk_score = (
            self._provider.get_risk_score(
                self._all_decisions
            )
        )

        critical = sum(
            decision.severity
            == "CRITICAL"
            for decision in self._all_decisions
        )

        block_count = sum(
            decision.decision
            == "BLOCK"
            for decision in self._all_decisions
        )

        average_confidence = int(
            sum(
                decision.confidence
                for decision
                in self._all_decisions
            )
            / len(
                self._all_decisions
            )
        )

        self._risk_value = (
            self._create_stat_card(
                layout,
                "RISK SCORE",
                f"{risk_score}/100",
            )
        )

        self._critical_value = (
            self._create_stat_card(
                layout,
                "CRITICAL DECISIONS",
                str(critical),
            )
        )

        self._block_value = (
            self._create_stat_card(
                layout,
                "BLOCK ACTIONS",
                str(block_count),
            )
        )

        self._confidence_value = (
            self._create_stat_card(
                layout,
                "AVG CONFIDENCE",
                f"{average_confidence}%",
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
        """Create a statistic card."""

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
        """Create decision filters."""

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

        label = QLabel(
            "SEARCH"
        )

        label.setObjectName(
            "trafficStatTitle"
        )

        layout.addWidget(
            label
        )

        self._search = QLineEdit()

        self._search.setPlaceholderText(
            "Decision, asset or source..."
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

        severity_label = QLabel(
            "SEVERITY"
        )

        severity_label.setObjectName(
            "trafficStatTitle"
        )

        layout.addWidget(
            severity_label
        )

        self._severity_filter = (
            QComboBox()
        )

        self._severity_filter.addItems(
            [
                "ALL",
                "CRITICAL",
                "HIGH",
                "MEDIUM",
                "LOW",
            ]
        )

        self._severity_filter.setObjectName(
            "assetFilter"
        )

        self._severity_filter.currentTextChanged.connect(
            self._refresh_table
        )

        layout.addWidget(
            self._severity_filter
        )

        decision_label = QLabel(
            "DECISION"
        )

        decision_label.setObjectName(
            "trafficStatTitle"
        )

        layout.addWidget(
            decision_label
        )

        self._decision_filter = (
            QComboBox()
        )

        self._decision_filter.addItems(
            [
                "ALL",
                "BLOCK",
                "INVESTIGATE",
                "MONITOR",
                "ALLOW",
            ]
        )

        self._decision_filter.setObjectName(
            "assetFilter"
        )

        self._decision_filter.currentTextChanged.connect(
            self._refresh_table
        )

        layout.addWidget(
            self._decision_filter
        )

        refresh_button = QPushButton(
            "REFRESH"
        )

        refresh_button.setObjectName(
            "secondaryButton"
        )

        refresh_button.clicked.connect(
            self._refresh_decisions
        )

        layout.addWidget(
            refresh_button
        )

        self.add_content(
            frame
        )

    def _add_decision_table(self) -> None:
        """Add decision table."""

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
            "SECURITY DECISIONS"
        )

        title.setObjectName(
            "panelTitle"
        )

        layout.addWidget(
            title
        )

        self._table = DecisionTable()

        self._table.itemSelectionChanged.connect(
            self._show_selected_decision
        )

        layout.addWidget(
            self._table,
            1,
        )

        self.add_content(
            frame
        )

    def _add_detail_panel(self) -> None:
        """Add decision details."""

        frame = QFrame()

        frame.setObjectName(
            "alertDetailPanel"
        )

        layout = QVBoxLayout(
            frame
        )

        layout.setContentsMargins(
            16,
            14,
            16,
            14,
        )

        title = QLabel(
            "DECISION ANALYSIS"
        )

        title.setObjectName(
            "panelTitle"
        )

        layout.addWidget(
            title
        )

        self._detail_title = QLabel(
            "Select a decision"
        )

        self._detail_title.setObjectName(
            "alertDetailTitle"
        )

        layout.addWidget(
            self._detail_title
        )

        self._detail_info = QLabel(
            "Select a decision to view "
            "the reasoning and recommended action."
        )

        self._detail_info.setWordWrap(
            True
        )

        self._detail_info.setObjectName(
            "alertDetailInfo"
        )

        layout.addWidget(
            self._detail_info
        )

        self.add_content(
            frame
        )

    def _refresh_decisions(self) -> None:
        """Reload decisions."""

        self._all_decisions = (
            self._provider.get_decisions()
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

        severity = (
            self._severity_filter.currentText()
            if hasattr(
                self,
                "_severity_filter",
            )
            else "ALL"
        )

        decision_type = (
            self._decision_filter.currentText()
            if hasattr(
                self,
                "_decision_filter",
            )
            else "ALL"
        )

        filtered = []

        for decision in self._all_decisions:

            searchable_text = (
                f"{decision.title} "
                f"{decision.asset} "
                f"{decision.source} "
                f"{decision.decision_id}"
            ).lower()

            matches_search = (
                not search
                or search in searchable_text
            )

            matches_severity = (
                severity == "ALL"
                or decision.severity
                == severity
            )

            matches_decision = (
                decision_type == "ALL"
                or decision.decision
                == decision_type
            )

            if (
                matches_search
                and matches_severity
                and matches_decision
            ):
                filtered.append(
                    decision
                )

        self._table.set_decisions(
            filtered
        )

    def _show_selected_decision(
        self,
    ) -> None:
        """Display selected decision details."""

        row = self._table.currentRow()

        if row < 0:
            return

        item = self._table.item(
            row,
            1,
        )

        if item is None:
            return

        decision_value = (
            item.text()
        )

        asset_item = self._table.item(
            row,
            4,
        )

        if asset_item is None:
            return

        asset_name = (
            asset_item.text()
        )

        selected = next(
            (
                decision
                for decision
                in self._all_decisions
                if decision.decision
                == decision_value
                and decision.asset
                == asset_name
            ),
            None,
        )

        if selected is None:
            return

        self._selected_decision = (
            selected
        )

        self._detail_title.setText(
            f"{selected.decision}  |  "
            f"{selected.title}"
        )

        details = (
            f"<b>Decision ID:</b> "
            f"{selected.decision_id}<br>"
            f"<b>Severity:</b> "
            f"{selected.severity}<br>"
            f"<b>Confidence:</b> "
            f"{selected.confidence}%<br>"
            f"<b>Asset:</b> "
            f"{selected.asset}<br>"
            f"<b>Source:</b> "
            f"{selected.source}<br>"
            f"<b>Category:</b> "
            f"{selected.category}<br><br>"
            f"<b>Reason:</b> "
            f"{selected.reason}<br><br>"
            f"<b>Recommended Action:</b> "
            f"{selected.recommended_action}"
        )

        self._detail_info.setText(
            details
        )

    def _update_summary(self) -> None:
        """Update risk summary."""

        risk_score = (
            self._provider.get_risk_score(
                self._all_decisions
            )
        )

        critical = sum(
            decision.severity
            == "CRITICAL"
            for decision in self._all_decisions
        )

        block_count = sum(
            decision.decision
            == "BLOCK"
            for decision in self._all_decisions
        )

        average_confidence = int(
            sum(
                decision.confidence
                for decision
                in self._all_decisions
            )
            / len(
                self._all_decisions
            )
        )

        self._risk_value.setText(
            f"{risk_score}/100"
        )

        self._critical_value.setText(
            str(critical)
        )

        self._block_value.setText(
            str(block_count)
        )

        self._confidence_value.setText(
            f"{average_confidence}%"
        )