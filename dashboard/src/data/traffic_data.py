from dataclasses import dataclass
from datetime import datetime
from typing import List
import random


@dataclass(frozen=True)
class PacketData:
    """Represents a network packet observed by VoltGuard."""

    timestamp: str
    source: str
    destination: str
    protocol: str
    source_port: int
    destination_port: int
    packet_type: str
    size: int
    status: str


class MockTrafficProvider:
    """
    Temporary traffic provider used during dashboard development.

    This class will eventually be replaced or adapted to consume
    packets from the Packet Interceptor module.
    """

    SOURCES = [
        "10.10.20.11",
        "10.10.20.12",
        "10.10.20.15",
        "10.10.20.18",
        "10.10.20.21",
    ]

    DESTINATIONS = [
        "10.10.20.25",
        "10.10.20.31",
        "10.10.20.40",
        "10.10.20.50",
    ]

    PROTOCOLS = [
        "Modbus/TCP",
        "TCP",
        "UDP",
    ]

    PACKET_TYPES = [
        "READ",
        "WRITE",
        "STATUS",
        "CONTROL",
    ]

    def generate_packet(self) -> PacketData:
        """Generate one simulated OT network packet."""

        protocol = random.choice(self.PROTOCOLS)

        if protocol == "Modbus/TCP":
            source_port = random.choice([502, 102])
            destination_port = 502
        elif protocol == "TCP":
            source_port = random.randint(1024, 65535)
            destination_port = random.choice(
                [80, 443, 8080]
            )
        else:
            source_port = random.randint(1024, 65535)
            destination_port = random.choice(
                [53, 123, 161]
            )

        packet_type = random.choice(
            self.PACKET_TYPES
        )

        # Most packets are allowed in the simulation.
        status = random.choices(
            ["ALLOWED", "BLOCKED"],
            weights=[90, 10],
            k=1,
        )[0]

        return PacketData(
            timestamp=datetime.now().strftime(
                "%H:%M:%S"
            ),
            source=random.choice(
                self.SOURCES
            ),
            destination=random.choice(
                self.DESTINATIONS
            ),
            protocol=protocol,
            source_port=source_port,
            destination_port=destination_port,
            packet_type=packet_type,
            size=random.randint(
                64,
                1500,
            ),
            status=status,
        )

    def get_initial_packets(
        self,
        count: int = 12,
    ) -> List[PacketData]:
        """Generate initial traffic history."""

        return [
            self.generate_packet()
            for _ in range(count)
        ]