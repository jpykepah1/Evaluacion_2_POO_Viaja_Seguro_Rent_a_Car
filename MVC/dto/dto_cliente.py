from dao.dao_cliente import DaoCliente
from modelo.cliente import Cliente

class ClienteDTO:
    def agregarCliente(self, run, nombre, apellido, direccion, telefono):
        daocliente = DaoCliente()
        return daocliente.agregarCliente(Cliente(run, nombre, apellido, direccion, telefono))

    def buscarCliente(self, run):
        daocliente = DaoCliente()
        return daocliente.buscarCliente(run)

    def actualizarCliente(self, run, nombre, apellido, direccion, telefono):
        daocliente = DaoCliente()
        return daocliente.actualizarCliente(Cliente(run, nombre, apellido, direccion, telefono))

    def eliminarCliente(self, run):
        daocliente = DaoCliente()
        return daocliente.eliminarCliente(run)

    def listarClientes(self):
        daocliente = DaoCliente()
        return daocliente.listarClientes()