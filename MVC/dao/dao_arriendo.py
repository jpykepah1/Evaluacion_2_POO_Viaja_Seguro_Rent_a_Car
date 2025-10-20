from conex.conn import Conex
from modelo.arriendo import Arriendo

class DaoArriendo:
    def __init__(self):
        self.conex = Conex()
        self.conn = self.conex.getConex()
        self.cursor = None

    def agregarArriendo(self, arriendo):
        sql = """INSERT INTO arriendo (id_vehiculo, id_cliente, id_empleado, fecha_inicio, fecha_fin, costo_total, estado) 
                 VALUES (%s, %s, %s, %s, %s, %s, %s)"""
        try:
            self.cursor = self.conn.cursor()
            self.cursor.execute(sql, (arriendo.getIdVehiculo(), arriendo.getIdCliente(), arriendo.getIdEmpleado(), 
                                     arriendo.getFechaInicio(), arriendo.getFechaFin(), arriendo.getCostoTotal(), 
                                     arriendo.getEstado()))
            self.conn.commit()
            return True
        except Exception as e:
            print(f"Error al agregar arriendo: {e}")
            return False
        finally:
            if self.cursor:
                self.cursor.close()

    def buscarArriendo(self, id_arriendo):
        sql = "SELECT * FROM arriendo WHERE id_arriendo = %s"
        try:
            self.cursor = self.conn.cursor()
            self.cursor.execute(sql, (id_arriendo,))
            resultado = self.cursor.fetchone()
            if resultado:
                return Arriendo(resultado[1], resultado[2], resultado[3], resultado[4], 
                              resultado[5], resultado[6], resultado[7], resultado[0], resultado[8])
            return None
        except Exception as e:
            print(f"Error al buscar arriendo: {e}")
            return None
        finally:
            if self.cursor:
                self.cursor.close()

    def actualizarArriendo(self, arriendo):
        sql = """UPDATE arriendo SET id_vehiculo = %s, id_cliente = %s, id_empleado = %s, 
                 fecha_inicio = %s, fecha_fin = %s, costo_total = %s, estado = %s 
                 WHERE id_arriendo = %s"""
        try:
            self.cursor = self.conn.cursor()
            self.cursor.execute(sql, (arriendo.getIdVehiculo(), arriendo.getIdCliente(), arriendo.getIdEmpleado(), 
                                     arriendo.getFechaInicio(), arriendo.getFechaFin(), arriendo.getCostoTotal(), 
                                     arriendo.getEstado(), arriendo.getIdArriendo()))
            self.conn.commit()
            return True
        except Exception as e:
            print(f"Error al actualizar arriendo: {e}")
            return False
        finally:
            if self.cursor:
                self.cursor.close()

    def eliminarArriendo(self, id_arriendo):
        sql = "DELETE FROM arriendo WHERE id_arriendo = %s"
        try:
            self.cursor = self.conn.cursor()
            self.cursor.execute(sql, (id_arriendo,))
            self.conn.commit()
            return True
        except Exception as e:
            print(f"Error al eliminar arriendo: {e}")
            return False
        finally:
            if self.cursor:
                self.cursor.close()

    def listarArriendos(self):
        sql = """SELECT a.*, v.patente, v.marca, v.modelo, c.nombre, c.apellido 
                 FROM arriendo a
                 JOIN vehiculo v ON a.id_vehiculo = v.id_vehiculo
                 JOIN cliente c ON a.id_cliente = c.id_cliente
                 ORDER BY a.fecha_inicio DESC"""
        try:
            self.cursor = self.conn.cursor()
            self.cursor.execute(sql)
            resultados = self.cursor.fetchall()
            arriendos = []
            for resultado in resultados:
                arriendo = Arriendo(resultado[1], resultado[2], resultado[3], resultado[4], 
                                  resultado[5], resultado[6], resultado[7], resultado[0], resultado[8])
                # Agregar información adicional para mostrar
                arriendo.info_vehiculo = f"{resultado[9]} - {resultado[10]} {resultado[11]}"
                arriendo.info_cliente = f"{resultado[12]} {resultado[13]}"
                arriendos.append(arriendo)
            return arriendos
        except Exception as e:
            print(f"Error al listar arriendos: {e}")
            return []
        finally:
            if self.cursor:
                self.cursor.close()

    def listarArriendosPorFecha(self, fecha):
        sql = """SELECT a.*, v.patente, v.marca, v.modelo, c.nombre, c.apellido 
                 FROM arriendo a
                 JOIN vehiculo v ON a.id_vehiculo = v.id_vehiculo
                 JOIN cliente c ON a.id_cliente = c.id_cliente
                 WHERE a.fecha_inicio = %s OR a.fecha_fin = %s
                 ORDER BY a.fecha_inicio"""
        try:
            self.cursor = self.conn.cursor()
            self.cursor.execute(sql, (fecha, fecha))
            resultados = self.cursor.fetchall()
            arriendos = []
            for resultado in resultados:
                arriendo = Arriendo(resultado[1], resultado[2], resultado[3], resultado[4], 
                                  resultado[5], resultado[6], resultado[7], resultado[0], resultado[8])
                arriendo.info_vehiculo = f"{resultado[9]} - {resultado[10]} {resultado[11]}"
                arriendo.info_cliente = f"{resultado[12]} {resultado[13]}"
                arriendos.append(arriendo)
            return arriendos
        except Exception as e:
            print(f"Error al listar arriendos por fecha: {e}")
            return []
        finally:
            if self.cursor:
                self.cursor.close()
