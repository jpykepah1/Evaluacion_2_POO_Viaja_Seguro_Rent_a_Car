# utils/seguridad.py
import re
import logging
from typing import Optional, List
from utils.encoder import Encoder

logger = logging.getLogger(__name__)

class ValidadorSeguridad:
    """
    Clase para validaciones de seguridad robustas
    """
    
    @staticmethod
    def validar_entrada_sql(texto: str, max_longitud: int = 255) -> bool:
        """
        Previene inyección SQL validando entradas
        """
        if not texto or len(texto) > max_longitud:
            return False
        
        # Patrones peligrosos
        patrones_peligrosos = [
            r"(\b(SELECT|INSERT|UPDATE|DELETE|DROP|UNION|EXEC)\b)",
            r"(\-\-|\#|\/\*)",
            r"(\b(OR|AND)\b\s+\d+\s*=\s*\d+)",
            r"(\b(WAITFOR|DELAY)\b)",
        ]
        
        for patron in patrones_peligrosos:
            if re.search(patron, texto, re.IGNORECASE):
                logger.warning(f"Intento de inyección SQL detectado: {texto}")
                return False
        
        return True
    
    @staticmethod
    def sanitizar_texto(texto: str) -> str:
        """
        Sanitiza texto removiendo caracteres peligrosos
        """
        if not texto:
            return ""
        
        # Remover caracteres potencialmente peligrosos
        texto_limpio = re.sub(r"[;\\\'\"\-\-\#\*]", "", texto)
        return texto_limpio.strip()
    
    @staticmethod
    def validar_password_segura(password: str) -> tuple:
        """
        Valida que la contraseña cumple con políticas de seguridad
        """
        if len(password) < 8:
            return False, "La contraseña debe tener al menos 8 caracteres"
        
        if not re.search(r"[A-Z]", password):
            return False, "Debe contener al menos una mayúscula"
        
        if not re.search(r"[a-z]", password):
            return False, "Debe contener al menos una minúscula"
        
        if not re.search(r"\d", password):
            return False, "Debe contener al menos un número"
        
        if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
            return False, "Debe contener al menos un carácter especial"
        
        return True, "Contraseña segura"
    
    @staticmethod
    def cifrar_datos_sensibles(texto: str) -> Optional[str]:
        """
        Cifra datos sensibles usando el encoder de contraseñas
        """
        try:
            encoder = Encoder()
            return encoder.encode(texto)
        except Exception as e:
            logger.error(f"Error cifrando datos: {e}")
            return None
    
    @staticmethod
    def verificar_acceso_modulo(usuario, modulo: str) -> bool:
        """
        Verifica si un usuario tiene acceso a un módulo específico
        """
        modulos_gerente = ['gestion_empleados', 'informes', 'configuracion']
        modulos_empleado = ['gestion_clientes', 'gestion_vehiculos', 'gestion_arriendos']
        
        if usuario.getCargo() == 'gerente':
            return modulo in modulos_gerente + modulos_empleado
        elif usuario.getCargo() == 'empleado':
            return modulo in modulos_empleado
        
        return False