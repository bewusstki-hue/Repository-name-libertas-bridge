import re
from datetime import datetime


class LocalInferenceEngine:
    """Offline keyword-based inference engine — no network, no ML model required."""

    _PATTERNS = [
        (r'\bübers[e]?tz', "_translate"),
        (r'\bzusammenfass', "_summarize"),
        (r'\bdiagnos[e]?|fieber|schmerz|symptom', "_medical"),
        (r'(\d+(?:\.\d+)?)\s*([\+\-\*\/])\s*(\d+(?:\.\d+)?)', "_math"),
        (r'\bzeit|uhrzeit|datum|heute|jetzt|sp[äa]t|uhr\b', "_datetime"),
        (r'\bwetter|temperatur|regen|sonnig|schnee', "_weather"),
        (r'\bcode|programmier|python|javascript|funktion|klasse|bug|fehler', "_code_help"),
        (r'\berk[lä]?r|was ist|was bedeutet|wie funktioniert|definier', "_explain"),
        (r'\bpasswort|sicherheit|verschlüssel|hash', "_security"),
    ]

    def process(self, text: str) -> str:
        print("\n⚙️  [LOKAL] Verarbeite offline...")
        lower = text.lower()
        for pattern, handler in self._PATTERNS:
            m = re.search(pattern, lower)
            if m:
                return getattr(self, handler)(text, m)
        return f"✅[LOKAL] Verstanden — für komplexe Anfragen Komplexität ≥ 5 wählen: {text[:60]}"

    # --- Handler ---

    def _translate(self, text: str, _m) -> str:
        german_words = {"der", "die", "das", "und", "ist", "ich", "ein", "eine", "nicht", "mit"}
        tokens = set(text.lower().split())
        if german_words & tokens:
            return "🌍[LOKAL] Erkannt: Deutschsprachige Anfrage — für vollständige Übersetzungen Komplexität ≥ 5 nutzen."
        return "🌍[LOKAL] Übersetzungsanfrage erkannt — Cloud-Modus empfohlen (Komplexität ≥ 5)."

    def _summarize(self, text: str, _m) -> str:
        words = text.split()
        return (
            f"📝[LOKAL] Ihr Text enthält {len(words)} Wörter. "
            "Für eine inhaltliche Zusammenfassung Cloud-Modus nutzen (Komplexität ≥ 5)."
        )

    def _medical(self, text: str, _m) -> str:
        return (
            "🩺[LOKAL] Hinweis: Diese Anwendung ersetzt keine ärztliche Beratung. "
            "Bitte konsultieren Sie bei gesundheitlichen Fragen einen Arzt."
        )

    def _math(self, text: str, m) -> str:
        try:
            a, op, b = float(m.group(1)), m.group(2), float(m.group(3))
            ops = {"+": a + b, "-": a - b, "*": a * b}
            if op == "/" and b != 0:
                ops["/"] = a / b
            elif op == "/" and b == 0:
                return "🔢[LOKAL] Fehler: Division durch null ist nicht definiert."
            result = ops.get(op)
            if result is not None:
                display = int(result) if result == int(result) else result
                return f"🔢[LOKAL] {a} {op} {b} = {display}"
        except (ValueError, AttributeError):
            pass
        return "🔢[LOKAL] Rechenaufgabe erkannt — bitte Aufgabe genauer formulieren."

    def _datetime(self, text: str, _m) -> str:
        now = datetime.now()
        return f"🕐[LOKAL] Jetzt: {now.strftime('%A, %d.%m.%Y  %H:%M:%S')}"

    def _weather(self, text: str, _m) -> str:
        return "🌤️[LOKAL] Keine lokalen Wetterdaten — Cloud-Modus nutzen (Komplexität ≥ 5)."

    def _code_help(self, text: str, _m) -> str:
        return (
            "💻[LOKAL] Code-Anfrage erkannt. Für komplexe Programmieraufgaben "
            "Cloud-Modus empfohlen (Komplexität ≥ 5)."
        )

    def _explain(self, text: str, _m) -> str:
        return (
            "❓[LOKAL] Erklärungsanfrage erkannt. Für detaillierte Antworten "
            "Cloud-Modus empfohlen (Komplexität ≥ 5)."
        )

    def _security(self, text: str, _m) -> str:
        return (
            "🔐[LOKAL] Sicherheitsthema erkannt. Passwörter und sensible Daten "
            "werden niemals an Cloud-Dienste weitergeleitet."
        )
