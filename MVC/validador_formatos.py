import re
from datetime import datetime

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
            return False, "❌ Formato de RUN inválido"

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
            return False, "❌ El RUN solo puede contener números"

        # Validar longitud del cuerpo
        if len(cuerpo) < 7 or len(cuerpo) > 8:
            return False, "❌ RUN debe tener 7 u 8 dígitos"

        return True, f"{cuerpo}-{dv.upper()}"
        
    except Exception as e:
        return False, f"❌ Error: {str(e)}"

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
            return True, "✅ Patente válida (formato antiguo)"
        # Formato nuevo: ABC123 (3 letras + 3 números = 6 caracteres)  
        elif re.match(r'^[A-Z]{3}\d{3}$', patente_limpia):
            return True, "✅ Patente válida (formato nuevo)"
        else:
            return False, "❌ Formato de patente inválido. Use: ABCD12 o ABC123"
            
    except Exception as e:
        return False, f"❌ Error: {str(e)}"

def validar_email(email):
    """Valida formato de email"""
    patron = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    
    if re.match(patron, email.strip()):
        return True, "✅ Email válido"
    return False, "❌ Email inválido"

def validar_telefono(telefono):
    """Valida teléfono chileno"""
    telefono_limpio = telefono.replace(" ", "").replace("+", "").strip()
    
    if re.match(r'^(56?9?[2-9]\d{7})$', telefono_limpio):
        return True, "✅ Teléfono válido"
    return False, "❌ Teléfono inválido"

def validar_fecha(fecha_str):
    """Valida formato de fecha YYYY-MM-DD"""
    try:
        datetime.strptime(fecha_str.strip(), '%Y-%m-%d')
        return True, "✅ Fecha válida"
    except ValueError:
        return False, "❌ Fecha inválida. Use: YYYY-MM-DD"

def validar_nombre(nombre):
    """Valida nombre/apellido (solo letras)"""
    if re.match(r'^[A-Za-zÁÉÍÓÚáéíóúÑñ\s]{2,50}$', nombre.strip()):
        return True, "✅ Nombre válido"
    return False, "❌ Solo letras y espacios (2-50 caracteres)"

def validar_direccion(direccion):
    """Valida dirección"""
    if 5 <= len(direccion.strip()) <= 100:
        return True, "✅ Dirección válida"
    return False, "❌ Dirección debe tener 5-100 caracteres"

def validar_precio(precio_str):
    """Valida precio (número positivo)"""
    try:
        precio = float(precio_str)
        if precio > 0:
            return True, "✅ Precio válido"
        return False, "❌ Precio debe ser mayor a 0"
    except ValueError:
        return False, "❌ Precio debe ser un número"

def validar_año(año_str):
    """Valida año de vehículo"""
    try:
        año = int(año_str)
        if 1900 <= año <= datetime.now().year + 1:
            return True, "✅ Año válido"
        return False, f"❌ Año debe estar entre 1900 y {datetime.now().year + 1}"
    except ValueError:
        return False, "❌ Año debe ser un número"

def validar_password(password):
    """Valida contraseña"""
    if len(password) >= 6:
        return True, "✅ Contraseña válida"
    return False, "❌ Contraseña muy corta (mínimo 6 caracteres)"

def validar_cargo(cargo):
    """Valida cargo de empleado"""
    if cargo.lower() in ['gerente', 'empleado']:
        return True, "✅ Cargo válido"
    return False, "❌ Cargo debe ser 'gerente' o 'empleado'"

def validar_estado_vehiculo(estado):
    """Valida estado de vehículo"""
    if estado.lower() in ['disponible', 'arrendado', 'mantencion']:
        return True, "✅ Estado válido"
    return False, "❌ Estado debe ser: disponible, arrendado o mantencion"

def validar_estado_arriendo(estado):
    """Valida estado de arriendo"""
    if estado.lower() in ['activo', 'finalizado', 'cancelado']:
        return True, "✅ Estado válido"
    return False, "❌ Estado debe ser: activo, finalizado o cancelado"

# Código de prueba
if __name__ == "__main__":
    print("🧪 Probando validaciones...")
    
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
    
    print("✅ Todas las funciones cargadas correctamente")
