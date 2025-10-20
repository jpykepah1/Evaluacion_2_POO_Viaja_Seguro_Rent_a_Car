from modelo.user import User
from dao.dao_user import daoUser
from utils.encoder import Encoder

class UserDTO:
    def validarLogin(self, username, clave):
        print(f"🔍 Intentando login para RUN: {username}")
        daouser = daoUser()
        resultado = daouser.validarLogin(User(run=username))
       
        if resultado is not None:
            run_db, password_hash_db, nombre, apellido, cargo, id_empleado = resultado
            print(f"🔍 Hash encontrado en BD: {password_hash_db[:20]}...")
            print(f"🔍 Verificando contraseña...")
            
            # Verificar la contraseña
            if Encoder().verify(clave, password_hash_db):
                print(f"✅ Contraseña correcta para {nombre} {apellido}")
                return User(run_db, nombre, apellido, password_hash_db, cargo, id_empleado)
            else:
                print("❌ Contraseña incorrecta")
                return None
        else:
            print("❌ No se pudo obtener resultado de la base de datos")
            return None

    def agregarUsuario(self, run, nombre, apellido, password, cargo):
        hashed_password = Encoder().encode(password)
        daouser = daoUser()
        return daouser.agregarUsuario(
            User(run=run, nombre=nombre, apellido=apellido, password=hashed_password, cargo=cargo)
        )

    def actualizarUsuario(self, run, nombre, apellido, password, cargo):
        # Si la password viene en texto plano, la encriptamos
        if not password.startswith('$2b$'):
            hashed_password = Encoder().encode(password)
        else:
            hashed_password = password
            
        daouser = daoUser()
        return daouser.actualizarUsuario(
            User(run=run, nombre=nombre, apellido=apellido, password=hashed_password, cargo=cargo)
        )

    def buscarUsuario(self, run):
        daouser = daoUser()
        resultado = daouser.buscarUsuario(User(run=run))
        if resultado:
            return User(resultado[0], resultado[1], resultado[2], resultado[3], resultado[4], resultado[5])
        return None

    def eliminarUsuario(self, run):
        daouser = daoUser()
        return daouser.eliminarUsuario(User(run=run))

    def listarUsuarios(self):
        daouser = daoUser()
        return daouser.listarUsuarios()
