import re
from .local_engine import LocalInferenceEngine
from .cloud_proxy import CloudProxy
from .mesh_sync import MeshSync

class SovereignShield:
    def __init__(self):
        self.local = LocalInferenceEngine()
        self.cloud = CloudProxy()
        self.mesh = MeshSync()

    def sanitize(self, text: str) -> str:
        return re.sub(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', '[EMAIL]', text)

    def route(self, complexity: int, payload: str):
        if complexity < 5:
            return self.local.process(payload)
        else:
            clean = self.sanitize(payload)
            return self.cloud.process(clean)
