from pathlib import Path
import sys


ROOT = Path(__file__).parent
for source_root in (ROOT / "packet_interceptor",):
    source_path = str(source_root)
    if source_path in sys.path:
        sys.path.remove(source_path)
    sys.path.insert(0, source_path)

import src as _packet_interceptor_src

import dashboard.src.data as _dashboard_data
import dashboard.src.integration as _dashboard_integration

sys.modules.setdefault("data", _dashboard_data)
sys.modules.setdefault("integration", _dashboard_integration)
sys.modules.setdefault("src.integration", _dashboard_integration)
setattr(_packet_interceptor_src, "integration", _dashboard_integration)