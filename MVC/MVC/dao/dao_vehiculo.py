from conex.conn import Conex
from modelo.vehiculo import Vehiculo
import logging
from typing import Optional, List
import pymysql

logger = logging.getLogger(__name__)

class DaoVehiculo:
    """
    Data Access Object para la entidad Vehiculo.
    
    Proporciona métodos para realizar operaciones CRUD en la tabla 'vehiculo'
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

    def agregarVehiculo(self, vehiculo: Vehiculo) -> bool:
        """
        Inserta un nuevo vehículo en la base de datos.
        
        Args:
            vehiculo (Vehiculo): Instancia de Vehiculo con los datos a insertar
            
        Returns:
            bool: True si la inserción fue exitosa, False en caso contrario
            
        Raises:
            pymysql.Error: Si ocurre un error de integridad (ej: patente duplicada)
        """
        sql = "INSERT INTO vehiculo (patente, marca, modelo, año, precio_diario, estado) VALUES (%s, %s, %s, %s, %s, %s)"
        try:
            self.cursor = self.conn.cursor()
            self.cursor.execute(sql, (
                vehiculo.getPatente(), 
                vehiculo.getMarca(), 
                vehiculo.getModelo(), 
                vehiculo.getAño(), 
                vehiculo.getPrecioDiario(), 
                vehiculo.getEstado()
            ))
            self.conn.commit()
            return True
        except Exception as e:
            logger.error("Error al agregar vehículo: %s", e)
            return False
        finally:
            if self.cursor:
                self.cursor.close()

    def buscarVehiculo(self, patente: str) -> Optional[Vehiculo]:
        """
        Busca un vehículo por su patente.
        
        Args:
            patente (str): Patente del vehículo a buscar
            
        Returns:
            Optional[Vehiculo]: Instancia de Vehiculo si se encuentra, None en caso contrario
        """
        sql = "SELECT id_vehiculo, patente, marca, modelo, año, precio_diario, estado, create_time FROM vehiculo WHERE patente = %s"
        try:
            self.cursor = self.conn.cursor()
            self.cursor.execute(sql, (patente,))
            resultado = self.cursor.fetchone()
            if resultado:
                return Vehiculo(
                    patente=resultado[1], 
                    marca=resultado[2], 
                    modelo=resultado[3], 
                    año=int(resultado[4]), 
                    precio_diario=float(resultado[5]), 
                    estado=resultado[6], 
                    id_vehiculo=int(resultado[0]), 
                    create_time=resultado[7]
                )
            return None
        except Exception as e:
            logger.error("Error al buscar vehículo: %s", e)
            return None
        finally:
            if self.cursor:
                self.cursor.close()

    def buscarVehiculoPorId(self, id_vehiculo: int) -> Optional[Vehiculo]:
        """
        Busca un vehículo por su ID único.
        
        Args:
            id_vehiculo (int): ID del vehículo a buscar
            
        Returns:
            Optional[Vehiculo]: Instancia de Vehiculo si se encuentra, None en caso contrario
        """
        sql = "SELECT id_vehiculo, patente, marca, modelo, año, precio_diario, estado, create_time FROM vehiculo WHERE id_vehiculo = %s"
        try:
            self.cursor = self.conn.cursor()
            self.cursor.execute(sql, (id_vehiculo,))
            resultado = self.cursor.fetchone()
            if resultado:
                return Vehiculo(
                    patente=resultado[1], 
                    marca=resultado[2], 
                    modelo=resultado[3], 
                    año=int(resultado[4]), 
                    precio_diario=float(resultado[5]), 
                    estado=resultado[6], 
                    id_vehiculo=int(resultado[0]), 
                    create_time=resultado[7]
                )
            return None
        except Exception as e:
            logger.error("Error al buscar vehículo por ID: %s", e)
            return None
        finally:
            if self.cursor:
                self.cursor.close()

    def actualizarVehiculo(self, vehiculo: Vehiculo) -> bool:
        """
        Actualiza los datos de un vehículo existente.
        
        Args:
            vehiculo (Vehiculo): Instancia de Vehiculo con los datos actualizados
            
        Returns:
            bool: True si la actualización fue exitosa, False en caso contrario
        """
        sql = "UPDATE vehiculo SET marca = %s, modelo = %s, año = %s, precio_diario = %s, estado = %s WHERE patente = %s"
        try:
            self.cursor = self.conn.cursor()
            self.cursor.execute(sql, (
                vehiculo.getMarca(), 
                vehiculo.getModelo(), 
                vehiculo.getAño(), 
                vehiculo.getPrecioDiario(), 
                vehiculo.getEstado(), 
                vehiculo.getPatente()
            ))
            self.conn.commit()
            return True
        except Exception as e:
            logger.error("Error al actualizar vehículo: %s", e)
            return False
        finally:
            if self.cursor:
                self.cursor.close()

    def eliminarVehiculo(self, patente: str) -> bool:
        """
        Elimina un vehículo de la base de datos.
        
        Args:
            patente (str): Patente del vehículo a eliminar
            
        Returns:
            bool: True si la eliminación fue exitosa, False en caso contrario
            
        Warning:
            Esta operación puede fallar si el vehículo tiene arriendos asociados
        """
        sql = "DELETE FROM vehiculo WHERE patente = %s"
        try:
            self.cursor = self.conn.cursor()
            self.cursor.execute(sql, (patente,))
            self.conn.commit()
            return True
        except Exception as e:
            logger.error("Error al eliminar vehículo: %s", e)
            return False
        finally:
            if self.cursor:
                self.cursor.close()

    def listarVehiculos(self) -> List[Vehiculo]:
        """
        Obtiene todos los vehículos registrados en el sistema.
        
        Returns:
            List[Vehiculo]: Lista de objetos Vehiculo con todos los vehículos
            
        Note:
            Retorna una lista vacía si no hay vehículos o si ocurre un error
        """
        sql = "SELECT id_vehiculo, patente, marca, modelo, año, precio_diario, estado, create_time FROM vehiculo ORDER BY marca, modelo"
        try:
            self.cursor = self.conn.cursor()
            self.cursor.execute(sql)
            resultados = self.cursor.fetchall()
            vehiculos: List[Vehiculo] = []
            for resultado in resultados:
                vehiculo = Vehiculo(
                    patente=resultado[1], 
                    marca=resultado[2], 
                    modelo=resultado[3], 
                    año=int(resultado[4]), 
                    precio_diario=float(resultado[5]),
                    estado=resultado[6], 
                    id_vehiculo=resultado[0], 
                    create_time=resultado[7]
                )
                vehiculos.append(vehiculo)
            return vehiculos
        except Exception as e:
            logger.error("Error al listar vehículos: %s", e)
            return []
        finally:
            if self.cursor:
                self.cursor.close()

    def listarVehiculosDisponibles(self) -> List[Vehiculo]:
        """
        Obtiene todos los vehículos con estado 'disponible'.
        
        Returns:
            List[Vehiculo]: Lista de vehículos disponibles para arriendo
            
        Note:
            Retorna una lista vacía si no hay vehículos disponibles o si ocurre un error
        """
        sql = "SELECT id_vehiculo, patente, marca, modelo, año, precio_diario, estado, create_time FROM vehiculo WHERE estado = 'disponible' ORDER BY marca, modelo"
        try:
            self.cursor = self.conn.cursor()
            self.cursor.execute(sql)
            resultados = self.cursor.fetchall()
            vehiculos: List[Vehiculo] = []
            for resultado in resultados:
                vehiculo = Vehiculo(
                    patente=resultado[1], 
                    marca=resultado[2], 
                    modelo=resultado[3], 
                    año=int(resultado[4]), 
                    precio_diario=float(resultado[5]), 
                    estado=resultado[6], 
                    id_vehiculo=resultado[0], 
                    create_time=resultado[7]
                )
                vehiculos.append(vehiculo)
            return vehiculos
        except Exception as e:
            logger.error("Error al listar vehículos disponibles: %s", e)
            return []
        finally:
            if self.cursor:
                self.cursor.close()
