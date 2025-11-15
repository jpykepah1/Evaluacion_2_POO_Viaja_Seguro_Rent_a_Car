# utils/logger.py
import logging
import os
from datetime import datetime

class SistemaLogging:
    _configurado = False
    
    @classmethod
    def configurar(cls, nivel=logging.INFO, archivo_log='sistema_arriendos.log'):
        if cls._configurado:
            return
            
        # Crear directorio de logs si no existe
        os.makedirs('logs', exist_ok=True)
        ruta_log = os.path.join('logs', archivo_log)
        
        # Configurar formato
        formato = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        
        # Configurar handler de archivo
        file_handler = logging.FileHandler(ruta_log, encoding='utf-8')
        file_handler.setFormatter(formato)
        
        # Configurar handler de consola (solo para desarrollo)
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formato)
        
        # Configurar logger raíz
        logger_raíz = logging.getLogger()
        logger_raíz.setLevel(nivel)
        logger_raíz.addHandler(file_handler)
        
        # En producción, comentar la siguiente línea para evitar logs en consola
        logger_raíz.addHandler(console_handler)
        
        cls._configurado = True
        logging.info("Sistema de logging configurado correctamente")
    
    @classmethod
    def obtener_logger(cls, nombre):
        return logging.getLogger(nombre)
