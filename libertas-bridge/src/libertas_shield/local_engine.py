import time

class LocalInferenceEngine:
    def process(self, text: str) -> str:
        print("\n⚙️  [LOKAL] Verarbeite offline...")
        time.sleep(1)
        lower = text.lower()
        if "übersetz" in lower:
            return "🇩🇪[LOKAL] Übersetzung: Hallo Welt"
        if "zusammenfass" in lower:
            return "📝[LOKAL] Kurze Zusammenfassung"
        if "diagnose" in lower or "fieber" in lower:
            return "🩺[LOKAL] Mögliche Ursache - Arzt konsultieren"
        return f"✅[LOKAL] Verarbeitet: {text[:50]}..."
