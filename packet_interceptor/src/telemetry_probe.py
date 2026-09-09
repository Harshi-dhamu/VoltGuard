import time
from typing import Dict, Any, List
from src.logger import setup_logger

logger = setup_logger()

class PerformanceMonitor:
    """Tracks latency telemetry across interceptor processing stages."""

    def __init__(self):
        self.latencies_ms: List[float] = []

    def record_latency(self, start_time: float, end_time: float) -> float:
        """Calculates and records duration in milliseconds."""
        duration_ms = (end_time - start_time) * 1000.0
        self.latencies_ms.append(duration_ms)
        return duration_ms

    def get_statistics(self) -> Dict[str, float]:
        """Calculates mean, P95, and P99 latency stats."""
        if not self.latencies_ms:
            return {"count": 0, "avg_ms": 0.0, "p95_ms": 0.0, "p99_ms": 0.0, "max_ms": 0.0}

        sorted_latencies = sorted(self.latencies_ms)
        count = len(sorted_latencies)

        avg_ms = sum(sorted_latencies) / count
        p95_idx = int(count * 0.95)
        p99_idx = int(count * 0.99)

        stats = {
            "count": float(count),
            "avg_ms": round(avg_ms, 4),
            "p95_ms": round(sorted_latencies[min(p95_idx, count - 1)], 4),
            "p99_ms": round(sorted_latencies[min(p99_idx, count - 1)], 4),
            "max_ms": round(sorted_latencies[-1], 4)
        }

        logger.info(
            f"[TELEMETRY PROBE] Packets: {count} | Avg: {stats['avg_ms']}ms | "
            f"P95: {stats['p95_ms']}ms | P99: {stats['p99_ms']}ms | Max: {stats['max_ms']}ms"
        )
        return stats

    def reset(self):
        """Clears recorded latency metrics."""
        self.latencies_ms.clear()