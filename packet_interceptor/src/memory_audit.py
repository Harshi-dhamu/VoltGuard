import os
import sys
import gc
from typing import Dict, Any
from src.logger import setup_logger

logger = setup_logger()

class MemoryAuditTracker:
    """Monitors process memory footprint to detect leak anomalies."""

    def __init__(self):
        self.baseline_bytes = self.get_process_memory_bytes()

    @staticmethod
    def get_process_memory_bytes() -> int:
        """Returns current process RAM usage in bytes."""
        try:
            import psutil
            process = psutil.Process(os.getpid())
            return process.memory_info().rss
        except ImportError:
            # Fallback estimation using Python internal object sizing if psutil is unavailable
            return sys.getallocatedblocks() * 64

    def get_memory_delta_mb(self) -> float:
        """Calculates memory growth in MB relative to the initial baseline."""
        gc.collect()  # Trigger garbage collection for precise measurement
        current_bytes = self.get_process_memory_bytes()
        delta_mb = (current_bytes - self.baseline_bytes) / (1024 * 1024)
        return round(delta_mb, 4)

    def audit_report(self) -> Dict[str, Any]:
        """Generates a summary of process memory state."""
        gc.collect()
        current = self.get_process_memory_bytes()
        delta_mb = round((current - self.baseline_bytes) / (1024 * 1024), 4)

        report = {
            "baseline_mb": round(self.baseline_bytes / (1024 * 1024), 2),
            "current_mb": round(current / (1024 * 1024), 2),
            "delta_mb": delta_mb
        }

        logger.info(
            f"[MEMORY AUDIT] Baseline: {report['baseline_mb']} MB | "
            f"Current: {report['current_mb']} MB | Delta: {report['delta_mb']} MB"
        )
        return report