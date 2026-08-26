import time
from .models.modbus_packet import ModbusPacket, NormalizedCommand

REGISTER_MAP = {
    1001: {"device_id": "PUMP_01", "command": "SET_SPEED", "unit": "RPM"},
    1002: {"device_id": "VALVE_01", "command": "SET_POSITION", "unit": "%"},
    1003: {"device_id": "PRESSURE_REG_01", "command": "SET_PRESSURE_TARGET", "unit": "PSI"},
}

class CommandNormalizer:
    @staticmethod
    def normalize(packet: ModbusPacket) -> NormalizedCommand:
        mapping = REGISTER_MAP.get(packet.register_address, {
            "device_id": f"DEVICE_UNIT_{packet.unit_id}",
            "command": f"WRITE_REGISTER_{packet.register_address}",
            "unit": "RAW"
        })

        return NormalizedCommand(
            device_id=mapping["device_id"],
            command=mapping["command"],
            value=float(packet.value),
            unit=mapping["unit"],
            transaction_id=packet.transaction_id,
            timestamp=time.time()
        )