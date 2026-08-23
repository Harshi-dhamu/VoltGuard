from typing import Dict

from PyQt6.QtWidgets import (
    QHBoxLayout,
    QMainWindow,
    QStackedWidget,
    QWidget,
)

from pages.alerts_page import AlertsPage
from pages.assets_page import AssetsPage
from pages.decisions_page import DecisionsPage
from pages.logs_page import LogsPage
from pages.overview_page import OverviewPage
from pages.traffic_page import TrafficPage
from pages.integration_page import IntegrationPage
from pages.event_monitor_page import EventMonitorPage
from pages.incidents_page import IncidentsPage
from widgets.sidebar import Sidebar
from pages.analytics_page import AnalyticsPage

from integration.application_context import (
    ApplicationContext,
)


class MainWindow(QMainWindow):
    """Main VoltGuard application window."""

    def __init__(self) -> None:
        super().__init__()

        self._app_context = ApplicationContext()

        self.setWindowTitle(
            "VoltGuard | OT Security Platform"
        )

        self.setMinimumSize(
            1280,
            780,
        )

        self._pages: Dict[str, QWidget] = {}

        self._build_ui()
        self._register_pages()
        self._show_page("Overview")

    def _build_ui(self) -> None:
        """Build the application shell."""

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

        self.sidebar = Sidebar()

        self.sidebar.navigation_requested.connect(
            self._show_page
        )

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

    def _register_pages(self) -> None:
        """Create and register all application pages."""

        pages = {
            "Overview": OverviewPage,
            "Traffic Monitor": TrafficPage,
            "Assets": AssetsPage,
            "Alerts": AlertsPage,
            "Decisions": DecisionsPage,
            "Event Logs": LogsPage,
            "Incident Center": IncidentsPage,
            "Security Analytics": AnalyticsPage,
            "System Integration": IntegrationPage,
            "Live Event Monitor": EventMonitorPage,
        }

        for name, page_class in pages.items():

            if page_class is IntegrationPage:

                page = page_class(
                    self._app_context.event_bus,
                    self._app_context.integration_manager,
                )

            elif page_class is EventMonitorPage:

                page = page_class(
                    self._app_context.event_bus,
                )

            else:

                page = page_class()

            self._pages[name] = page

            self.page_stack.addWidget(
                page
            )

    def _show_page(
        self,
        page_name: str,
    ) -> None:
        """Display the requested page."""

        page = self._pages.get(
            page_name
        )

        if page is None:
            return

        self.page_stack.setCurrentWidget(
            page
        )