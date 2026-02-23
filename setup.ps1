# LIBERTAS-BRIDGE – Setup für Windows PowerShell

$folder = "libertas-bridge"
New-Item -ItemType Directory -Path $folder -Force | Out-Null
Set-Location $folder

Write-Host "Ordner '$folder' erstellt" -ForegroundColor Green

# config.json
@'
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
'@ | Out-File config.json -Encoding utf8

# requirements.txt
"# Keine externen Abhängigkeiten nötig" | Out-File requirements.txt -Encoding utf8

# src/main.py
New-Item -ItemType Directory src\libertas_shield -Force | Out-Null

@'
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
'@ | Out-File src\main.py -Encoding utf8

# __init__.py
"" | Out-File src\libertas_shield\__init__.py

# local_engine.py
@'
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
'@ | Out-File src\libertas_shield\local_engine.py -Encoding utf8

# cloud_proxy.py
@'
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
'@ | Out-File src\libertas_shield\cloud_proxy.py -Encoding utf8

# mesh_sync.py
@'
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
'@ | Out-File src\libertas_shield\mesh_sync.py -Encoding utf8

# shield.py
@'
import re
from .local_engine import LocalInferenceEngine
from .cloud_proxy import CloudProxy
from .mesh_sync import MeshSync

class SovereignShield:
    def __init__(self):
        self.
