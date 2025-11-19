import re
import logging
from datetime import datetime
from typing import Optional

def validar_run(run):
    """
    Valida RUN chileno
    Formatos: 12345678-9, 12.345.678-9, 123456789
    """
    try:
        # Limpiar RUN (quitar espacios, puntos, pero mantener guión)
        run_limpio = run.upper().replace(" ", "").replace(".", "").strip()

        # Validar formato
        if not re.match(r'^\d{7,8}[-]?[0-9Kk]$', run_limpio):
            return False, "[ERROR] Formato de RUN inválido"

        # Separar cuerpo y DV
        if '-' in run_limpio:
            partes = run_limpio.split('-')
            cuerpo = partes[0]
            dv = partes[1]
        else:
            cuerpo = run_limpio[:-1]
            dv = run_limpio[-1]

        # Validar que cuerpo sea numérico
        if not cuerpo.isdigit():
            return False, "[ERROR] El RUN solo puede contener números"

        # Validar longitud del cuerpo
        if len(cuerpo) < 7 or len(cuerpo) > 8:
            return False, "[ERROR] RUN debe tener 7 u 8 dígitos"

        return True, f"{cuerpo}-{dv.upper()}"
        
    except Exception as e:
        return False, f"[ERROR] {str(e)}"

def validar_patente(patente):
    """
    Valida patente chilena
    Formatos: ABCD12, ABC123
    """
    try:
        patente_limpia = patente.upper().replace(" ", "").replace("-", "").strip()
        
        # Validar formatos
        # Formato antiguo: ABCD12 (4 letras + 2 números = 6 caracteres)
        if re.match(r'^[A-Z]{4}\d{2}$', patente_limpia):
            return True, "[OK] Patente válida (formato antiguo)"
        # Formato nuevo: ABC123 (3 letras + 3 números = 6 caracteres)  
        elif re.match(r'^[A-Z]{3}\d{3}$', patente_limpia):
            return True, "[OK] Patente válida (formato nuevo)"
        else:
            return False, "[ERROR] Formato de patente inválido. Use: ABCD12 o ABC123"
            
    except Exception as e:
        return False, f"[ERROR] {str(e)}"

def validar_email(email):
    """Valida formato de email"""
    patron = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    
    if re.match(patron, email.strip()):
        return True, "[OK] Email válido"
    return False, "[ERROR] Email inválido"

def validar_telefono(telefono):
    """Valida teléfono chileno"""
    telefono_limpio = telefono.replace(" ", "").replace("+", "").strip()
    
    if re.match(r'^(56?9?[2-9]\d{7})$', telefono_limpio):
        return True, "[OK] Teléfono válido"
    return False, "[ERROR] Teléfono inválido"

def validar_fecha(fecha_str):
    """Valida formato de fecha YYYY-MM-DD"""
    try:
        datetime.strptime(fecha_str.strip(), '%Y-%m-%d')
        return True, "[OK] Fecha válida"
    except ValueError:
        return False, "[ERROR] Fecha inválida. Use: YYYY-MM-DD"

def validar_nombre(nombre):
    """Valida nombre/apellido (solo letras)"""
    if re.match(r'^[A-Za-zÁÉÍÓÚáéíóúÑñ\s]{2,50}$', nombre.strip()):
        return True, "[OK] Nombre válido"
    return False, "[ERROR] Solo letras y espacios (2-50 caracteres)"

def validar_direccion(direccion):
    """Valida dirección"""
    if 5 <= len(direccion.strip()) <= 100:
        return True, "[OK] Dirección válida"
    return False, "[ERROR] Dirección debe tener 5-100 caracteres"

def validar_precio(precio_str):
    """Valida precio (número positivo)"""
    try:
        precio = float(precio_str)
        if precio > 0:
            return True, "[OK] Precio válido"
        return False, "[ERROR] Precio debe ser mayor a 0"
    except ValueError:
        return False, "[ERROR] Precio debe ser un número"

def validar_año(año_str):
    """Valida año de vehículo"""
    try:
        año = int(año_str)
        if 1900 <= año <= datetime.now().year + 1:
            return True, "[OK] Año válido"
        return False, f"[ERROR] Año debe estar entre 1900 y {datetime.now().year + 1}"
    except ValueError:
        return False, "[ERROR] Año debe ser un número"

def validar_password(password):
    """Valida contraseña"""
    if len(password) >= 6:
        return True, "[OK] Contraseña válida"
    return False, "[ERROR] Contraseña muy corta (mínimo 6 caracteres)"

def validar_cargo(cargo):
    """Valida cargo de empleado"""
    if cargo.lower() in ['gerente', 'empleado']:
        return True, "[OK] Cargo válido"
    return False, "[ERROR] Cargo debe ser 'gerente' o 'empleado'"

def validar_estado_vehiculo(estado):
    """Valida estado de vehículo"""
    if estado.lower() in ['disponible', 'arrendado', 'mantencion']:
        return True, "[OK] Estado válido"
    return False, "[ERROR] Estado debe ser: disponible, arrendado o mantencion"

def validar_estado_arriendo(estado):
    """Valida estado de arriendo"""
    if estado.lower() in ['activo', 'finalizado', 'cancelado']:
        return True, "[OK] Estado válido"
    return False, "[ERROR] Estado debe ser: activo, finalizado o cancelado"


def validar_entrada_sql(texto: str, max_longitud: int = 255) -> bool:
    """
    Validación básica para detectar posibles intentos de inyección SQL.

    - Rechaza entradas vacías o demasiado largas.
    - Busca patrones comunes (SELECT, UNION, --, /*, OR 1=1, etc.).

    Nota: Esto no reemplaza el uso de consultas parametrizadas. Siempre
    use parámetros en las consultas SQL; esta función solo añade una
    capa adicional de detección / protección.
    """
    if not texto or len(texto) > max_longitud:
        return False

    patrones_peligrosos = [
        r"\b(SELECT|INSERT|UPDATE|DELETE|DROP|UNION|EXEC)\b",
        r"(--|#|/\*)",
        r"\b(OR|AND)\b\s+\d+\s*=\s*\d+",
        r"\b(WAITFOR|DELAY)\b",
    ]

    for patron in patrones_peligrosos:
        if re.search(patron, texto, re.IGNORECASE):
            logging.warning("Entrada sospechosa para SQL detectada: %s", texto)
            return False

    return True


def sanitizar_texto(texto: str) -> str:
    """
    Sanitiza una cadena removiendo caracteres potencialmente peligrosos.
    Útil para mostrar datos en UI o para reducir riesgo antes de registrarlos.
    """
    if not texto:
        return ""

    # Remueve caracteres comunes que podrían facilitar inyección o romper formatos
    texto_limpio = re.sub(r"[;\\'\"\-\#\*]", "", texto)
    return texto_limpio.strip()


def validar_password_segura(password: str) -> tuple:
    """
    Valida que la contraseña cumpla una política mínima de seguridad.

    Retorna (bool, mensaje)
    """
    if len(password) < 8:
        return False, "[ERROR] La contraseña debe tener al menos 8 caracteres"
    if not re.search(r"[A-Z]", password):
        return False, "[ERROR] Debe contener al menos una mayúscula"
    if not re.search(r"[a-z]", password):
        return False, "[ERROR] Debe contener al menos una minúscula"
    if not re.search(r"\d", password):
        return False, "[ERROR] Debe contener al menos un número"
    if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
        return False, "[ERROR] Debe contener al menos un carácter especial"
    return True, "[OK] Contraseña segura"


# Código de prueba
if __name__ == "__main__":
    print("[TEST] Probando validaciones...")
    
    # Probar RUN
    tests_run = ["12345678-9", "123456789", "12.345.678-9"]
    for test in tests_run:
        resultado = validar_run(test)
        print(f"RUN '{test}': {resultado}")
    
    # Probar patente
    tests_patente = ["ABCD12", "ABC123", "AB1234"]
    for test in tests_patente:
        resultado = validar_patente(test)
        print(f"Patente '{test}': {resultado}")
    
    print("[OK] Todas las funciones cargadas correctamente")
