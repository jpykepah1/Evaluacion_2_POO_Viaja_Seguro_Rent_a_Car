from conex.conn import Conex
from modelo.vehiculo import Vehiculo

class DaoVehiculo:
    def __init__(self):
        self.conex = Conex()
        self.conn = self.conex.getConex()
        self.cursor = None

    def agregarVehiculo(self, vehiculo):
        sql = "INSERT INTO vehiculo (patente, marca, modelo, año, precio_diario, estado) VALUES (%s, %s, %s, %s, %s, %s)"
        try:
            self.cursor = self.conn.cursor()
            self.cursor.execute(sql, (vehiculo.getPatente(), vehiculo.getMarca(), vehiculo.getModelo(), 
                                    vehiculo.getAño(), vehiculo.getPrecioDiario(), vehiculo.getEstado()))
            self.conn.commit()
            return True
        except Exception as e:
            print(f"Error al agregar vehículo: {e}")
            return False
        finally:
            if self.cursor:
                self.cursor.close()

    def buscarVehiculo(self, patente):
        sql = "SELECT * FROM vehiculo WHERE patente = %s"
        try:
            self.cursor = self.conn.cursor()
            self.cursor.execute(sql, (patente,))
            resultado = self.cursor.fetchone()
            if resultado:
                return Vehiculo(resultado[1], resultado[2], resultado[3], resultado[4], 
                              resultado[5], resultado[6], resultado[0], resultado[7])
            return None
        except Exception as e:
            print(f"Error al buscar vehículo: {e}")
            return None
        finally:
            if self.cursor:
                self.cursor.close()

    def buscarVehiculoPorId(self, id_vehiculo):
        sql = "SELECT * FROM vehiculo WHERE id_vehiculo = %s"
        try:
            self.cursor = self.conn.cursor()
            self.cursor.execute(sql, (id_vehiculo,))
            resultado = self.cursor.fetchone()
            if resultado:
                return Vehiculo(resultado[1], resultado[2], resultado[3], resultado[4], 
                              resultado[5], resultado[6], resultado[0], resultado[7])
            return None
        except Exception as e:
            print(f"Error al buscar vehículo por ID: {e}")
            return None
        finally:
            if self.cursor:
                self.cursor.close()

    def actualizarVehiculo(self, vehiculo):
        sql = "UPDATE vehiculo SET marca = %s, modelo = %s, año = %s, precio_diario = %s, estado = %s WHERE patente = %s"
        try:
            self.cursor = self.conn.cursor()
            self.cursor.execute(sql, (vehiculo.getMarca(), vehiculo.getModelo(), vehiculo.getAño(), 
                                    vehiculo.getPrecioDiario(), vehiculo.getEstado(), vehiculo.getPatente()))
            self.conn.commit()
            return True
        except Exception as e:
            print(f"Error al actualizar vehículo: {e}")
            return False
        finally:
            if self.cursor:
                self.cursor.close()

    def eliminarVehiculo(self, patente):
        sql = "DELETE FROM vehiculo WHERE patente = %s"
        try:
            self.cursor = self.conn.cursor()
            self.cursor.execute(sql, (patente,))
            self.conn.commit()
            return True
        except Exception as e:
            print(f"Error al eliminar vehículo: {e}")
            return False
        finally:
            if self.cursor:
                self.cursor.close()

    def listarVehiculos(self):
        sql = "SELECT * FROM vehiculo ORDER BY marca, modelo"
        try:
            self.cursor = self.conn.cursor()
            self.cursor.execute(sql)
            resultados = self.cursor.fetchall()
            vehiculos = []
            for resultado in resultados:
                vehiculo = Vehiculo(resultado[1], resultado[2], resultado[3], resultado[4], 
                                  resultado[5], resultado[6], resultado[0], resultado[7])
                vehiculos.append(vehiculo)
            return vehiculos
        except Exception as e:
            print(f"Error al listar vehículos: {e}")
            return []
        finally:
            if self.cursor:
                self.cursor.close()

    def listarVehiculosDisponibles(self):
        sql = "SELECT * FROM vehiculo WHERE estado = 'disponible' ORDER BY marca, modelo"
        try:
            self.cursor = self.conn.cursor()
            self.cursor.execute(sql)
            resultados = self.cursor.fetchall()
            vehiculos = []
            for resultado in resultados:
                vehiculo = Vehiculo(resultado[1], resultado[2], resultado[3], resultado[4], 
                                  resultado[5], resultado[6], resultado[0], resultado[7])
                vehiculos.append(vehiculo)
            return vehiculos
        except Exception as e:
            print(f"Error al listar vehículos disponibles: {e}")
            return []
        finally:
            if self.cursor:
                self.cursor.close()
