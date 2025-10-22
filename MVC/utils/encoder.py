import bcrypt
import logging
from typing import Optional

logger = logging.getLogger(__name__)

class Encoder:
    """
    Utilidad para el manejo seguro de contraseñas usando bcrypt.
    
    Proporciona métodos para encriptar y verificar contraseñas
    utilizando el algoritmo bcrypt con salt automático.
    """
   
    def encode(self, password: str) -> Optional[str]:
        """
        Genera un hash seguro de una contraseña usando bcrypt.
        
        Args:
            password (str): Contraseña en texto plano a encriptar
            
        Returns:
            Optional[str]: Hash bcrypt de la contraseña, o None en caso de error
            
        Example:
            >>> encoder = Encoder()
            >>> hash = encoder.encode("mi_contraseña")
            >>> print(hash.startswith('$2b$'))
            True
        """
        try:
            # Generar salt y hashear la contraseña
            salt = bcrypt.gensalt()
            hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
            logger.debug("Contraseña encriptada exitosamente")
            return hashed.decode('utf-8')
        except Exception as e:
            logger.error("Error al encriptar contraseña: %s", str(e))
            return None
   
    def verify(self, password: str, hashed_password: str) -> bool:
        """
        Verifica si una contraseña coincide con un hash bcrypt.
        
        Args:
            password (str): Contraseña en texto plano a verificar
            hashed_password (str): Hash bcrypt almacenado
            
        Returns:
            bool: True si la contraseña coincide, False en caso contrario
            
        Note:
            Este método es seguro contra timing attacks
        """
        try:
            if not hashed_password:
                logger.warning("Intento de verificación con hash vacío")
                return False
            return bcrypt.checkpw(
                password.encode('utf-8'), 
                hashed_password.encode('utf-8')
            )
        except Exception as e:
            logger.error("Error al verificar contraseña: %s", str(e))
            return False

    def is_hashed(self, password: str) -> bool:
        """
        Determina si una cadena ya está en formato hash bcrypt.
        
        Args:
            password (str): Cadena a verificar
            
        Returns:
            bool: True si la cadena tiene formato de hash bcrypt, False en caso contrario
            
        Example:
            >>> encoder = Encoder()
            >>> encoder.is_hashed('$2b$12$...')
            True
            >>> encoder.is_hashed('contraseña_plana')
            False
        """
        if not password:
            return False
        return password.startswith('$2b$')
