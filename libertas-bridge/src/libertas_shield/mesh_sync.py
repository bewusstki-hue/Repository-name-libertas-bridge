import hashlib
import json
import os
import time
from datetime import datetime

_MESH_FILE = "mesh_knowledge.json"


class MeshSync:
    """Dezentrales Wissens-Netz mit JSON-Persistenz und Datei-basiertem Broadcast."""

    def __init__(self, sync_interval: int = 30):
        self.node_id = hashlib.sha256(str(time.time()).encode()).hexdigest()[:8]
        self.sync_interval = sync_interval
        self.knowledge_base: dict = self._load()
        print(f"🌐 Mesh Node {self.node_id} ({len(self.knowledge_base)} Einträge geladen)")

    # --- Persistenz ---

    def _load(self) -> dict:
        if os.path.exists(_MESH_FILE):
            try:
                with open(_MESH_FILE, "r", encoding="utf-8") as f:
                    return json.load(f)
            except (OSError, json.JSONDecodeError):
                pass
        return {}

    def _save(self):
        try:
            with open(_MESH_FILE, "w", encoding="utf-8") as f:
                json.dump(self.knowledge_base, f, ensure_ascii=False, indent=2)
        except OSError as e:
            print(f"⚠️  Mesh-Speicherfehler: {e}")

    # --- Wissen verwalten ---

    def add_knowledge(self, topic: str, content: str) -> str:
        eid = hashlib.md5(f"{topic}{content}".encode()).hexdigest()[:8]
        self.knowledge_base[eid] = {
            "topic": topic,
            "content": content,
            "node": self.node_id,
            "timestamp": datetime.now().isoformat(),
        }
        self._save()
        print(f"🌐 Hinzugefügt: [{eid}] {topic}")
        return eid

    def get_knowledge(self, query: str) -> list:
        """Sucht nach Einträgen, deren Thema oder Inhalt den Suchbegriff enthält."""
        q = query.lower()
        return [
            (eid, entry)
            for eid, entry in self.knowledge_base.items()
            if q in entry["topic"].lower() or q in entry["content"].lower()
        ]

    def list_topics(self) -> list:
        return [
            (eid, e["topic"], e["timestamp"][:10])
            for eid, e in self.knowledge_base.items()
        ]

    def remove_knowledge(self, eid: str) -> bool:
        if eid in self.knowledge_base:
            del self.knowledge_base[eid]
            self._save()
            print(f"🗑️  Eintrag {eid} entfernt.")
            return True
        print(f"⚠️  Eintrag {eid} nicht gefunden.")
        return False

    # --- Broadcast / Import ---

    def broadcast_knowledge(self) -> str | None:
        """Exportiert alle Einträge als JSON-Datei (Datei-basierter Broadcast)."""
        count = len(self.knowledge_base)
        if count == 0:
            print("📡 Keine Einträge zum Senden.")
            return None
        export_file = f"mesh_broadcast_{self.node_id}_{int(time.time())}.json"
        try:
            with open(export_file, "w", encoding="utf-8") as f:
                json.dump(
                    {
                        "node": self.node_id,
                        "exported": datetime.now().isoformat(),
                        "entries": self.knowledge_base,
                    },
                    f,
                    ensure_ascii=False,
                    indent=2,
                )
            print(f"📡 {count} Eintrag/Einträge exportiert → {export_file}")
            return export_file
        except OSError as e:
            print(f"⚠️  Broadcast-Fehler: {e}")
            return None

    def import_broadcast(self, filepath: str) -> int:
        """Importiert Einträge aus einer Broadcast-Datei eines anderen Nodes."""
        try:
            with open(filepath, "r", encoding="utf-8") as f:
                data = json.load(f)
            imported = 0
            for eid, entry in data.get("entries", {}).items():
                if eid not in self.knowledge_base:
                    self.knowledge_base[eid] = entry
                    imported += 1
            self._save()
            print(f"📥 {imported} neue Eintrag/Einträge importiert von Node {data.get('node', '?')}")
            return imported
        except (OSError, json.JSONDecodeError) as e:
            print(f"⚠️  Import-Fehler: {e}")
            return 0
