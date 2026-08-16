import logging
from typing import Dict, Any, Callable, Optional
from .models.modbus_packet import NormalizedCommand

logger = logging.getLogger("PhysicsInterface")

class PhysicsEngineInterface:
    """
    Decoupled interface for Dhruti's Physics Engine.
    Dispatches normalized commands without direct dependency on raw packet structures.
    """
    def __init__(self, dispatch_callback: Optional[Callable[[Dict[str, Any]], bool]] = None):
        self.dispatch_callback = dispatch_callback

    def send_to_physics_engine(self, command: NormalizedCommand) -> bool:
        payload = command.to_dict()
        logger.info(f"[INTERCEPTOR -> PHYSICS] Dispatching Command for {command.device_id}")
        
        if self.dispatch_callback:
            return self.dispatch_callback(payload)
        
        # Default mock transmission
        print(f"\n[PHYSICS INTERFACE DISPATCH]\n{command.to_json()}")
        return True