DARK_THEME = """
* {
    font-family: "Segoe UI";
}

QMainWindow,
#mainContainer {
    background-color: #0a0f14;
    color: #d7dee7;
}

#sidebar {
    background-color: #0d131a;
    border-right: 1px solid #202a35;
}

#sidebarLogo {
    color: #e6edf3;
    font-size: 19px;
    font-weight: 800;
    letter-spacing: 2px;
}

#sidebarSubtitle {
    color: #667382;
    font-size: 8px;
    font-weight: 700;
    letter-spacing: 1px;
}

#sidebarSeparator {
    background-color: #202a35;
}

#sidebarSectionTitle {
    color: #586675;
    font-size: 9px;
    font-weight: 700;
    letter-spacing: 1px;
}

#sidebarSystemStatus {
    color: #55c77a;
    font-size: 11px;
}

#navigationButton {
    background-color: transparent;
    color: #8c99a8;
    border: none;
    border-radius: 5px;
    padding: 10px 11px;
    text-align: left;
    font-size: 12px;
}

#navigationButton:hover {
    background-color: #151d26;
    color: #dfe7ef;
}

#navigationButton:pressed {
    background-color: #1b2632;
}

#pageTitle {
    color: #e6edf3;
    font-size: 22px;
    font-weight: 650;
}

#pageSubtitle {
    color: #6f7d8b;
    font-size: 11px;
}

#environmentBadge {
    color: #8d9aa8;
    background-color: #111921;
    border: 1px solid #293540;
    border-radius: 4px;
    padding: 6px 10px;
    font-size: 9px;
    font-weight: 700;
}

#systemBar {
    background-color: #0e1714;
    border: 1px solid #1c3427;
    border-radius: 5px;
}

#protectionStatus {
    color: #55c77a;
    font-size: 10px;
    font-weight: 700;
}

#systemSeparator {
    color: #34423a;
}

#systemInfo,
#heartbeat {
    color: #758292;
    font-size: 10px;
}

#metricCard_normal,
#metricCard_warning,
#metricCard_critical {
    background-color: #10171f;
    border: 1px solid #202b36;
    border-radius: 6px;
}

#metricCard_normal:hover,
#metricCard_warning:hover,
#metricCard_critical:hover {
    border: 1px solid #354352;
}

#metricCard_warning {
    border-left: 3px solid #d6a84f;
}

#metricCard_critical {
    border-left: 3px solid #d95d5d;
}

#metricLabel {
    color: #6e7b89;
    font-size: 9px;
    font-weight: 700;
    letter-spacing: 1px;
}

#metricValue {
    color: #e6edf3;
    font-size: 25px;
    font-weight: 650;
}

#metricDescription {
    color: #596674;
    font-size: 10px;
}

#panel {
    background-color: #10171f;
    border: 1px solid #202b36;
    border-radius: 6px;
}

#panelTitle {
    color: #aab5c0;
    font-size: 10px;
    font-weight: 700;
    letter-spacing: 1px;
}

#tableHeader {
    color: #586674;
    font-size: 8px;
    font-weight: 700;
}

#tableValue {
    color: #9ca8b4;
    font-size: 10px;
}

#statusAllowed,
#decisionAllow {
    color: #55c77a;
    font-size: 9px;
    font-weight: 700;
}

#statusBlocked,
#decisionDrop {
    color: #df6b6b;
    font-size: 9px;
    font-weight: 700;
}

#alertRow,
#decisionRow {
    background-color: #0c131a;
    border: 1px solid #1c2630;
    border-radius: 4px;
}

#severity_critical {
    color: #e56b6b;
    font-size: 8px;
    font-weight: 800;
}

#severity_high {
    color: #d6a84f;
    font-size: 8px;
    font-weight: 800;
}

#severity_medium {
    color: #7ea4c9;
    font-size: 8px;
    font-weight: 800;
}

#alertMessage {
    color: #c9d2dc;
    font-size: 10px;
}

#alertAsset {
    color: #596674;
    font-size: 9px;
}

#decisionTime {
    color: #596674;
    font-family: "Consolas";
    font-size: 9px;
}

#decisionAsset {
    color: #9ca8b4;
    font-size: 9px;
    font-weight: 600;
}

#decisionCommand {
    color: #6f7d8b;
    font-size: 9px;
}
#navigationButton[active="true"] {
    background-color: #18232d;
    color: #e6edf3;
    border-left: 2px solid #55c77a;
}

#navigationButton[active="true"]:hover {
    background-color: #1c2934;
}

#transparentContainer {
    background-color: transparent;
    border: none;
}

#assetName {
    color: #d7dee7;
    font-size: 13px;
    font-weight: 650;
}

#assetType {
    color: #667382;
    font-size: 10px;
}

#assetOnline {
    color: #55c77a;
    font-size: 9px;
    font-weight: 700;
}

#assetWarning {
    color: #d6a84f;
    font-size: 9px;
    font-weight: 700;
}

#logRow {
    background-color: #10171f;
    border: 1px solid #202b36;
    border-radius: 5px;
}

#logTime {
    color: #596674;
    font-family: "Consolas";
    font-size: 9px;
    min-width: 80px;
}

#logCategory {
    color: #7e8c9a;
    font-size: 9px;
    font-weight: 700;
    min-width: 90px;
}

#logMessage {
    color: #aab5c0;
    font-size: 10px;
}

#trafficToolbar {
    background-color: #0f171e;
    border: 1px solid #202b36;
    border-radius: 6px;
}

#monitoringStatus {
    color: #55c77a;
    font-size: 10px;
    font-weight: 700;
    letter-spacing: 0.5px;
}

#monitoringPaused {
    color: #d6a84f;
    font-size: 10px;
    font-weight: 700;
    letter-spacing: 0.5px;
}

#monitoringInfo {
    color: #697786;
    font-size: 10px;
}

#secondaryButton {
    background-color: #151e27;
    color: #aab5c0;
    border: 1px solid #293642;
    border-radius: 4px;
    padding: 7px 12px;
    font-size: 9px;
    font-weight: 700;
}

#secondaryButton:hover {
    background-color: #1b2732;
    color: #e0e7ed;
    border-color: #3a4a58;
}

#secondaryButton:pressed {
    background-color: #10171e;
}

#trafficStatCard {
    background-color: #10171f;
    border: 1px solid #202b36;
    border-radius: 6px;
}

#trafficStatTitle {
    color: #687684;
    font-size: 9px;
    font-weight: 700;
    letter-spacing: 0.8px;
}

#trafficStatValue {
    color: #e2e8ee;
    font-size: 21px;
    font-weight: 650;
}

#trafficTable {
    background-color: #0d141b;
    color: #aeb8c2;
    border: 1px solid #202b36;
    gridline-color: #18232d;
    selection-background-color: #18252f;
    selection-color: #e3e9ee;
}

#trafficTable QHeaderView::section {
    background-color: #111a22;
    color: #657381;
    border: none;
    border-bottom: 1px solid #26323d;
    padding: 9px 7px;
    font-size: 8px;
    font-weight: 700;
}

#trafficTable QTableCornerButton::section {
    background-color: #111a22;
}

#trafficTable QScrollBar:vertical {
    background-color: #0d141b;
    width: 8px;
    margin: 0;
}

#trafficTable QScrollBar::handle:vertical {
    background-color: #2a3743;
    min-height: 25px;
    border-radius: 4px;
}

#trafficTable QScrollBar::add-line:vertical,
#trafficTable QScrollBar::sub-line:vertical {
    height: 0;
}

#trafficTable QScrollBar:horizontal {
    background-color: #0d141b;
    height: 8px;
}

#trafficTable QScrollBar::handle:horizontal {
    background-color: #2a3743;
    border-radius: 4px;
}

#blockedTraffic {
    color: #df6b6b;
    font-weight: 700;
}

#allowedTraffic {
    color: #55c77a;
    font-weight: 700;
}
#assetSearch {
    background-color: #0c131a;
    color: #d5dde5;
    border: 1px solid #293642;
    border-radius: 4px;
    padding: 7px 10px;
    min-height: 18px;
}

#assetSearch:focus {
    border: 1px solid #3c5263;
}

#assetFilter {
    background-color: #0c131a;
    color: #aeb8c2;
    border: 1px solid #293642;
    border-radius: 4px;
    padding: 6px 10px;
    min-width: 100px;
}

#assetFilter:hover {
    border-color: #3c4c59;
}

#assetFilter QAbstractItemView {
    background-color: #111a22;
    color: #aeb8c2;
    border: 1px solid #293642;
    selection-background-color: #1b2a35;
    selection-color: #e2e8ee;
}

#assetTable {
    background-color: #0d141b;
    color: #aeb8c2;
    border: 1px solid #202b36;
    gridline-color: #18232d;
    selection-background-color: #18252f;
    selection-color: #e3e9ee;
}

#assetTable QHeaderView::section {
    background-color: #111a22;
    color: #657381;
    border: none;
    border-bottom: 1px solid #26323d;
    padding: 9px 7px;
    font-size: 8px;
    font-weight: 700;
}
#alertTable {
    background-color: #0d141b;
    color: #aeb8c2;
    border: 1px solid #202b36;
    gridline-color: #18232d;
    selection-background-color: #18252f;
    selection-color: #e3e9ee;
}

#alertTable QHeaderView::section {
    background-color: #111a22;
    color: #657381;
    border: none;
    border-bottom: 1px solid #26323d;
    padding: 9px 7px;
    font-size: 8px;
    font-weight: 700;
}

#alertDetailPanel {
    background-color: #10171f;
    border: 1px solid #202b36;
    border-radius: 6px;
}

#alertDetailTitle {
    color: #dce4eb;
    font-size: 14px;
    font-weight: 650;
    padding-top: 4px;
    padding-bottom: 4px;
}

#alertDetailInfo {
    color: #8f9ca8;
    font-size: 10px;
    line-height: 1.5;
}
"""