import pytest
import asyncio
from src.event_handler import EventBusIntegrationHandler
from src.event_consumer import AsyncEventConsumer
from scripts.mock_generator import build_modbus_tcp_packet

def test_day25_end_to_end_malicious_drop_and_event_emit():
    """Validates that a malicious high-value payload triggers a DROP action and CRITICAL anomaly event."""
    emitted = []

    def mock_event_bus(event):
        emitted.append(event)

    handler = EventBusIntegrationHandler(event_bus_callback=mock_event_bus)
    
    # Modbus packet exceeding threshold (value = 50000)
    malicious_bytes = build_modbus_tcp_packet(901, 1, 6, 1001, 50000)
    
    event = handler.process_and_emit(malicious_bytes)

    # 1. Verify Event bus payload properties
    assert len(emitted) == 1
    assert event["source_module"] == "packet_interceptor"
    assert event["event_type"] == "NETWORK_ANOMALY"
    assert event["severity"] == "CRITICAL"
    
    # 2. Verify inline decision status
    payload = event.get("payload", {})
    assert payload.get("status") == "DROP" or payload.get("action") == "DROP"

@pytest.mark.asyncio
async def test_day25_async_consumer_throughput():
    """Ensures async consumer ingests events without blocking execution."""
    processed = []

    def handle_event(evt):
        processed.append(evt)

    consumer = AsyncEventConsumer(handler_callback=handle_event)
    worker = asyncio.create_task(consumer.start_consumer())

    test_event = {"event_id": "test-123", "event_type": "NETWORK_ANOMALY"}
    await consumer.enqueue_event(test_event)
    await asyncio.sleep(0.05)  # Let event loop yield to worker

    assert len(processed) == 1
    assert processed[0]["event_id"] == "test-123"

    consumer.stop_consumer()
    await consumer.enqueue_event(None)  # Sentinel to unlock queue
    await worker