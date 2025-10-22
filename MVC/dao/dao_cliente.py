from conex.conn import Conex
from modelo.cliente import Cliente
import logging
from typing import Optional, List
import pymysql

logger = logging.getLogger(__name__)

class DaoCliente:
    """
    Data Access Object para la entidad Cliente.
    
    Proporciona métodos para realizar operaciones CRUD en la tabla 'cliente'
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

    def agregarCliente(self, cliente: Cliente) -> bool:
        """
        Inserta un nuevo cliente en la base de datos.
        
        Args:
            cliente (Cliente): Instancia de Cliente con los datos a insertar
            
        Returns:
            bool: True si la inserción fue exitosa, False en caso contrario
            
        Raises:
            pymysql.Error: Si ocurre un error de integridad (ej: RUN duplicado)
        """
        sql = "INSERT INTO cliente (run, nombre, apellido, direccion, telefono) VALUES (%s, %s, %s, %s, %s)"
        try:
            self.cursor = self.conn.cursor()
            self.cursor.execute(sql, (
                cliente.getRun(), 
                cliente.getNombre(), 
                cliente.getApellido(), 
                cliente.getDireccion(), 
                cliente.getTelefono()
            ))
            self.conn.commit()
            return True
        except Exception as e:
            logger.error("Error al agregar cliente: %s", e)
            return False
        finally:
            if self.cursor:
                self.cursor.close()

    def buscarCliente(self, run: str) -> Optional[Cliente]:
        """
        Busca un cliente por su RUN.
        
        Args:
            run (str): RUN del cliente a buscar
            
        Returns:
            Optional[Cliente]: Instancia de Cliente si se encuentra, None en caso contrario
        """
        sql = "SELECT * FROM cliente WHERE run = %s"
        try:
            self.cursor = self.conn.cursor()
            self.cursor.execute(sql, (run,))
            resultado = self.cursor.fetchone()
            if resultado:
                return Cliente(
                    run=resultado[1], 
                    nombre=resultado[2], 
                    apellido=resultado[3], 
                    direccion=resultado[4], 
                    telefono=resultado[5], 
                    id_cliente=resultado[0], 
                    create_time=resultado[6]
                )
            return None
        except Exception as e:
            logger.error("Error al buscar cliente: %s", e)
            return None
        finally:
            if self.cursor:
                self.cursor.close()

    def actualizarCliente(self, cliente: Cliente) -> bool:
        """
        Actualiza los datos de un cliente existente.
        
        Args:
            cliente (Cliente): Instancia de Cliente con los datos actualizados
            
        Returns:
            bool: True si la actualización fue exitosa, False en caso contrario
        """
        sql = "UPDATE cliente SET nombre = %s, apellido = %s, direccion = %s, telefono = %s WHERE run = %s"
        try:
            self.cursor = self.conn.cursor()
            self.cursor.execute(sql, (
                cliente.getNombre(), 
                cliente.getApellido(), 
                cliente.getDireccion(), 
                cliente.getTelefono(), 
                cliente.getRun()
            ))
            self.conn.commit()
            return True
        except Exception as e:
            logger.error("Error al actualizar cliente: %s", e)
            return False
        finally:
            if self.cursor:
                self.cursor.close()

    def eliminarCliente(self, run: str) -> bool:
        """
        Elimina un cliente de la base de datos.
        
        Args:
            run (str): RUN del cliente a eliminar
            
        Returns:
            bool: True si la eliminación fue exitosa, False en caso contrario
            
        Warning:
            Esta operación puede fallar si el cliente tiene arriendos asociados
        """
        sql = "DELETE FROM cliente WHERE run = %s"
        try:
            self.cursor = self.conn.cursor()
            self.cursor.execute(sql, (run,))
            self.conn.commit()
            return True
        except Exception as e:
            logger.error("Error al eliminar cliente: %s", e)
            return False
        finally:
            if self.cursor:
                self.cursor.close()

    def listarClientes(self) -> List[Cliente]:
        """
        Obtiene todos los clientes registrados en el sistema.
        
        Returns:
            List[Cliente]: Lista de objetos Cliente con todos los clientes
            
        Note:
            Retorna una lista vacía si no hay clientes o si ocurre un error
        """
        sql = "SELECT * FROM cliente ORDER BY nombre, apellido"
        try:
            self.cursor = self.conn.cursor()
            self.cursor.execute(sql)
            resultados = self.cursor.fetchall()
            clientes: List[Cliente] = []
            for resultado in resultados:
                cliente = Cliente(
                    run=resultado[1], 
                    nombre=resultado[2], 
                    apellido=resultado[3], 
                    direccion=resultado[4], 
                    telefono=resultado[5], 
                    id_cliente=resultado[0], 
                    create_time=resultado[6]
                )
                clientes.append(cliente)
            return clientes
        except Exception as e:
            logger.error("Error al listar clientes: %s", e)
            return []
        finally:
            if self.cursor:
                self.cursor.close()
