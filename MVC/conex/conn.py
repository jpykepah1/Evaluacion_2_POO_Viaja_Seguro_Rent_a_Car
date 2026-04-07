import os
import pymysql
from typing import Optional
import logging

logger = logging.getLogger(__name__)

class Conex:
    """
    Maneja la conexión a la base de datos MySQL.

    Proporciona una interfaz simplificada para establecer, verificar
    y cerrar conexiones a la base de datos.

    Attributes:
        host (str): Servidor de base de datos
        user (str): Usuario de la base de datos
        passwd (str): Contraseña del usuario
        database (str): Nombre de la base de datos
        port (int): Puerto de conexión
        __myconn: Conexión interna a MySQL
    """

    def __init__(self, host: Optional[str] = None, user: Optional[str] = None,
                 passwd: Optional[str] = None, database: Optional[str] = None,
                 port: Optional[int] = None) -> None:
        """
        Inicializa una nueva conexión a la base de datos.

        Args:
            host (str): Servidor de base de datos (default: DB_HOST o "localhost")
            user (str): Usuario de la base de datos (default: DB_USER o "root")
            passwd (str): Contraseña del usuario (default: DB_PASSWORD o "")
            database (str): Nombre de la base de datos (default: DB_NAME o "viaja_seguro")
            port (int): Puerto de conexión (default: DB_PORT o 3306)
        """
        self.host = host if host is not None else os.environ.get("DB_HOST", "localhost")
        self.user = user if user is not None else os.environ.get("DB_USER", "root")
        self.passwd = passwd if passwd is not None else os.environ.get("DB_PASSWORD", "")
        self.database = database if database is not None else os.environ.get("DB_NAME", "viaja_seguro")
        try:
            self.port = port if port is not None else int(os.environ.get("DB_PORT", "3306"))
        except ValueError:
            self.port = 3306
        self.__myconn: Optional[pymysql.connections.Connection] = None
        self.connect()

    def connect(self) -> None:
        """
        Establece la conexión con la base de datos.

        Raises:
            pymysql.Error: Si no se puede establecer la conexión
        """
        try:
            self.__myconn = pymysql.connect(
                host=self.host,
                user=self.user,
                password=self.passwd,
                database=self.database,
                port=self.port,
                charset='utf8mb4'
            )
            logger.info("✅ Conexión a MySQL establecida correctamente")
            logger.info("✅ Base de datos: %s", self.database)
        except Exception as ex:
            logger.error("❌ Error de conexión: %s", ex)
            logger.error("   Host: %s, User: %s, Database: %s",
                        self.host, self.user, self.database)
            self.__myconn = None

    def closeConex(self) -> None:
        """Cierra la conexión a la base de datos si está abierta."""
        if self.__myconn:
            self.__myconn.close()
            logger.info("🔌 Conexión cerrada")

    def getConex(self) -> Optional[pymysql.connections.Connection]:
        """
        Obtiene la conexión activa a la base de datos.

        Returns:
            Optional[pymysql.connections.Connection]: Conexión activa o None
        """
        return self.__myconn

    def is_connected(self) -> bool:
        """
        Verifica si la conexión está activa y funcionando.

        Returns:
            bool: True si la conexión está activa, False en caso contrario
        """
        try:
            if self.__myconn and self.__myconn.open:
                cursor = self.__myconn.cursor()
                cursor.execute("SELECT 1")
                cursor.close()
                return True
            return False
        except Exception:
            return False
