import json
import os
import re

from .local_engine import LocalInferenceEngine
from .cloud_proxy import CloudProxy
from .mesh_sync import MeshSync

_CONFIG_PATH = os.path.join(os.path.dirname(__file__), "../../config.json")


class SovereignShield:
    def __init__(self):
        self.config = self._load_config()
        self.local = LocalInferenceEngine()
        self.cloud = CloudProxy(self.config)
        self.mesh = MeshSync(self.config.get("mesh_auto_sync_interval", 30))
        self._pii_patterns = {
            k: re.compile(v)
            for k, v in self.config.get("pii_patterns", {}).items()
        }

    def _load_config(self) -> dict:
        try:
            path = os.path.abspath(_CONFIG_PATH)
            with open(path, "r", encoding="utf-8") as f:
                cfg = json.load(f)
            print(f"✅ Konfiguration geladen ({len(cfg.get('pii_patterns', {}))} PII-Patterns)")
            return cfg
        except Exception as e:
            print(f"⚠️  Konfigurationsfehler: {e} — Standardwerte aktiv")
            return {}

    def sanitize(self, text: str) -> str:
        result = text
        for label, pattern in self._pii_patterns.items():
            result = pattern.sub(f"[{label}]", result)
        return result

    def route(self, complexity: int, payload: str) -> str:
        if not 1 <= complexity <= 10:
            raise ValueError("Komplexität muss zwischen 1 und 10 liegen")
        if complexity < 5:
            return self.local.process(payload)
        else:
            clean = self.sanitize(payload)
            if clean != payload:
                removed = [label for label, p in self._pii_patterns.items() if p.search(payload)]
                print(f"🔒 PII entfernt: {', '.join(removed)}")
            return self.cloud.process(clean)

    def status(self) -> dict:
        return {
            "node_id": self.mesh.node_id,
            "mesh_entries": len(self.mesh.knowledge_base),
            "pii_patterns": list(self._pii_patterns.keys()),
            "cloud_configured": bool(self.cloud.api_key),
            "log_level": self.config.get("log_level", "info"),
        }
