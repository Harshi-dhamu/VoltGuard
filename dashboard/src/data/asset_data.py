from dataclasses import dataclass
from typing import List


@dataclass(frozen=True)
class AssetData:
    """Represents an industrial asset monitored by VoltGuard."""

    asset_id: str
    name: str
    asset_type: str
    ip_address: str
    protocol: str
    zone: str
    status: str
    risk: str
    last_seen: str


class MockAssetProvider:
    """Temporary provider for dashboard asset data."""

    def get_assets(self) -> List[AssetData]:
        """Return simulated industrial assets."""

        return [
            AssetData(
                asset_id="PLC-001",
                name="Main Process PLC",
                asset_type="PLC",
                ip_address="10.10.20.11",
                protocol="Modbus/TCP",
                zone="CONTROL",
                status="ONLINE",
                risk="LOW",
                last_seen="12 sec ago",
            ),
            AssetData(
                asset_id="PLC-002",
                name="Packaging PLC",
                asset_type="PLC",
                ip_address="10.10.20.12",
                protocol="Modbus/TCP",
                zone="CONTROL",
                status="ONLINE",
                risk="MEDIUM",
                last_seen="8 sec ago",
            ),
            AssetData(
                asset_id="RTU-001",
                name="Remote Pump RTU",
                asset_type="RTU",
                ip_address="10.10.20.15",
                protocol="DNP3",
                zone="FIELD",
                status="ONLINE",
                risk="LOW",
                last_seen="4 sec ago",
            ),
            AssetData(
                asset_id="HMI-001",
                name="Operator HMI",
                asset_type="HMI",
                ip_address="10.10.20.21",
                protocol="TCP",
                zone="SUPERVISORY",
                status="ONLINE",
                risk="MEDIUM",
                last_seen="15 sec ago",
            ),
            AssetData(
                asset_id="ENG-001",
                name="Engineering Workstation",
                asset_type="ENGINEERING",
                ip_address="10.10.20.30",
                protocol="TCP",
                zone="SUPERVISORY",
                status="ONLINE",
                risk="HIGH",
                last_seen="22 sec ago",
            ),
            AssetData(
                asset_id="SEN-001",
                name="Temperature Sensor",
                asset_type="SENSOR",
                ip_address="10.10.20.41",
                protocol="UDP",
                zone="FIELD",
                status="ONLINE",
                risk="LOW",
                last_seen="5 sec ago",
            ),
            AssetData(
                asset_id="SEN-002",
                name="Pressure Sensor",
                asset_type="SENSOR",
                ip_address="10.10.20.42",
                protocol="UDP",
                zone="FIELD",
                status="OFFLINE",
                risk="MEDIUM",
                last_seen="7 min ago",
            ),
            AssetData(
                asset_id="RTU-002",
                name="Water Treatment RTU",
                asset_type="RTU",
                ip_address="10.10.20.50",
                protocol="DNP3",
                zone="FIELD",
                status="ONLINE",
                risk="HIGH",
                last_seen="31 sec ago",
            ),
        ]