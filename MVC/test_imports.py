import sys
import os

# Agregar el directorio actual al path
sys.path.append(os.path.dirname(__file__))

try:
    from modelo.user import User
    print("✅ User importado correctamente")
    
    from dao.dao_user import daoUser
    print("✅ daoUser importado correctamente")
    
    from dto.dto_user import UserDTO
    print("✅ UserDTO importado correctamente")
    
    from conex.conn import Conex
    print("✅ Conex importado correctamente")
    
    print("🎉 Todas las importaciones funcionan!")
    
except ImportError as e:
    print(f"❌ Error de importación: {e}")
except Exception as e:
    print(f"❌ Otro error: {e}")