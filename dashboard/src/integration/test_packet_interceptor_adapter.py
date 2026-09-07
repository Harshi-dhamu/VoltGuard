from integration.application_context import ApplicationContext
from integration.packet_interceptor_adapter import (
    PacketInterceptorAdapter,
)


def main() -> None:
    context = ApplicationContext()

    adapter = PacketInterceptorAdapter(
        context.integration_manager
    )

    packet_event = {
        "event_id": "TEST-PKT-0001",
        "source_module": "packet_interceptor",
        "event_type": "NETWORK_ANOMALY",
        "severity": "CRITICAL",
        "asset": "PUMP_01",
        "message": (
            "Parameter anomaly detected on "
            "PUMP_01: EXCEEDS_MAX_THRESHOLD "
            "(50000 RPM)"
        ),
        "timestamp": "",
        "payload": {
            "transaction_id": 302,
            "function_code": 6,
            "register_address": 1001,
            "command": "SET_SPEED",
            "value": 50000,
            "unit": "RPM",
            "is_suspicious": True,
            "suspicious_reason": (
                "EXCEEDS_MAX_THRESHOLD"
            ),
        },
    }

    success = adapter.publish_event(
        packet_event
    )

    print()
    print("=" * 60)
    print("PACKET INTERCEPTOR INTEGRATION TEST")
    print("=" * 60)

    print(
        "Published:",
        success,
    )

    status = (
        context.integration_manager.get_status()
    )

    print(
        "Total events:",
        status["total_events"],
    )

    print(
        "Last event:",
        status["last_event"],
    )

    print("=" * 60)


if __name__ == "__main__":
    main()