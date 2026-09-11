import threading
from typing import Dict, Any, List
from src.logger import setup_logger

logger = setup_logger()

class PolicyConfigManager:
    """Manages hot-reloadable security policies for real-time packet inspection."""

    _instance = None
    _lock = threading.Lock()

    def __new__(cls):
        with cls._lock:
            if cls._instance is None:
                cls._instance = super(PolicyConfigManager, cls).__new__(cls)
                cls._instance._init_defaults()
            return cls._instance

    def _init_defaults(self):
        """Initializes baseline operational security parameters."""
        self.lock = threading.RLock()
        self.policies: Dict[str, Any] = {
            "max_register_value": 10000,
            "blocked_unit_ids": [],
            "blocked_function_codes": [15, 16],  # Default block on high-impact write commands if flagged
            "enforce_strict_inspection": True
        }

    def reload_policies(self, new_config: Dict[str, Any]):
        """Dynamically updates active security rules at runtime."""
        with self.lock:
            for key, val in new_config.items():
                self.policies[key] = val
            logger.info(f"[POLICY MANAGER] Dynamic policy reload applied. Current config: {self.policies}")

    def get_policy(self, key: str, default: Any = None) -> Any:
        """Retrieves a specific policy value in a thread-safe manner."""
        with self.lock:
            return self.policies.get(key, default)

    def is_value_exceeded(self, value: int) -> bool:
        """Checks if a payload register value breaches the active threshold."""
        with self.lock:
            max_val = self.policies.get("max_register_value", 10000)
            return value > max_val

    def is_unit_blocked(self, unit_id: int) -> bool:
        """Checks if a Unit ID is on the active blacklist."""
        with self.lock:
            return unit_id in self.policies.get("blocked_unit_ids", [])