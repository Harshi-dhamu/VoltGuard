import asyncio
import unittest
from src.interceptor_engine import InterceptorEngine


class TestInterceptorEngine(unittest.IsolatedAsyncioTestCase):
    async def test_interceptor_engine_pipeline(self):
        engine = InterceptorEngine(host="127.0.0.1", port=5020, max_queue_size=10)
        engine.is_running = True
        engine._loop = asyncio.get_running_loop()

        # Start queue worker
        worker = asyncio.create_task(engine._process_queue_worker())

        # Simulated packet dictionary generated from StreamModbusParser
        mock_packet = {
            "transaction_id": 1,
            "protocol_id": 0,
            "length": 6,
            "unit_id": 1,
            "function_code": 6,
            "register_address": 100,
            "value": 1000
        }

        # Test Enqueue
        success = await engine.enqueue_packet(mock_packet)
        self.assertTrue(success)

        # Allow worker processing time
        await asyncio.sleep(0.1)
        self.assertEqual(engine.packet_queue.qsize(), 0)

        # Cleanup
        engine.is_running = False
        worker.cancel()
        await asyncio.gather(worker, return_exceptions=True)