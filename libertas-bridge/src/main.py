from libertas_shield.shield import SovereignShield

_HELP = """
Befehle:
  <anfrage>             Anfrage stellen (Komplexität wird abgefragt)
  /status               System-Status anzeigen
  /mesh list            Alle Mesh-Einträge auflisten
  /mesh add             Wissen zum Mesh hinzufügen
  /mesh search <term>   Im Mesh suchen
  /mesh remove <id>     Eintrag aus dem Mesh entfernen
  /mesh broadcast       Wissen als JSON-Datei exportieren
  /mesh import <datei>  Wissen aus einer Broadcast-Datei importieren
  /help                 Diese Hilfe anzeigen
  exit                  Beenden

Komplexität:
  1-4  →  Offline (LocalInferenceEngine, kein Netz, keine Datenweitergabe)
  5-10 →  Cloud (Anthropic API, PII wird automatisch entfernt)
"""


def _print_status(shield: SovereignShield):
    s = shield.status()
    w = 44
    print(f"\n{'='*w}")
    print(f"  Node-ID     : {s['node_id']}")
    print(f"  Mesh-Eintr. : {s['mesh_entries']}")
    print(f"  PII-Muster  : {', '.join(s['pii_patterns'])}")
    cloud_info = "konfiguriert ✅" if s["cloud_configured"] else "Demo-Modus ⚠️  (ANTHROPIC_API_KEY fehlt)"
    print(f"  Cloud       : {cloud_info}")
    print(f"  Log-Level   : {s['log_level']}")
    print(f"{'='*w}\n")


def _mesh_list(shield: SovereignShield):
    entries = shield.mesh.list_topics()
    if not entries:
        print("📭 Keine Einträge im Mesh.")
        return
    print(f"\n{'─'*48}")
    for eid, topic, date in entries:
        print(f"  [{eid}]  {date}  {topic}")
    print(f"{'─'*48}\n")


def _mesh_add(shield: SovereignShield):
    topic = input("  Thema  : ").strip()
    if not topic:
        print("  Abgebrochen — Thema darf nicht leer sein.")
        return
    content = input("  Inhalt : ").strip()
    if not content:
        print("  Abgebrochen — Inhalt darf nicht leer sein.")
        return
    shield.mesh.add_knowledge(topic, content)


def main():
    shield = SovereignShield()
    print("\n" + "=" * 60)
    print("  LIBERTAS-BRIDGE v1.1 — Privacy-First AI Routing")
    print("=" * 60)
    print(_HELP)

    while True:
        try:
            cmd = input(">>> ").strip()
            if not cmd:
                continue

            # --- Beenden ---
            if cmd.lower() == "exit":
                print("Auf Wiedersehen.")
                break

            # --- Slash-Kommandos ---
            elif cmd == "/help":
                print(_HELP)

            elif cmd == "/status":
                _print_status(shield)

            elif cmd == "/mesh list":
                _mesh_list(shield)

            elif cmd == "/mesh add":
                _mesh_add(shield)

            elif cmd.startswith("/mesh search "):
                term = cmd[len("/mesh search "):].strip()
                results = shield.mesh.get_knowledge(term)
                if not results:
                    print(f"🔍 Keine Treffer für '{term}'.")
                else:
                    print(f"\n🔍 {len(results)} Treffer für '{term}':")
                    for eid, entry in results:
                        print(f"  [{eid}] {entry['topic']}: {entry['content'][:60]}")
                    print()

            elif cmd.startswith("/mesh remove "):
                eid = cmd[len("/mesh remove "):].strip()
                shield.mesh.remove_knowledge(eid)

            elif cmd == "/mesh broadcast":
                shield.mesh.broadcast_knowledge()

            elif cmd.startswith("/mesh import "):
                filepath = cmd[len("/mesh import "):].strip()
                shield.mesh.import_broadcast(filepath)

            elif cmd.startswith("/"):
                print(f"  Unbekannter Befehl: {cmd!r}  —  /help für Hilfe")

            # --- Anfrage ---
            else:
                comp_str = input("  Komplexität (1-10): ").strip()
                comp = int(comp_str)
                result = shield.route(comp, cmd)
                print(f"\n→ {result}\n")

        except KeyboardInterrupt:
            print("\n  Unterbrochen. 'exit' zum Beenden.")
        except ValueError as e:
            print(f"  Fehler: {e}\n")
        except Exception as e:
            print(f"  Unerwarteter Fehler: {e}\n")


if __name__ == "__main__":
    main()
