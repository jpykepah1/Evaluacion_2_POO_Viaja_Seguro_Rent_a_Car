from conex.conn import Conex
from modelo.user import User

class daoUser:
    def __init__(self):
        self.conex = Conex()
        self.conn = self.conex.getConex()
        self.cursor = None

    def validarLogin(self, user):
        sql = "SELECT run, password, nombre, apellido, cargo, id_empleado FROM empleado WHERE run = %s"
        try:
            if not self.conn:
                print("❌ No hay conexión a la base de datos")
                return None
                
            self.cursor = self.conn.cursor()
            self.cursor.execute(sql, (user.getRun(),))
            resultado = self.cursor.fetchone()
            
            if resultado:
                print(f"✅ Usuario encontrado: {resultado[2]} {resultado[3]}")
                return resultado[0], resultado[1], resultado[2], resultado[3], resultado[4], resultado[5]
            else:
                print(f"❌ No se encontró usuario con RUN: {user.getRun()}")
                return None
                
        except Exception as e:
            print(f"❌ Error en validarLogin: {e}")
            return None
        finally:
            if self.cursor:
                self.cursor.close()

    def agregarUsuario(self, user):
        sql = "INSERT INTO empleado (run, password, nombre, apellido, cargo) VALUES (%s, %s, %s, %s, %s)"
        try:
            self.cursor = self.conn.cursor()
            self.cursor.execute(sql, (user.getRun(), user.getPassword(), user.getNombre(), user.getApellido(), user.getCargo()))
            self.conn.commit()
            return True
        except Exception as e:
            print(f"Error al agregar usuario: {e}")
            return False
        finally:
            if self.cursor:
                self.cursor.close()

    def actualizarUsuario(self, user):
        sql = "UPDATE empleado SET nombre = %s, apellido = %s, password = %s, cargo = %s WHERE run = %s"
        try:
            self.cursor = self.conn.cursor()
            self.cursor.execute(sql, (user.getNombre(), user.getApellido(), user.getPassword(), user.getCargo(), user.getRun()))
            self.conn.commit()
            return True
        except Exception as e:
            print(f"Error al actualizar usuario: {e}")
            return False
        finally:
            if self.cursor:
                self.cursor.close()

    def buscarUsuario(self, user):
        sql = "SELECT run, nombre, apellido, password, cargo, id_empleado FROM empleado WHERE run = %s"
        try:
            self.cursor = self.conn.cursor()
            self.cursor.execute(sql, (user.getRun(),))
            resultado = self.cursor.fetchone()
            return resultado
        except Exception as e:
            print(f"Error al buscar usuario: {e}")
            return None
        finally:
            if self.cursor:
                self.cursor.close()

    def eliminarUsuario(self, user):
        sql = "DELETE FROM empleado WHERE run = %s"
        try:
            self.cursor = self.conn.cursor()
            self.cursor.execute(sql, (user.getRun(),))
            self.conn.commit()
            return True
        except Exception as e:
            print(f"Error al eliminar usuario: {e}")
            return False
        finally:
            if self.cursor:
                self.cursor.close()

    def listarUsuarios(self):
        sql = "SELECT run, nombre, apellido, password, cargo, id_empleado FROM empleado ORDER BY nombre, apellido"
        try:
            self.cursor = self.conn.cursor()
            self.cursor.execute(sql)
            resultados = self.cursor.fetchall()
            usuarios = []
            for resultado in resultados:
                user = User(resultado[0], resultado[1], resultado[2], resultado[3], resultado[4], resultado[5])
                usuarios.append(user)
            return usuarios
        except Exception as e:
            print(f"Error al listar usuarios: {e}")
            return []
        finally:
            if self.cursor:
                self.cursor.close()