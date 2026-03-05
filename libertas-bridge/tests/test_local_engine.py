"""Tests für LocalInferenceEngine."""

import sys
import os
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../src"))

from libertas_shield.local_engine import LocalInferenceEngine


class TestLocalEngine(unittest.TestCase):
    def setUp(self):
        self.engine = LocalInferenceEngine()

    def test_math_addition(self):
        result = self.engine.process("Was ist 5 + 3?")
        self.assertIn("8", result)
        self.assertIn("[LOKAL]", result)

    def test_math_multiplication(self):
        result = self.engine.process("Rechne 6 * 7")
        self.assertIn("42", result)

    def test_math_division_by_zero(self):
        result = self.engine.process("10 / 0")
        self.assertIn("null", result.lower())

    def test_datetime_response(self):
        result = self.engine.process("Wie spät ist es?")
        self.assertIn("[LOKAL]", result)
        self.assertIn("🕐", result)

    def test_medical_response(self):
        result = self.engine.process("Ich habe Fieber und Schmerzen")
        self.assertIn("🩺", result)
        self.assertIn("[LOKAL]", result)

    def test_translate_german(self):
        result = self.engine.process("Übersetze das bitte")
        self.assertIn("🌍", result)

    def test_security_response(self):
        result = self.engine.process("Wie sicher ist mein Passwort?")
        self.assertIn("🔐", result)

    def test_unknown_returns_fallback(self):
        result = self.engine.process("xyzxyz123nonsense")
        self.assertIn("[LOKAL]", result)

    def test_returns_string(self):
        result = self.engine.process("Irgendeine Anfrage")
        self.assertIsInstance(result, str)


if __name__ == "__main__":
    unittest.main()
