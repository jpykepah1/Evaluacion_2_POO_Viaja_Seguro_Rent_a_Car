from conex.conn import Conex
from modelo.cliente import Cliente

class DaoCliente:
    def __init__(self):
        self.conex = Conex()
        self.conn = self.conex.getConex()
        self.cursor = None

    def agregarCliente(self, cliente):
        sql = "INSERT INTO cliente (run, nombre, apellido, direccion, telefono) VALUES (%s, %s, %s, %s, %s)"
        try:
            self.cursor = self.conn.cursor()
            self.cursor.execute(sql, (cliente.getRun(), cliente.getNombre(), cliente.getApellido(), cliente.getDireccion(), cliente.getTelefono()))
            self.conn.commit()
            return True
        except Exception as e:
            print(f"Error al agregar cliente: {e}")
            return False
        finally:
            if self.cursor:
                self.cursor.close()

    def buscarCliente(self, run):
        sql = "SELECT * FROM cliente WHERE run = %s"
        try:
            self.cursor = self.conn.cursor()
            self.cursor.execute(sql, (run,))
            resultado = self.cursor.fetchone()
            if resultado:
                return Cliente(resultado[1], resultado[2], resultado[3], resultado[4], resultado[5], resultado[0], resultado[6])
            return None
        except Exception as e:
            print(f"Error al buscar cliente: {e}")
            return None
        finally:
            if self.cursor:
                self.cursor.close()

    def actualizarCliente(self, cliente):
        sql = "UPDATE cliente SET nombre = %s, apellido = %s, direccion = %s, telefono = %s WHERE run = %s"
        try:
            self.cursor = self.conn.cursor()
            self.cursor.execute(sql, (cliente.getNombre(), cliente.getApellido(), cliente.getDireccion(), cliente.getTelefono(), cliente.getRun()))
            self.conn.commit()
            return True
        except Exception as e:
            print(f"Error al actualizar cliente: {e}")
            return False
        finally:
            if self.cursor:
                self.cursor.close()

    def eliminarCliente(self, run):
        sql = "DELETE FROM cliente WHERE run = %s"
        try:
            self.cursor = self.conn.cursor()
            self.cursor.execute(sql, (run,))
            self.conn.commit()
            return True
        except Exception as e:
            print(f"Error al eliminar cliente: {e}")
            return False
        finally:
            if self.cursor:
                self.cursor.close()

    def listarClientes(self):
        sql = "SELECT * FROM cliente ORDER BY nombre, apellido"
        try:
            self.cursor = self.conn.cursor()
            self.cursor.execute(sql)
            resultados = self.cursor.fetchall()
            clientes = []
            for resultado in resultados:
                cliente = Cliente(resultado[1], resultado[2], resultado[3], resultado[4], resultado[5], resultado[0], resultado[6])
                clientes.append(cliente)
            return clientes
        except Exception as e:
            print(f"Error al listar clientes: {e}")
            return []
        finally:
            if self.cursor:
                self.cursor.close()