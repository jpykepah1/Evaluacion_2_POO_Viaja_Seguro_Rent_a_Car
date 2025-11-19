from conex.conn import Conex
from modelo.arriendo import Arriendo
import logging
from typing import Optional, List
import pymysql

logger = logging.getLogger(__name__)

class DaoArriendo:
    """
    Data Access Object para la entidad Arriendo.
    
    Proporciona métodos para realizar operaciones CRUD en la tabla 'arriendo'
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

    def agregarArriendo(self, arriendo: Arriendo) -> bool:
        """
        Inserta un nuevo arriendo en la base de datos.
        
        Args:
            arriendo (Arriendo): Instancia de Arriendo con los datos a insertar
            
        Returns:
            bool: True si la inserción fue exitosa, False en caso contrario
            
        Raises:
            pymysql.Error: Si ocurre un error de integridad referencial
        """
        sql = """INSERT INTO arriendo (id_vehiculo, id_cliente, id_empleado, fecha_inicio, fecha_fin, costo_total, estado, valor_uf_fecha, fecha_uf_consulta) 
                 VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"""
        try:
            self.cursor = self.conn.cursor()
            self.cursor.execute(sql, (
                arriendo.getIdVehiculo(), 
                arriendo.getIdCliente(), 
                arriendo.getIdEmpleado(), 
                arriendo.getFechaInicio(), 
                arriendo.getFechaFin(), 
                arriendo.getCostoTotal(), 
                arriendo.getEstado(),
                arriendo.getValorUfFecha(),
                arriendo.getFechaUfConsulta()
            ))
            self.conn.commit()
            return True
        except Exception as e:
            logger.error("Error al agregar arriendo: %s", e)
            return False
        finally:
            if self.cursor:
                self.cursor.close()

    def buscarArriendo(self, id_arriendo: int) -> Optional[Arriendo]:
        """
        Busca un arriendo por su ID único.
        
        Args:
            id_arriendo (int): ID del arriendo a buscar
            
        Returns:
            Optional[Arriendo]: Instancia de Arriendo si se encuentra, None en caso contrario
        """
        sql = "SELECT id_arriendo, id_vehiculo, id_cliente, id_empleado, fecha_inicio, fecha_fin, costo_total, estado, create_time, valor_uf_fecha, fecha_uf_consulta FROM arriendo WHERE id_arriendo = %s"
        try:
            self.cursor = self.conn.cursor()
            self.cursor.execute(sql, (id_arriendo,))
            resultado = self.cursor.fetchone()
            if resultado:
                return Arriendo(
                    id_arriendo=int(resultado[0]),
                    id_vehiculo=int(resultado[1]) if resultado[1] is not None else None,
                    id_cliente=int(resultado[2]) if resultado[2] is not None else None,
                    id_empleado=int(resultado[3]) if resultado[3] is not None else None,
                    fecha_inicio=resultado[4],
                    fecha_fin=resultado[5],
                    costo_total=float(resultado[6]) if resultado[6] is not None else 0.0,
                    estado=resultado[7],
                    create_time=resultado[8],
                    valor_uf_fecha=float(resultado[9]) if resultado[9] is not None else 0.0,
                    fecha_uf_consulta=resultado[10]
                )
            return None
        except Exception as e:
            logger.error("Error al buscar arriendo: %s", e)
            return None
        finally:
            if self.cursor:
                self.cursor.close()

    def actualizarArriendo(self, arriendo: Arriendo) -> bool:
        """
        Actualiza los datos de un arriendo existente.
        
        Args:
            arriendo (Arriendo): Instancia de Arriendo con los datos actualizados
            
        Returns:
            bool: True si la actualización fue exitosa, False en caso contrario
        """
        sql = """UPDATE arriendo SET id_vehiculo = %s, id_cliente = %s, id_empleado = %s, 
                 fecha_inicio = %s, fecha_fin = %s, costo_total = %s, estado = %s, valor_uf_fecha = %s, fecha_uf_consulta = %s 
                 WHERE id_arriendo = %s"""
        try:
            self.cursor = self.conn.cursor()
            self.cursor.execute(sql, (
                arriendo.getIdVehiculo(), 
                arriendo.getIdCliente(), 
                arriendo.getIdEmpleado(), 
                arriendo.getFechaInicio(), 
                arriendo.getFechaFin(), 
                arriendo.getCostoTotal(), 
                arriendo.getEstado(),
                arriendo.getValorUfFecha(),
                arriendo.getFechaUfConsulta(),
                arriendo.getIdArriendo()
            ))
            self.conn.commit()
            return True
        except Exception as e:
            logger.error("Error al actualizar arriendo: %s", e)
            return False
        finally:
            if self.cursor:
                self.cursor.close()

    def eliminarArriendo(self, id_arriendo: int) -> bool:
        """
        Elimina un arriendo de la base de datos.
        
        Args:
            id_arriendo (int): ID del arriendo a eliminar
            
        Returns:
            bool: True si la eliminación fue exitosa, False en caso contrario
        """
        sql = "DELETE FROM arriendo WHERE id_arriendo = %s"
        try:
            self.cursor = self.conn.cursor()
            self.cursor.execute(sql, (id_arriendo,))
            self.conn.commit()
            return True
        except Exception as e:
            logger.error("Error al eliminar arriendo: %s", e)
            return False
        finally:
            if self.cursor:
                self.cursor.close()

    def listarArriendos(self) -> List[Arriendo]:
        """
        Obtiene todos los arriendos registrados en el sistema.
        
        Returns:
            List[Arriendo]: Lista de objetos Arriendo con todos los arriendos
            
        Note:
            Retorna una lista vacía si no hay arriendos o si ocurre un error
        """
        sql = """SELECT a.id_arriendo, a.id_vehiculo, a.id_cliente, a.id_empleado,
                 a.fecha_inicio, a.fecha_fin, a.costo_total, a.estado, a.create_time,
                 a.valor_uf_fecha, a.fecha_uf_consulta,
                 v.patente, v.marca, v.modelo,
                 c.nombre, c.apellido
             FROM arriendo a
             JOIN vehiculo v ON a.id_vehiculo = v.id_vehiculo
             JOIN cliente c ON a.id_cliente = c.id_cliente
             ORDER BY a.fecha_inicio DESC"""
        try:
            self.cursor = self.conn.cursor()
            self.cursor.execute(sql)
            resultados = self.cursor.fetchall()
            arriendos: List[Arriendo] = []
            for resultado in resultados:
                arriendo = Arriendo(
                    id_arriendo=int(resultado[0]),
                    id_vehiculo=int(resultado[1]) if resultado[1] is not None else None,
                    id_cliente=int(resultado[2]) if resultado[2] is not None else None,
                    id_empleado=int(resultado[3]) if resultado[3] is not None else None,
                    fecha_inicio=resultado[4],
                    fecha_fin=resultado[5],
                    costo_total=float(resultado[6]) if resultado[6] is not None else 0.0,
                    estado=resultado[7],
                    create_time=resultado[8],
                    valor_uf_fecha=float(resultado[9]) if resultado[9] is not None else 0.0,
                    fecha_uf_consulta=resultado[10]
                )
                # Nota: no agregar atributos de presentación al modelo aquí.
                # La información de vehículo/cliente para presentación debe armarse
                # en la capa DTO o en el controlador.
                arriendos.append(arriendo)
            return arriendos
        except Exception as e:
            logger.error("Error al listar arriendos: %s", e)
            return []
        finally:
            if self.cursor:
                self.cursor.close()

    def listarArriendosConRelacion(self) -> List[dict]:
        """
        Obtiene todos los arriendos junto con campos seleccionados de vehiculo y cliente
        en una sola consulta (evita consultas por cada arriendo).

        Retorna lista de dicts con claves: 'arriendo', 'veh_patente', 'veh_marca', 'veh_modelo', 'cli_nombre', 'cli_apellido'
        """
        sql = """SELECT a.id_arriendo, a.id_vehiculo, a.id_cliente, a.id_empleado,
                 a.fecha_inicio, a.fecha_fin, a.costo_total, a.estado, a.create_time,
                 a.valor_uf_fecha, a.fecha_uf_consulta,
                 v.patente, v.marca, v.modelo,
                 c.nombre, c.apellido
             FROM arriendo a
             JOIN vehiculo v ON a.id_vehiculo = v.id_vehiculo
             JOIN cliente c ON a.id_cliente = c.id_cliente
             ORDER BY a.fecha_inicio DESC"""
        try:
            self.cursor = self.conn.cursor()
            self.cursor.execute(sql)
            resultados = self.cursor.fetchall()
            lista: List[dict] = []
            for resultado in resultados:
                arriendo = Arriendo(
                    id_arriendo=int(resultado[0]),
                    id_vehiculo=int(resultado[1]) if resultado[1] is not None else None,
                    id_cliente=int(resultado[2]) if resultado[2] is not None else None,
                    id_empleado=int(resultado[3]) if resultado[3] is not None else None,
                    fecha_inicio=resultado[4],
                    fecha_fin=resultado[5],
                    costo_total=float(resultado[6]) if resultado[6] is not None else 0.0,
                    estado=resultado[7],
                    create_time=resultado[8],
                    valor_uf_fecha=float(resultado[9]) if resultado[9] is not None else 0.0,
                    fecha_uf_consulta=resultado[10]
                )
                lista.append({
                    'arriendo': arriendo,
                    'veh_patente': resultado[11],
                    'veh_marca': resultado[12],
                    'veh_modelo': resultado[13],
                    'cli_nombre': resultado[14],
                    'cli_apellido': resultado[15]
                })
            return lista
        except Exception as e:
            logger.error("Error al listar arriendos con relación: %s", e)
            return []
        finally:
            if self.cursor:
                self.cursor.close()

    def listarArriendosPorFechaConRelacion(self, fecha: str) -> List[dict]:
        """
        Obtiene arriendos que coinciden con la fecha junto con campos del vehiculo y cliente.
        """
        sql = """SELECT a.id_arriendo, a.id_vehiculo, a.id_cliente, a.id_empleado,
                 a.fecha_inicio, a.fecha_fin, a.costo_total, a.estado, a.create_time,
                 a.valor_uf_fecha, a.fecha_uf_consulta,
                 v.patente, v.marca, v.modelo,
                 c.nombre, c.apellido
             FROM arriendo a
             JOIN vehiculo v ON a.id_vehiculo = v.id_vehiculo
             JOIN cliente c ON a.id_cliente = c.id_cliente
             WHERE a.fecha_inicio = %s OR a.fecha_fin = %s
             ORDER BY a.fecha_inicio"""
        try:
            self.cursor = self.conn.cursor()
            self.cursor.execute(sql, (fecha, fecha))
            resultados = self.cursor.fetchall()
            lista: List[dict] = []
            for resultado in resultados:
                arriendo = Arriendo(
                    id_arriendo=int(resultado[0]),
                    id_vehiculo=int(resultado[1]) if resultado[1] is not None else None,
                    id_cliente=int(resultado[2]) if resultado[2] is not None else None,
                    id_empleado=int(resultado[3]) if resultado[3] is not None else None,
                    fecha_inicio=resultado[4],
                    fecha_fin=resultado[5],
                    costo_total=float(resultado[6]) if resultado[6] is not None else 0.0,
                    estado=resultado[7],
                    create_time=resultado[8],
                    valor_uf_fecha=float(resultado[9]) if resultado[9] is not None else 0.0,
                    fecha_uf_consulta=resultado[10]
                )
                lista.append({
                    'arriendo': arriendo,
                    'veh_patente': resultado[11],
                    'veh_marca': resultado[12],
                    'veh_modelo': resultado[13],
                    'cli_nombre': resultado[14],
                    'cli_apellido': resultado[15]
                })
            return lista
        except Exception as e:
            logger.error("Error al listar arriendos por fecha con relación: %s", e)
            return []
        finally:
            if self.cursor:
                self.cursor.close()

    def listarArriendosPorFecha(self, fecha: str) -> List[Arriendo]:
        """
        Obtiene los arriendos que coinciden con una fecha específica.
        
        Args:
            fecha (str): Fecha a buscar en formato YYYY-MM-DD
            
        Returns:
            List[Arriendo]: Lista de arriendos que empiezan o terminan en la fecha especificada
            
        Note:
            Retorna una lista vacía si no hay coincidencias o si ocurre un error
        """
        sql = """SELECT a.id_arriendo, a.id_vehiculo, a.id_cliente, a.id_empleado,
                 a.fecha_inicio, a.fecha_fin, a.costo_total, a.estado, a.create_time,
                 a.valor_uf_fecha, a.fecha_uf_consulta,
                 v.patente, v.marca, v.modelo,
                 c.nombre, c.apellido
             FROM arriendo a
             JOIN vehiculo v ON a.id_vehiculo = v.id_vehiculo
             JOIN cliente c ON a.id_cliente = c.id_cliente
             WHERE a.fecha_inicio = %s OR a.fecha_fin = %s
             ORDER BY a.fecha_inicio"""
        try:
            self.cursor = self.conn.cursor()
            self.cursor.execute(sql, (fecha, fecha))
            resultados = self.cursor.fetchall()
            arriendos: List[Arriendo] = []
            for resultado in resultados:
                arriendo = Arriendo(
                    id_arriendo=int(resultado[0]),
                    id_vehiculo=int(resultado[1]) if resultado[1] is not None else None,
                    id_cliente=int(resultado[2]) if resultado[2] is not None else None,
                    id_empleado=int(resultado[3]) if resultado[3] is not None else None,
                    fecha_inicio=resultado[4],
                    fecha_fin=resultado[5],
                    costo_total=float(resultado[6]) if resultado[6] is not None else 0.0,
                    estado=resultado[7],
                    create_time=resultado[8],
                    valor_uf_fecha=float(resultado[9]) if resultado[9] is not None else 0.0,
                    fecha_uf_consulta=resultado[10]
                )
                # Nota: no agregar atributos de presentación al modelo aquí.
                # Devolver solo el objeto Arriendo; la capa superior se encargará
                # de obtener y formatear los datos relacionados.
                arriendos.append(arriendo)
            return arriendos
        except Exception as e:
            logger.error("Error al listar arriendos por fecha: %s", e)
            return []
        finally:
            if self.cursor:
                self.cursor.close()
