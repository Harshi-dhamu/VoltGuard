from .models.modbus_packet import NormalizedCommand

# Operational thresholds (Physics Engine & Decision Engine make the final call)
SAFETY_THRESHOLDS = {
    "PUMP_01": {"max": 5000.0, "min": 0.0, "unit": "RPM"},
    "VALVE_01": {"max": 100.0, "min": 0.0, "unit": "%"},
    "PRESSURE_REG_01": {"max": 150.0, "min": 0.0, "unit": "PSI"}
}

class SuspiciousTrafficDetector:
    @staticmethod
    def analyze(command: NormalizedCommand) -> NormalizedCommand:
        device = command.device_id
        if device in SAFETY_THRESHOLDS:
            limits = SAFETY_THRESHOLDS[device]
            if command.value > limits["max"]:
                command.is_suspicious = True
                command.suspicious_reason = f"EXCEEDS_MAX_THRESHOLD: {command.value} {command.unit} > {limits['max']} {limits['unit']}"
            elif command.value < limits["min"]:
                command.is_suspicious = True
                command.suspicious_reason = f"BELOW_MIN_THRESHOLD: {command.value} {command.unit} < {limits['min']} {limits['unit']}"

        return command