# LIBERTAS-BRIDGE v1.1

Privacy-First AI Routing Framework — leitet Anfragen intelligent zwischen lokalem Offline-Processing und anonymisierter Cloud-Verarbeitung weiter.

## Architektur

```
Anfrage
  │
  ▼
SovereignShield (Routing-Orchestrator)
  │
  ├── Komplexität 1–4  →  LocalInferenceEngine  (offline, kein Netz)
  │
  └── Komplexität 5–10 →  PII-Sanitisierung → CloudProxy (Anthropic API)
                                                    │
                                              MeshSync (Wissens-Netz)
```

## Features

- **Offline-First**: Einfache Anfragen werden lokal ohne jede Netzwerkverbindung verarbeitet
- **PII-Schutz**: E-Mail, Telefon, Name, Datum, GPS, IP werden vor Cloud-Anfragen automatisch entfernt
- **Echter Cloud-Aufruf**: Über `urllib` (keine Abhängigkeiten) gegen die Anthropic API
- **Mesh-Netz**: Persistentes, lokales Wissens-Netz mit JSON-Export/Import zwischen Nodes
- **Zero Dependencies**: Nur Python-Standardbibliothek

## Installation

```bash
# Linux / macOS
bash setup.sh

# Windows (PowerShell)
.\setup.ps1
```

Oder manuell:

```bash
cd libertas-bridge/src
python main.py
```

## Cloud-Modus aktivieren

Einen Anthropic API-Key als Umgebungsvariable setzen:

```bash
export ANTHROPIC_API_KEY="sk-ant-..."
```

Ohne Key läuft die Anwendung im Demo-Modus (Cloud-Anfragen werden simuliert).

## Verwendung

```
============================================================
  LIBERTAS-BRIDGE v1.1 — Privacy-First AI Routing
============================================================

>>> Wie viel ist 7 * 6?
  Komplexität (1-10): 2
→ 🔢[LOKAL] 7.0 * 6.0 = 42

>>> Erkläre mir Quantenverschränkung
  Komplexität (1-10): 7
→ ☁️[CLOUD] Quantenverschränkung ist ein Phänomen...
```

### Befehle

| Befehl | Funktion |
|---|---|
| `<anfrage>` | Anfrage stellen (Komplexität wird abgefragt) |
| `/status` | System-Status anzeigen |
| `/mesh list` | Alle Mesh-Einträge auflisten |
| `/mesh add` | Wissen hinzufügen |
| `/mesh search <term>` | Im Mesh suchen |
| `/mesh remove <id>` | Eintrag entfernen |
| `/mesh broadcast` | Wissen als JSON exportieren |
| `/mesh import <datei>` | Wissen aus Broadcast-Datei importieren |
| `/help` | Hilfe anzeigen |
| `exit` | Beenden |

## Konfiguration

`libertas-bridge/config.json`:

```json
{
  "mesh_auto_sync_interval": 30,
  "log_level": "info",
  "cloud_provider": "anthropic",
  "cloud_endpoint": "https://api.anthropic.com/v1/messages",
  "cloud_model": "claude-haiku-4-5-20251001",
  "api_key_env": "ANTHROPIC_API_KEY",
  "pii_patterns": { ... }
}
```

## Tests

```bash
cd libertas-bridge
python -m unittest discover -s tests -v
```

34 Tests abgedeckt: Shield-Routing, PII-Sanitisierung, LocalEngine, MeshSync.

## Projektstruktur

```
libertas-bridge/
├── config.json
├── requirements.txt          # Keine Abhängigkeiten
├── src/
│   ├── main.py               # CLI-Einstiegspunkt
│   └── libertas_shield/
│       ├── shield.py         # Routing & PII-Sanitisierung
│       ├── local_engine.py   # Offline Keyword-Verarbeitung
│       ├── cloud_proxy.py    # Anonymisierter Cloud-Aufruf
│       └── mesh_sync.py      # Dezentrales Wissens-Netz
└── tests/
    ├── test_shield.py
    ├── test_local_engine.py
    └── test_mesh_sync.py
```

## Lizenz

GNU Affero General Public License v3 (AGPL-3.0)
