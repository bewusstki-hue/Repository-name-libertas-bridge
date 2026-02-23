#!/bin/bash

# LIBERTAS-BRIDGE – Setup für Linux/Mac
folder="libertas-bridge"
mkdir -p "$folder"
cd "$folder"

echo "Ordner '$folder' erstellt"

# config.json
cat > config.json << 'EOF'
{
  "mesh_auto_sync_interval": 30,
  "log_level": "info",
  "pii_patterns": {
    "EMAIL": "\\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\\.[A-Z|a-z]{2,}\\b",
    "PHONE": "(\\+?49|0)[0-9\\s\\-]{8,}",
    "NAME": "\\b[A-Z][a-z]+ [A-Z][a-z]+\\b",
    "DATE": "\\d{2}\\.\\d{2}\\.\\d{4}",
    "GPS": "\\d{1,3}\\.\\d{1,6},\\s*\\d{1,3}\\.\\d{1,6}",
    "IP": "\\b(?:[0-9]{1,3}\\.){3}[0-9]{1,3}\\b"
  }
}
EOF

# requirements.txt
cat > requirements.txt << 'EOF'
# Keine externen Abhängigkeiten nötig
EOF

# src/main.py
mkdir -p src/libertas_shield

cat > src/main.py << 'EOF'
from libertas_shield.shield import SovereignShield

def main():
    shield = SovereignShield()
    print("\n" + "="*60)
    print(" LIBERTAS-BRIDGE v1.1")
    print("="*60)
    print("\nTippe 'exit' zum Beenden\n")
    
    while True:
        try:
            cmd = input(">>> ").strip()
            if cmd.lower() == 'exit':
                break
            comp = int(input("Komplexität (1-10): "))
            result = shield.route(comp, cmd)
            print(f"→ {result}\n")
        except Exception as e:
            print(f"Fehler: {e}\n")

if __name__ == "__main__":
    main()
EOF

# __init__.py
touch src/libertas_shield/__init__.py

# local_engine.py
cat > src/libertas_shield/local_engine.py << 'EOF'
import time

class LocalInferenceEngine:
    def process(self, text: str) -> str:
        print("\n⚙️ [LOKAL] Offline...")
        time.sleep(1)
        lower = text.lower()
        if "übersetz" in lower:
            return "🇩🇪[LOKAL] Übersetzung: Hallo Welt"
        if "zusammenfass" in lower:
            return "📝[LOKAL] Zusammenfassung"
        if "diagnose" in lower or "fieber" in lower:
            return "🩺[LOKAL] Mögliche Ursache – Arzt konsultieren"
        return f"✅[LOKAL] {text[:50]}..."
EOF

# cloud_proxy.py
cat > src/libertas_shield/cloud_proxy.py << 'EOF'
import time, hashlib
from datetime import datetime

class CloudProxy:
    def process(self, sanitized_text: str) -> str:
        print(f"\n☁️ [CLOUD] Anonym: {sanitized_text}")
        self._log(sanitized_text)
        time.sleep(1.5)
        return "✅[CLOUD] Anonym verarbeitet"

    def _log(self, text: str):
        h = hashlib.sha256(text.encode()).hexdigest()
        try:
            with open("data_union_log.txt", "a", encoding="utf-8") as f:
                f.write(f"{datetime.now().isoformat()} | {h}\n")
        except:
            pass
EOF

# mesh_sync.py
cat > src/libertas_shield/mesh_sync.py << 'EOF'
import time, hashlib
from datetime import datetime

class MeshSync:
    def __init__(self):
        self.node_id = str(hash(time.time()))[:8]
        self.knowledge_base = {}
        print(f"🌐 Mesh Node {self.node_id}")

    def add_knowledge(self, topic, content):
        eid = hashlib.md5(f"{topic}{content}".encode()).hexdigest()[:8]
        self.knowledge_base[eid] = {
            "topic": topic,
            "content": content,
            "timestamp": datetime.now().isoformat()
        }
        print(f"🌐 Hinzugefügt: {topic}")
EOF

# shield.py
cat > src/libertas_shield/shield.py << 'EOF'
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
EOF

echo ""
echo "✅ Fertig!"
echo "Starten: cd libertas-bridge && python3 src/main.py"
