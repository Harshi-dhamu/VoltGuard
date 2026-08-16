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
"""