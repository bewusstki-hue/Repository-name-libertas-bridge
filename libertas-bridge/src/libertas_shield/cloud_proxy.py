import hashlib
import json
import os
import urllib.error
import urllib.request
from datetime import datetime


class CloudProxy:
    """Anonymisierter Cloud-Proxy. Sendet sanitisierte Anfragen via HTTP (urllib, keine Abhängigkeiten)."""

    def __init__(self, config: dict):
        self.provider = config.get("cloud_provider", "anthropic")
        self.endpoint = config.get("cloud_endpoint", "https://api.anthropic.com/v1/messages")
        self.model = config.get("cloud_model", "claude-haiku-4-5-20251001")
        env_key = config.get("api_key_env", "ANTHROPIC_API_KEY")
        self.api_key = os.environ.get(env_key, "")

    def process(self, sanitized_text: str) -> str:
        print(f"\n☁️  [CLOUD] Sende anonymisiert...")
        self._log(sanitized_text)
        if self.api_key:
            try:
                return self._call_api(sanitized_text)
            except urllib.error.HTTPError as e:
                body = e.read().decode("utf-8", errors="replace")
                print(f"⚠️  API HTTP-Fehler {e.code}: {body[:120]} — Demo-Modus aktiv")
            except urllib.error.URLError as e:
                print(f"⚠️  Netzwerkfehler: {e.reason} — Demo-Modus aktiv")
            except Exception as e:
                print(f"⚠️  Unbekannter Fehler: {e} — Demo-Modus aktiv")
        else:
            print("ℹ️  Kein API-Key gesetzt (Umgebungsvariable ANTHROPIC_API_KEY). Demo-Modus.")
        return "✅[CLOUD] Verarbeitet (Demo-Modus — kein API-Key konfiguriert)"

    def _call_api(self, text: str) -> str:
        if self.provider == "anthropic":
            return self._call_anthropic(text)
        raise ValueError(f"Unbekannter Provider: {self.provider!r}")

    def _call_anthropic(self, text: str) -> str:
        payload = json.dumps(
            {
                "model": self.model,
                "max_tokens": 512,
                "messages": [{"role": "user", "content": text}],
            }
        ).encode("utf-8")

        req = urllib.request.Request(
            self.endpoint,
            data=payload,
            headers={
                "Content-Type": "application/json",
                "x-api-key": self.api_key,
                "anthropic-version": "2023-06-01",
            },
            method="POST",
        )

        with urllib.request.urlopen(req, timeout=30) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            return f"☁️[CLOUD] {data['content'][0]['text']}"

    def _log(self, text: str):
        h = hashlib.sha256(text.encode()).hexdigest()
        try:
            with open("data_union_log.txt", "a", encoding="utf-8") as f:
                f.write(f"{datetime.now().isoformat()} | {h}\n")
        except OSError:
            pass
