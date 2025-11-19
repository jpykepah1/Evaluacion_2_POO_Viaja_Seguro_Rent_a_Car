from modelo.user import User
from dao.dao_user import daoUser
from utils.encoder import Encoder
import logging
from typing import Optional, Tuple, List

logger = logging.getLogger(__name__)

class UserDTO:
    """
    Data Transfer Object para la entidad User.
    
    Se encarga de la transferencia de datos entre la capa de negocio
    y la capa de persistencia, aplicando validaciones y transformaciones
    necesarias.
    """
    
    def validarLogin(self, username: str, clave: str) -> Optional[User]:
        """
        Valida las credenciales de un usuario en el sistema.
        
        Args:
            username (str): RUN del usuario a validar
            clave (str): Contraseña en texto plano para verificar
            
        Returns:
            Optional[User]: Instancia de User si las credenciales son válidas,
                          None en caso contrario
                          
        Raises:
            Exception: Si ocurre un error inesperado durante la validación
        """
        logger.debug("Intentando validar login para usuario: %s", username)
        daouser = daoUser()
        resultado = daouser.validarLogin(User(run=username))
       
        if resultado is not None:
            run_db, password_hash_db, nombre, apellido, cargo, id_empleado = resultado
            logger.debug("Hash de contraseña recuperado para usuario: %s", username)
            
            # Verificar la contraseña
            if Encoder().verify(clave, password_hash_db):
                logger.info("Login exitoso para usuario: %s %s (%s)", nombre, apellido, cargo)
                return User(
                    run=run_db, 
                    nombre=nombre, 
                    apellido=apellido, 
                    password=password_hash_db, 
                    cargo=cargo, 
                    id_empleado=id_empleado
                )
            else:
                logger.warning("Contraseña incorrecta para usuario: %s", username)
                return None
        else:
            logger.warning("Usuario no encontrado: %s", username)
            return None

    def agregarUsuario(self, run: str, nombre: str, apellido: str, 
                      password: str, cargo: str) -> bool:
        """
        Agrega un nuevo usuario al sistema.
        
        Args:
            run (str): RUN del nuevo usuario
            nombre (str): Nombre del usuario
            apellido (str): Apellido del usuario
            password (str): Contraseña en texto plano (será encriptada)
            cargo (str): Cargo del usuario ('gerente' o 'empleado')
            
        Returns:
            bool: True si el usuario fue agregado exitosamente, False en caso contrario
            
        Raises:
            Exception: Si ocurre un error durante la inserción en la base de datos
        """
        logger.info("Agregando nuevo usuario: %s %s (%s)", nombre, apellido, cargo)
        hashed_password = Encoder().encode(password)
        daouser = daoUser()
        return daouser.agregarUsuario(
            User(
                run=run, 
                nombre=nombre, 
                apellido=apellido, 
                password=hashed_password, 
                cargo=cargo
            )
        )

    def actualizarUsuario(self, run: str, nombre: str, apellido: str, 
                         password: str, cargo: str) -> bool:
        """
        Actualiza la información de un usuario existente.
        
        Args:
            run (str): RUN del usuario a actualizar
            nombre (str): Nuevo nombre del usuario
            apellido (str): Nuevo apellido del usuario
            password (str): Nueva contraseña (si está en texto plano, será encriptada)
            cargo (str): Nuevo cargo del usuario
            
        Returns:
            bool: True si la actualización fue exitosa, False en caso contrario
            
        Note:
            Si la password ya está encriptada (comienza con '$2b$'), no se vuelve a encriptar
        """
        logger.info("Actualizando usuario: %s", run)
        # Si la password viene en texto plano, la encriptamos
        if not password.startswith('$2b$'):
            hashed_password = Encoder().encode(password)
        else:
            hashed_password = password
            
        daouser = daoUser()
        return daouser.actualizarUsuario(
            User(
                run=run, 
                nombre=nombre, 
                apellido=apellido, 
                password=hashed_password, 
                cargo=cargo
            )
        )

    def buscarUsuario(self, run: str) -> Optional[User]:
        """
        Busca un usuario por su RUN.
        
        Args:
            run (str): RUN del usuario a buscar
            
        Returns:
            Optional[User]: Instancia de User si se encuentra, None en caso contrario
        """
        daouser = daoUser()
        resultado = daouser.buscarUsuario(User(run=run))
        if resultado:
            return User(
                run=resultado[0], 
                nombre=resultado[1], 
                apellido=resultado[2], 
                password=resultado[3], 
                cargo=resultado[4], 
                id_empleado=resultado[5]
            )
        return None

    def eliminarUsuario(self, run: str) -> bool:
        """
        Elimina un usuario del sistema.
        
        Args:
            run (str): RUN del usuario a eliminar
            
        Returns:
            bool: True si la eliminación fue exitosa, False en caso contrario
            
        Warning:
            Esta operación es irreversible
        """
        daouser = daoUser()
        return daouser.eliminarUsuario(User(run=run))

    def listarUsuarios(self) -> List[User]:
        """
        Obtiene la lista completa de usuarios del sistema.
        
        Returns:
            List[User]: Lista de todos los usuarios registrados
            
        Note:
            Retorna una lista vacía si no hay usuarios registrados
        """
        daouser = daoUser()
        return daouser.listarUsuarios()
