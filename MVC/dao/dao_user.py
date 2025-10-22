from conex.conn import Conex
from modelo.user import User
import logging
from typing import Optional, List, Tuple, Any
import pymysql

logger = logging.getLogger(__name__)

class daoUser:
    """
    Data Access Object para la entidad User.
    
    Proporciona métodos para realizar operaciones CRUD en la tabla 'empleado'
    de la base de datos.
    """
    
    def __init__(self) -> None:
        """
        Inicializa el DAO creando una conexión a la base de datos.
        
        Attributes:
            conex (Conex): Instancia de conexión a la base de datos
            conn: Conexión activa a la base de datos
            cursor: Cursor para ejecutar consultas SQL
        """
        self.conex = Conex()
        self.conn = self.conex.getConex()
        self.cursor: Optional[pymysql.cursors.Cursor] = None

    def validarLogin(self, user: User) -> Optional[Tuple[str, str, str, str, str, int]]:
        """
        Valida las credenciales de un usuario para el login.
        
        Args:
            user (User): Instancia de User con el RUN a validar
            
        Returns:
            Optional[Tuple]: Tupla con los datos del usuario si existe, None en caso contrario
            La tupla contiene: (run, password_hash, nombre, apellido, cargo, id_empleado)
            
        Raises:
            Exception: Si ocurre un error de conexión o consulta a la base de datos
        """
        sql = "SELECT run, password, nombre, apellido, cargo, id_empleado FROM empleado WHERE run = %s"
        try:
            if not self.conn:
                logger.error("No hay conexión a la base de datos para validar login")
                return None
                
            self.cursor = self.conn.cursor()
            self.cursor.execute(sql, (user.getRun(),))
            resultado = self.cursor.fetchone()
            
            if resultado:
                logger.debug("Usuario encontrado en BD: %s", resultado[0])
                return resultado[0], resultado[1], resultado[2], resultado[3], resultado[4], resultado[5]
            else:
                logger.debug("Usuario no encontrado en BD: %s", user.getRun())
                return None
                
        except Exception as e:
            logger.error("Error en validarLogin para usuario %s: %s", user.getRun(), str(e))
            return None
        finally:
            if self.cursor:
                self.cursor.close()

    def agregarUsuario(self, user: User) -> bool:
        """
        Inserta un nuevo usuario en la base de datos.
        
        Args:
            user (User): Instancia de User con los datos a insertar
            
        Returns:
            bool: True si la inserción fue exitosa, False en caso contrario
            
        Raises:
            pymysql.Error: Si ocurre un error de integridad (ej: RUN duplicado)
        """
        sql = "INSERT INTO empleado (run, password, nombre, apellido, cargo) VALUES (%s, %s, %s, %s, %s)"
        try:
            self.cursor = self.conn.cursor()
            self.cursor.execute(sql, (
                user.getRun(), 
                user.getPassword(), 
                user.getNombre(), 
                user.getApellido(), 
                user.getCargo()
            ))
            self.conn.commit()
            logger.debug("Usuario insertado en BD: %s", user.getRun())
            return True
        except Exception as e:
            logger.error("Error al agregar usuario %s en BD: %s", user.getRun(), str(e))
            return False
        finally:
            if self.cursor:
                self.cursor.close()

    def actualizarUsuario(self, user: User) -> bool:
        """
        Actualiza los datos de un usuario existente.
        
        Args:
            user (User): Instancia de User con los datos actualizados
            
        Returns:
            bool: True si la actualización fue exitosa, False en caso contrario
        """
        sql = "UPDATE empleado SET nombre = %s, apellido = %s, password = %s, cargo = %s WHERE run = %s"
        try:
            self.cursor = self.conn.cursor()
            self.cursor.execute(sql, (
                user.getNombre(), 
                user.getApellido(), 
                user.getPassword(), 
                user.getCargo(), 
                user.getRun()
            ))
            self.conn.commit()
            logger.debug("Usuario actualizado en BD: %s", user.getRun())
            return True
        except Exception as e:
            logger.error("Error al actualizar usuario %s en BD: %s", user.getRun(), str(e))
            return False
        finally:
            if self.cursor:
                self.cursor.close()

    def buscarUsuario(self, user: User) -> Optional[Tuple]:
        """
        Busca un usuario por su RUN.
        
        Args:
            user (User): Instancia de User con el RUN a buscar
            
        Returns:
            Optional[Tuple]: Tupla con los datos del usuario si existe, None en caso contrario
        """
        sql = "SELECT run, nombre, apellido, password, cargo, id_empleado FROM empleado WHERE run = %s"
        try:
            self.cursor = self.conn.cursor()
            self.cursor.execute(sql, (user.getRun(),))
            resultado = self.cursor.fetchone()
            logger.debug("Búsqueda de usuario en BD: %s - %s", user.getRun(), "encontrado" if resultado else "no encontrado")
            return resultado
        except Exception as e:
            logger.error("Error al buscar usuario %s en BD: %s", user.getRun(), str(e))
            return None
        finally:
            if self.cursor:
                self.cursor.close()

    def eliminarUsuario(self, user: User) -> bool:
        """
        Elimina un usuario de la base de datos.
        
        Args:
            user (User): Instancia de User con el RUN a eliminar
            
        Returns:
            bool: True si la eliminación fue exitosa, False en caso contrario
            
        Warning:
            Esta operación es irreversible y puede afectar la integridad referencial
        """
        sql = "DELETE FROM empleado WHERE run = %s"
        try:
            self.cursor = self.conn.cursor()
            self.cursor.execute(sql, (user.getRun(),))
            self.conn.commit()
            logger.debug("Usuario eliminado de BD: %s", user.getRun())
            return True
        except Exception as e:
            logger.error("Error al eliminar usuario %s de BD: %s", user.getRun(), str(e))
            return False
        finally:
            if self.cursor:
                self.cursor.close()

    def listarUsuarios(self) -> List[User]:
        """
        Obtiene todos los usuarios registrados en el sistema.
        
        Returns:
            List[User]: Lista de objetos User con todos los empleados
            
        Note:
            Retorna una lista vacía si no hay usuarios o si ocurre un error
        """
        sql = "SELECT run, nombre, apellido, password, cargo, id_empleado FROM empleado ORDER BY nombre, apellido"
        try:
            self.cursor = self.conn.cursor()
            self.cursor.execute(sql)
            resultados = self.cursor.fetchall()
            usuarios: List[User] = []
            for resultado in resultados:
                user = User(
                    run=resultado[0], 
                    nombre=resultado[1], 
                    apellido=resultado[2], 
                    password=resultado[3], 
                    cargo=resultado[4], 
                    id_empleado=resultado[5]
                )
                usuarios.append(user)
            logger.debug("Listados %d usuarios de BD", len(usuarios))
            return usuarios
        except Exception as e:
            logger.error("Error al listar usuarios de BD: %s", str(e))
            return []
        finally:
            if self.cursor:
                self.cursor.close()
