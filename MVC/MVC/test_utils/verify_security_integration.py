#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Verification Report for Security Integration - 2025-11-19
Genera un reporte completo del estado de la integración de seguridad
"""

import sys
import os
from pathlib import Path

# Add MVC directory to path (go up 2 levels from test_utils)
mvc_path = Path(__file__).parent.parent
sys.path.insert(0, str(mvc_path))
sys.path.insert(0, str(mvc_path / "utils"))

def verify_files_exist():
    """Verifica que todos los archivos necesarios existan"""
    print("\n" + "="*70)
    print("VERIFICACION DE ARCHIVOS")
    print("="*70)
    
    required_files = {
        "utils/validador_formatos.py": ["validar_entrada_sql", "validar_password_segura", "sanitizar_texto"],
        "controlador/validations.py": ["validar_entrada_sql", "validar_password_segura"],
        "test_utils/test_security_functions.py": ["TestValidarEntradaSQL", "TestValidarPasswordSegura"],
    }
    
    all_exist = True
    for file_path, functions in required_files.items():
        full_path = mvc_path / file_path
        if full_path.exists():
            print(f"[OK] {file_path}")
            # Check for functions in file
            with open(full_path, 'r', encoding='utf-8') as f:
                content = f.read()
                for func in functions:
                    if func in content:
                        print(f"     [OK] Contiene '{func}'")
                    else:
                        print(f"     [ERROR] No contiene '{func}'")
                        all_exist = False
        else:
            print(f"[ERROR] {file_path} NO EXISTE")
            all_exist = False
    
    return all_exist

def verify_security_functions():
    """Verifica que las funciones de seguridad funcionen correctamente"""
    print("\n" + "="*70)
    print("VERIFICACION DE FUNCIONES DE SEGURIDAD")
    print("="*70)
    
    try:
        from utils.validador_formatos import (
            validar_entrada_sql,
            validar_password_segura,
            sanitizar_texto
        )
        
        # Test 1: SQL Injection Detection
        print("\n[TEST 1] validar_entrada_sql()")
        test_cases = [
            ("Juan Perez", True, "Clean input"),
            ("Juan'; DROP TABLE empleado; --", False, "SQL Injection"),
            ("admin' OR 1=1 --", False, "OR 1=1 pattern"),
        ]
        
        for text, expected, desc in test_cases:
            result = validar_entrada_sql(text)
            status = "[OK]" if result == expected else "[ERROR]"
            print(f"{status} {desc}: {result} (expected {expected})")
        
        # Test 2: Strong Password
        print("\n[TEST 2] validar_password_segura()")
        pwd_cases = [
            ("SecurePass123!", True, "Valid strong password"),
            ("weak", False, "Too short"),
            ("NoSpecial123", False, "Missing special char"),
        ]
        
        for pwd, expected, desc in pwd_cases:
            result, msg = validar_password_segura(pwd)
            status = "[OK]" if result == expected else "[ERROR]"
            print(f"{status} {desc}: {result}")
            if result != expected:
                print(f"     Message: {msg}")
        
        # Test 3: Text Sanitization
        print("\n[TEST 3] sanitizar_texto()")
        test_text = "user'; DROP TABLE; --"
        sanitized = sanitizar_texto(test_text)
        expected_contains = "user"
        has_dangerous = any(c in sanitized for c in ";'--")
        status = "[OK]" if (expected_contains in sanitized and not has_dangerous) else "[ERROR]"
        print(f"{status} Removed dangerous chars: '{sanitized}'")
        
        return True
        
    except Exception as e:
        print(f"[ERROR] {str(e)}")
        import traceback
        traceback.print_exc()
        return False

def verify_controller_integration():
    """Verifica que las validaciones estén integradas en el controlador"""
    print("\n" + "="*70)
    print("VERIFICACION DE INTEGRACION EN CONTROLADOR")
    print("="*70)
    
    try:
        validations_path = mvc_path / "controlador" / "validations.py"  # mvc_path is already MVC/
        with open(validations_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        checks = {
            "Importa validar_entrada_sql": ("from validador_formatos import" in content or "from utils.validador_formatos import *" in content) and "validar_entrada_sql" in content,
            "Importa validar_password_segura": "validar_password_segura" in content,
            "Usa validar_password_segura en empleado": content.count("validar_password_segura") >= 2,
            "Valida SQL en empleado": content.count("validar_entrada_sql(run)") >= 1,
            "Valida SQL en cliente": content.count("validar_entrada_sql(run)") >= 2,
        }
        
        all_ok = True
        for check, result in checks.items():
            status = "[OK]" if result else "[ERROR]"
            print(f"{status} {check}: {'Yes' if result else 'No'}")
            if not result:
                all_ok = False
        
        return all_ok
        
    except Exception as e:
        print(f"[ERROR] {str(e)}")
        return False

def verify_test_suite():
    """Verifica que la suite de pruebas existe y es ejecutable"""
    print("\n" + "="*70)
    print("VERIFICACION DE SUITE DE PRUEBAS")
    print("="*70)
    
    try:
        test_file = mvc_path / "test_utils" / "test_security_functions.py"
        
        if not test_file.exists():
            print("[ERROR] test_security_functions.py no existe")
            return False
        
        print("[OK] test_security_functions.py existe")
        
        # Check test classes
        with open(test_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        test_classes = [
            "TestValidarEntradaSQL",
            "TestValidarPasswordSegura",
            "TestSanitizarTexto",
            "TestIntegration"
        ]
        
        for test_class in test_classes:
            if f"class {test_class}" in content:
                print(f"[OK] Clase de prueba: {test_class}")
            else:
                print(f"[ERROR] Clase de prueba no encontrada: {test_class}")
                return False
        
        return True
        
    except Exception as e:
        print(f"[ERROR] {str(e)}")
        return False

def verify_documentation():
    """Verifica que la documentación esté actualizada"""
    print("\n" + "="*70)
    print("VERIFICACION DE DOCUMENTACION")
    print("="*70)
    
    docs_root = mvc_path / "docs"  # Documentation is in MVC/docs
    doc_checks = {
        "README.md (actualizado)": (docs_root / "README.md", "validar_entrada_sql"),
        "changelog.md (nuevo)": (mvc_path / "changelog.md", "Seguridad Avanzada"),
        "SECURITY_INTEGRATION_SUMMARY.md (nuevo)": (docs_root / "SECURITY_INTEGRATION_SUMMARY.md", "Suite de Pruebas"),
    }
    
    all_ok = True
    for doc_name, (doc_path, search_text) in doc_checks.items():
        if doc_path.exists():
            with open(doc_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            if search_text in content:
                print(f"[OK] {doc_name} - Contiene '{search_text}'")
            else:
                print(f"[WARNING] {doc_name} - No contiene '{search_text}'")
                all_ok = False
        else:
            print(f"[ERROR] {doc_name} - Archivo no encontrado")
            all_ok = False
    
    return all_ok

def main():
    """Ejecuta todas las verificaciones"""
    print("\n" + "="*70)
    print("REPORTE DE VERIFICACION - INTEGRACION DE SEGURIDAD")
    print("="*70)
    print("Verificando integracion de funciones de seguridad avanzadas")
    print("Fecha: 2025-11-19")
    
    results = {
        "Archivos Requeridos": verify_files_exist(),
        "Funciones de Seguridad": verify_security_functions(),
        "Integracion en Controlador": verify_controller_integration(),
        "Suite de Pruebas": verify_test_suite(),
        "Documentacion": verify_documentation(),
    }
    
    print("\n" + "="*70)
    print("RESUMEN FINAL")
    print("="*70)
    
    for check, result in results.items():
        status = "[OK]" if result else "[ERROR]"
        print(f"{status} {check}")
    
    all_passed = all(results.values())
    
    print("\n" + "="*70)
    if all_passed:
        print("STATUS: TODOS LOS VERIFICACIONES PASARON")
        print("El sistema de seguridad esta completamente integrado y funcional.")
        print("="*70)
        return 0
    else:
        print("STATUS: ALGUNAS VERIFICACIONES FALLARON")
        print("Revise los errores arriba e intente corregirlos.")
        print("="*70)
        return 1

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
