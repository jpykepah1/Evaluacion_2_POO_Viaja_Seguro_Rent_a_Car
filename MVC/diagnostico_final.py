from conex.conn import Conex

def test_simple():
    try:
        conex = Conex()
        conn = conex.getConex()
        cursor = conn.cursor()
        
        # Consulta simple
        cursor.execute("SELECT run, password FROM empleado WHERE run = '12345678-9'")
        result = cursor.fetchone()
        
        print("✅ Consulta exitosa")
        print(f"RUN: {result[0]}")
        print(f"Password hash: {result[1][:30]}...")
        
        cursor.close()
        return True
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_login_simple():
    try:
        from dao.dao_user import daoUser
        from modelo.user import User
        
        dao = daoUser()
        user = User(run='12345678-9')
        result = dao.validarLogin(user)
        
        if result:
            print("✅ validarLogin exitoso")
            print(f"Datos retornados: {len(result)} elementos")
            return True
        else:
            print("❌ validarLogin retornó None")
            return False
    except Exception as e:
        print(f"❌ Error en test_login_simple: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("🔍 DIAGNÓSTICO FINAL")
    print("=" * 40)
    
    test1 = test_simple()
    test2 = test_login_simple()
    
    print("=" * 40)
    if test1 and test2:
        print("🎉 Diagnóstico exitoso - El sistema debería funcionar")
    else:
        print("❌ Hay problemas que resolver")