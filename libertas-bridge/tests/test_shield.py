"""Tests für SovereignShield — PII-Sanitisierung und Routing-Logik."""

import sys
import os
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../src"))

from libertas_shield.shield import SovereignShield


class TestSanitize(unittest.TestCase):
    def setUp(self):
        self.shield = SovereignShield()

    def test_email_removed(self):
        result = self.shield.sanitize("Schreib mir an test@example.com bitte.")
        self.assertNotIn("test@example.com", result)
        self.assertIn("[EMAIL]", result)

    def test_phone_removed(self):
        result = self.shield.sanitize("Ruf mich an: +4930123456789")
        self.assertNotIn("+4930123456789", result)
        self.assertIn("[PHONE]", result)

    def test_ip_removed(self):
        result = self.shield.sanitize("Server läuft auf 192.168.1.100")
        self.assertNotIn("192.168.1.100", result)
        self.assertIn("[IP]", result)

    def test_date_removed(self):
        result = self.shield.sanitize("Termin am 05.03.2026")
        self.assertNotIn("05.03.2026", result)
        self.assertIn("[DATE]", result)

    def test_no_pii_unchanged(self):
        text = "Was ist die Hauptstadt von Deutschland?"
        self.assertEqual(self.shield.sanitize(text), text)

    def test_multiple_pii_types(self):
        text = "Kontakt: Max@mail.de, 0301234567, 12.01.2024"
        result = self.shield.sanitize(text)
        self.assertNotIn("Max@mail.de", result)
        self.assertNotIn("0301234567", result)
        self.assertNotIn("12.01.2024", result)


class TestRouting(unittest.TestCase):
    def setUp(self):
        self.shield = SovereignShield()

    def test_low_complexity_uses_local(self):
        result = self.shield.route(3, "Hallo Welt")
        self.assertIn("[LOKAL]", result)

    def test_high_complexity_uses_cloud(self):
        result = self.shield.route(7, "Was ist Quantenphysik?")
        self.assertIn("[CLOUD]", result)

    def test_invalid_complexity_raises(self):
        with self.assertRaises(ValueError):
            self.shield.route(0, "Test")
        with self.assertRaises(ValueError):
            self.shield.route(11, "Test")

    def test_boundary_complexity_4_local(self):
        result = self.shield.route(4, "Test lokal")
        self.assertIn("[LOKAL]", result)

    def test_boundary_complexity_5_cloud(self):
        result = self.shield.route(5, "Test cloud")
        self.assertIn("[CLOUD]", result)


class TestStatus(unittest.TestCase):
    def setUp(self):
        self.shield = SovereignShield()

    def test_status_keys(self):
        s = self.shield.status()
        for key in ["node_id", "mesh_entries", "pii_patterns", "cloud_configured", "log_level"]:
            self.assertIn(key, s)

    def test_pii_patterns_not_empty(self):
        s = self.shield.status()
        self.assertGreater(len(s["pii_patterns"]), 0)


if __name__ == "__main__":
    unittest.main()
