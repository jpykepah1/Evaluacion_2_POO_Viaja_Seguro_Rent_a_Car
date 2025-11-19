import sys
import os

# Agregar el directorio actual al path
sys.path.append(os.path.dirname(__file__))

def test_conexion():
    try:
        from MVC.conex.conn import Conex
        conex = Conex()
        if conex.getConex():
            print("✅ Conexión a BD: OK")
            return True
        else:
            print("❌ Conexión a BD: FALLÓ")
            return False
    except Exception as e:
        print(f"❌ Error en conexión: {e}")
        return False

def test_tablas():
    try:
        from MVC.conex.conn import Conex
        conex = Conex()
        conn = conex.getConex()
        cursor = conn.cursor()
        
        # Verificar tabla empleado
        cursor.execute("SELECT COUNT(*) as count FROM empleado")
        resultado = cursor.fetchone()
        print(f"✅ Tabla empleado: {resultado['count']} registros")
        
        # Verificar datos de empleado
        cursor.execute("SELECT run, nombre, apellido, cargo, LENGTH(password) as pass_len FROM empleado")
        empleados = cursor.fetchall()
        for emp in empleados:
            print(f"   👤 {emp['run']}: {emp['nombre']} {emp['apellido']} - {emp['cargo']} (pass: {emp['pass_len']} chars)")
        
        cursor.close()
        return True
    except Exception as e:
        print(f"❌ Error en tablas: {e}")
        return False

def test_login():
    try:
        from MVC.dto.dto_user import UserDTO
        dto = UserDTO()
        
        print("\n🔐 Probando login...")
        resultado = dto.validarLogin('12345678-9', 'admin123')
        
        if resultado:
            print(f"✅ Login exitoso!")
            print(f"   Usuario: {resultado.getNombre()} {resultado.getApellido()}")
            print(f"   Cargo: {resultado.getCargo()}")
            return True
        else:
            print("❌ Login fallido")
            return False
    except Exception as e:
        print(f"❌ Error en login: {e}")
        return False

if __name__ == "__main__":
    print("🔍 INICIANDO DIAGNÓSTICO COMPLETO")
    print("=" * 50)
    
    test1 = test_conexion()
    test2 = test_tablas() if test1 else False
    test3 = test_login() if test2 else False
    
    print("=" * 50)
    if test1 and test2 and test3:
        print("🎉 TODAS LAS PRUEBAS PASARON! El sistema está listo.")
    else:
        print("❌ Algunas pruebas fallaron. Revisa los errores.")