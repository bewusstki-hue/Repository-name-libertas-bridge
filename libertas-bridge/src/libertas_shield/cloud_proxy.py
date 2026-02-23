import time
from datetime import datetime
import hashlib

class CloudProxy:
    def process(self, sanitized_text: str) -> str:
        print(f"\n☁️  [CLOUD] Anonymisiert gesendet: {sanitized_text}")
        self._log(sanitized_text)
        time.sleep(1.5)
        return "✅[CLOUD] Verarbeitet (anonym)"

    def _log(self, text: str):
        h = hashlib.sha256(text.encode()).hexdigest()
        try:
            with open("data_union_log.txt", "a", encoding="utf-8") as f:
                f.write(f"{datetime.now().isoformat()} | {h}\n")
        except:
            pass
