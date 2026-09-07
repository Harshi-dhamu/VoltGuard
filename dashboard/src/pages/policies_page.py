from typing import List, Optional

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QComboBox,
    QFrame,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QMessageBox,
    QPushButton,
    QVBoxLayout,
)

from data.policy_data import (
    SecurityPolicy,
    get_security_policies,
)

from widgets.policy_table import PolicyTable

from .base_page import BasePage


class PoliciesPage(BasePage):
    """VoltGuard security policy management center."""

    def __init__(
        self,
        parent=None,
    ) -> None:
        super().__init__(
            "Security Policies",
            "Policy rules controlling monitoring, alerting and response decisions",
            parent,
        )

        self._policies: List[
            SecurityPolicy
        ] = get_security_policies()

        self._build_content()

        self._refresh_table()

    def _build_content(self) -> None:
        """Build the policy management interface."""

        self._add_toolbar()
        self._add_statistics()
        self._add_policy_table()

    def _add_toolbar(self) -> None:
        """Create policy search and controls."""

        frame = QFrame()

        frame.setObjectName(
            "panel"
        )

        layout = QHBoxLayout(
            frame
        )

        layout.setContentsMargins(
            14,
            12,
            14,
            12,
        )

        layout.setSpacing(
            8
        )

        self._search = QLineEdit()

        self._search.setPlaceholderText(
            "Search policy ID, name or condition..."
        )

        self._search.setMinimumHeight(
            36
        )

        self._search.textChanged.connect(
            self._refresh_table
        )

        layout.addWidget(
            self._search,
            1,
        )

        self._severity_filter = QComboBox()

        self._severity_filter.addItems(
            [
                "All Severities",
                "CRITICAL",
                "HIGH",
                "MEDIUM",
                "LOW",
            ]
        )

        self._severity_filter.setMinimumHeight(
            36
        )

        self._severity_filter.currentTextChanged.connect(
            self._refresh_table
        )

        layout.addWidget(
            self._severity_filter
        )

        self._module_filter = QComboBox()

        self._module_filter.addItems(
            [
                "All Modules",
                "Packet Interceptor",
                "Physics Engine",
                "Decision Engine",
            ]
        )

        self._module_filter.setMinimumHeight(
            36
        )

        self._module_filter.currentTextChanged.connect(
            self._refresh_table
        )

        layout.addWidget(
            self._module_filter
        )

        refresh_button = QPushButton(
            "REFRESH"
        )

        refresh_button.setObjectName(
            "secondaryButton"
        )

        refresh_button.setMinimumHeight(
            36
        )

        refresh_button.clicked.connect(
            self._refresh_table
        )

        layout.addWidget(
            refresh_button
        )

        add_button = QPushButton(
            "+ ADD POLICY"
        )

        add_button.setObjectName(
            "primaryButton"
        )

        add_button.setMinimumHeight(
            36
        )

        add_button.clicked.connect(
            self._show_add_policy_message
        )

        layout.addWidget(
            add_button
        )

        self.add_content(
            frame
        )

    def _add_statistics(self) -> None:
        """Add policy statistics."""

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

        self._total_value = QLabel(
            "0"
        )

        self._enabled_value = QLabel(
            "0"
        )

        self._blocking_value = QLabel(
            "0"
        )

        self._critical_value = QLabel(
            "0"
        )

        self._add_stat(
            layout,
            "TOTAL POLICIES",
            self._total_value,
        )

        self._add_stat(
            layout,
            "ACTIVE",
            self._enabled_value,
        )

        self._add_stat(
            layout,
            "BLOCKING RULES",
            self._blocking_value,
        )

        self._add_stat(
            layout,
            "CRITICAL RULES",
            self._critical_value,
        )

        self.add_content(
            frame
        )

    def _add_stat(
        self,
        layout: QHBoxLayout,
        title: str,
        value: QLabel,
    ) -> None:
        """Add a statistic item."""

        container = QFrame()

        container_layout = QVBoxLayout(
            container
        )

        container_layout.setContentsMargins(
            8,
            4,
            8,
            4,
        )

        title_label = QLabel(
            title
        )

        title_label.setObjectName(
            "sidebarSectionTitle"
        )

        value.setObjectName(
            "trafficStatValue"
        )

        container_layout.addWidget(
            title_label
        )

        container_layout.addWidget(
            value
        )

        layout.addWidget(
            container
        )

    def _add_policy_table(self) -> None:
        """Add the main policy table."""

        frame = QFrame()

        frame.setObjectName(
            "panel"
        )

        layout = QVBoxLayout(
            frame
        )

        layout.setContentsMargins(
            10,
            10,
            10,
            10,
        )

        title = QLabel(
            "POLICY RULES"
        )

        title.setObjectName(
            "panelTitle"
        )

        layout.addWidget(
            title
        )

        self._table = PolicyTable()

        self._table.setMinimumHeight(
            430
        )

        self._table.policy_selected.connect(
            self._show_policy_details
        )

        layout.addWidget(
            self._table
        )

        self.add_content(
            frame
        )

    def _refresh_table(
        self,
        *_args,
    ) -> None:
        """Apply filters and refresh the table."""

        search = (
            self._search.text()
            .strip()
            .lower()
        )

        severity = (
            self._severity_filter.currentText()
        )

        module = (
            self._module_filter.currentText()
        )

        filtered = []

        for policy in self._policies:

            searchable = " ".join(
                [
                    policy.policy_id,
                    policy.name,
                    policy.condition,
                ]
            ).lower()

            if search and search not in searchable:
                continue

            if (
                severity != "All Severities"
                and policy.severity != severity
            ):
                continue

            if (
                module != "All Modules"
                and policy.module != module
            ):
                continue

            filtered.append(
                policy
            )

        self._table.set_policies(
            filtered
        )

        self._update_statistics()

    def _update_statistics(self) -> None:
        """Update policy statistics."""

        total = len(
            self._policies
        )

        active = sum(
            policy.enabled
            for policy in self._policies
        )

        blocking = sum(
            policy.action == "BLOCK"
            and policy.enabled
            for policy in self._policies
        )

        critical = sum(
            policy.severity == "CRITICAL"
            and policy.enabled
            for policy in self._policies
        )

        self._total_value.setText(
            str(total)
        )

        self._enabled_value.setText(
            str(active)
        )

        self._blocking_value.setText(
            str(blocking)
        )

        self._critical_value.setText(
            str(critical)
        )

    def _show_policy_details(
        self,
        values,
    ) -> None:
        """Display selected policy details."""

        if not values:
            return

        message = (
            f"Policy: {values[0]}\n\n"
            f"Name: {values[1]}\n"
            f"Module: {values[2]}\n"
            f"Condition: {values[3]}\n"
            f"Severity: {values[4]}\n"
            f"Action: {values[5]}\n"
            f"Status: {values[6]}\n"
            f"Updated: {values[7]}"
        )

        QMessageBox.information(
            self,
            "Policy Details",
            message,
        )

    def _show_add_policy_message(self) -> None:
        """Explain the current policy-management stage."""

        QMessageBox.information(
            self,
            "Policy Management",
            "Policy creation UI is prepared for the next integration stage.\n\n"
            "The current policy set is dashboard-side configuration data. "
            "It can later be connected directly to the Decision Engine.",
        )