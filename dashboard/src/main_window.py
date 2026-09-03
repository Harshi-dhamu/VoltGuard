from typing import Dict

from PyQt6.QtWidgets import (
    QHBoxLayout,
    QMainWindow,
    QStackedWidget,
    QWidget,
)

from integration.application_context import (
    ApplicationContext,
)

from pages.alerts_page import AlertsPage
from pages.analytics_page import AnalyticsPage
from pages.assets_page import AssetsPage
from pages.decisions_page import DecisionsPage
from pages.event_monitor_page import EventMonitorPage
from pages.incidents_page import IncidentsPage
from pages.integration_page import IntegrationPage
from pages.live_integration_page import LiveIntegrationPage
from pages.logs_page import LogsPage
from pages.overview_page import OverviewPage
from pages.policies_page import PoliciesPage
from pages.security_operations_page import (
    SecurityOperationsPage,
)
from pages.traffic_page import TrafficPage

from widgets.sidebar import Sidebar


class MainWindow(QMainWindow):
    """Main VoltGuard application window."""

    def __init__(self) -> None:
        super().__init__()

        # ======================================================
        # SHARED APPLICATION CONTEXT
        # ======================================================

        # One EventBus and one IntegrationManager are
        # shared by the complete dashboard.
        self._app_context = ApplicationContext()

        self.setWindowTitle(
            "VoltGuard | OT Security Platform"
        )

        self.setMinimumSize(
            1280,
            780,
        )

        self._pages: Dict[
            str,
            QWidget,
        ] = {}

        self._build_ui()

        self._register_pages()

        self._show_page(
            "Overview"
        )

    # ==========================================================
    # UI
    # ==========================================================

    def _build_ui(self) -> None:
        """Build the main application shell."""

        central = QWidget()

        central.setObjectName(
            "mainContainer"
        )

        root_layout = QHBoxLayout(
            central
        )

        root_layout.setContentsMargins(
            0,
            0,
            0,
            0,
        )

        root_layout.setSpacing(
            0
        )

        # ======================================================
        # SIDEBAR
        # ======================================================

        self.sidebar = Sidebar()

        self.sidebar.navigation_requested.connect(
            self._show_page
        )

        # ======================================================
        # PAGE STACK
        # ======================================================

        self.page_stack = QStackedWidget()

        self.page_stack.setObjectName(
            "pageStack"
        )

        root_layout.addWidget(
            self.sidebar
        )

        root_layout.addWidget(
            self.page_stack,
            1,
        )

        self.setCentralWidget(
            central
        )

    # ==========================================================
    # PAGE REGISTRATION
    # ==========================================================

    def _register_pages(self) -> None:
        """Create and register all application pages."""

        pages = {

            # --------------------------------------------------
            # MONITORING
            # --------------------------------------------------

            "Overview": OverviewPage,

            "Traffic Monitor": TrafficPage,

            "Assets": AssetsPage,

            # --------------------------------------------------
            # SECURITY
            # --------------------------------------------------

            "Alerts": AlertsPage,

            "Decisions": DecisionsPage,

            "Event Logs": LogsPage,

            "Security Operations": (
                SecurityOperationsPage
            ),

            "Incident Center": IncidentsPage,

            "Security Analytics": AnalyticsPage,

            "Security Policies": PoliciesPage,

            # --------------------------------------------------
            # INTEGRATION
            # --------------------------------------------------

            "System Integration": IntegrationPage,

            "Live Event Monitor": EventMonitorPage,

            "Live Module Integration": (
                LiveIntegrationPage
            ),
        }

        for name, page_class in pages.items():

            # ==================================================
            # SYSTEM INTEGRATION
            # ==================================================

            if page_class is IntegrationPage:

                page = page_class(
                    self._app_context.event_bus,
                    self._app_context.integration_manager,
                )

            # ==================================================
            # LIVE EVENT MONITOR
            # ==================================================

            elif page_class is EventMonitorPage:

                page = page_class(
                    self._app_context.event_bus,
                )

            # ==================================================
            # LIVE MODULE INTEGRATION
            # ==================================================

            elif page_class is LiveIntegrationPage:

                page = page_class(
                    self._app_context.integration_manager,
                )

            # ==================================================
            # SECURITY OPERATIONS
            # ==================================================

            elif page_class is SecurityOperationsPage:

                page = page_class(
                    self._app_context.event_bus,
                )

            # ==================================================
            # NORMAL PAGES
            # ==================================================

            else:

                page = page_class()

            # --------------------------------------------------
            # Store page
            # --------------------------------------------------

            self._pages[name] = page

            self.page_stack.addWidget(
                page
            )

    # ==========================================================
    # NAVIGATION
    # ==========================================================

    def _show_page(
        self,
        page_name: str,
    ) -> None:
        """Display the requested page."""

        page = self._pages.get(
            page_name
        )

        if page is None:

            print(
                f"[VoltGuard] Page not found: "
                f"{page_name}"
            )

            return

        self.page_stack.setCurrentWidget(
            page
        )

        # Keep sidebar state synchronized.
        self.sidebar.set_active_page(
            page_name
        )

    # ==========================================================
    # DYNAMIC PAGE SUPPORT
    # ==========================================================

    def _add_page(
        self,
        name: str,
        page: QWidget,
    ) -> None:
        """Register a page with the application."""

        self._pages[name] = page

        self.page_stack.addWidget(
            page
        )