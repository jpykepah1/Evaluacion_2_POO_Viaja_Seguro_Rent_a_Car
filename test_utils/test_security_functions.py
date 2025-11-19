#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test suite for security functions in validador_formatos.py

Tests the following functions:
- validar_entrada_sql(): SQL injection detection
- validar_password_segura(): Strong password policy
- sanitizar_texto(): Text sanitization
"""

import sys
import os
from pathlib import Path

# Add parent directory (MVC) to path
sys.path.insert(0, str(Path(__file__).parent.parent))

import unittest
from utils.validador_formatos import (
    validar_entrada_sql,
    validar_password_segura,
    sanitizar_texto
)


class TestValidarEntradaSQL(unittest.TestCase):
    """Test SQL injection detection"""

    def test_valid_clean_input(self):
        """Valid clean inputs should pass"""
        self.assertTrue(validar_entrada_sql("Juan Perez"))
        self.assertTrue(validar_entrada_sql("12345678"))
        self.assertTrue(validar_entrada_sql("Calle Principal 123"))

    def test_sql_keywords_rejected(self):
        """SQL keywords should be rejected"""
        self.assertFalse(validar_entrada_sql("SELECT * FROM users"))
        self.assertFalse(validar_entrada_sql("INSERT INTO tabla VALUES"))
        self.assertFalse(validar_entrada_sql("UPDATE users SET"))
        self.assertFalse(validar_entrada_sql("DELETE FROM users"))
        self.assertFalse(validar_entrada_sql("DROP TABLE users"))
        self.assertFalse(validar_entrada_sql("UNION SELECT"))

    def test_sql_comments_rejected(self):
        """SQL comments should be rejected"""
        self.assertFalse(validar_entrada_sql("text -- comment"))
        self.assertFalse(validar_entrada_sql("text # comment"))
        self.assertFalse(validar_entrada_sql("text /* comment */"))

    def test_sql_patterns_rejected(self):
        """Common SQL injection patterns should be rejected"""
        self.assertFalse(validar_entrada_sql("admin' OR 1=1 --"))
        self.assertFalse(validar_entrada_sql("admin' AND 1=1"))

    def test_max_length_enforced(self):
        """Entries exceeding max length should be rejected"""
        long_text = "a" * 300
        self.assertFalse(validar_entrada_sql(long_text, max_longitud=255))
        self.assertTrue(validar_entrada_sql(long_text, max_longitud=500))

    def test_empty_input_rejected(self):
        """Empty input should be rejected"""
        self.assertFalse(validar_entrada_sql(""))


class TestValidarPasswordSegura(unittest.TestCase):
    """Test strong password policy"""

    def test_valid_strong_password(self):
        """Valid strong passwords should pass"""
        valid_passes = [
            "SecurePass123!",
            "MyP@ssw0rd",
            "Test$ecure#123",
            "Password!A1",
        ]
        for pwd in valid_passes:
            is_valid, msg = validar_password_segura(pwd)
            self.assertTrue(is_valid, f"Password '{pwd}' should be valid. Message: {msg}")

    def test_password_too_short(self):
        """Passwords less than 8 characters should fail"""
        is_valid, msg = validar_password_segura("Pass1!")
        self.assertFalse(is_valid)
        self.assertIn("8 caracteres", msg)

    def test_password_missing_uppercase(self):
        """Passwords without uppercase should fail"""
        is_valid, msg = validar_password_segura("securepass123!")
        self.assertFalse(is_valid, "Should reject password without uppercase")

    def test_password_missing_lowercase(self):
        """Passwords without lowercase should fail"""
        is_valid, msg = validar_password_segura("SECUREPASS123!")
        self.assertFalse(is_valid, "Should reject password without lowercase")

    def test_password_missing_digit(self):
        """Passwords without digit should fail"""
        is_valid, msg = validar_password_segura("SecurePass!")
        self.assertFalse(is_valid, "Should reject password without digit")

    def test_password_missing_special_char(self):
        """Passwords without special character should fail"""
        is_valid, msg = validar_password_segura("SecurePass123")
        self.assertFalse(is_valid)
        self.assertIn("especial", msg)


class TestSanitizarTexto(unittest.TestCase):
    """Test text sanitization"""

    def test_remove_dangerous_chars(self):
        """Dangerous characters should be removed"""
        result = sanitizar_texto("user'; DROP TABLE; --")
        self.assertNotIn("'", result)
        self.assertNotIn(";", result)
        self.assertNotIn("-", result)
        self.assertEqual(result, "user DROP TABLE")

    def test_preserve_safe_chars(self):
        """Safe characters should be preserved"""
        result = sanitizar_texto("Juan Perez Garcia")
        self.assertEqual(result, "Juan Perez Garcia")

    def test_remove_backslash(self):
        """Backslashes should be removed"""
        result = sanitizar_texto("text\\with\\backslash")
        self.assertNotIn("\\", result)

    def test_remove_hash(self):
        """Hash symbols should be removed"""
        result = sanitizar_texto("text#hash")
        self.assertNotIn("#", result)

    def test_empty_input(self):
        """Empty input should return empty string"""
        self.assertEqual(sanitizar_texto(""), "")


class TestIntegration(unittest.TestCase):
    """Integration tests for security workflow"""

    def test_malicious_input_detection_workflow(self):
        """Simulate malicious input detection in data entry"""
        # Attempt 1: SQL injection in name
        name = "Juan'; DROP TABLE empleado; --"
        is_safe = validar_entrada_sql(name)
        self.assertFalse(is_safe, "SQL injection should be detected")

        # Attempt 2: Valid name but weak password
        name = "Juan Perez"
        password = "weak"
        name_safe = validar_entrada_sql(name)
        pwd_valid, _ = validar_password_segura(password)
        self.assertTrue(name_safe, "Valid name should pass")
        self.assertFalse(pwd_valid, "Weak password should fail")

        # Attempt 3: Valid name and strong password
        name = "Juan Perez"
        password = "SecurePass123!"
        name_safe = validar_entrada_sql(name)
        pwd_valid, _ = validar_password_segura(password)
        self.assertTrue(name_safe, "Valid name should pass")
        self.assertTrue(pwd_valid, "Strong password should pass")


if __name__ == "__main__":
    print("[TEST] Running Security Functions Test Suite\n")
    unittest.main(verbosity=2)
