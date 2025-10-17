from dao.dao_vehiculo import DaoVehiculo
from modelo.vehiculo import Vehiculo

class VehiculoDTO:
    def agregarVehiculo(self, patente, marca, modelo, año, precio_diario, estado="disponible"):
        daovehiculo = DaoVehiculo()
        return daovehiculo.agregarVehiculo(Vehiculo(patente, marca, modelo, año, precio_diario, estado))

    def buscarVehiculo(self, patente):
        daovehiculo = DaoVehiculo()
        return daovehiculo.buscarVehiculo(patente)

    def buscarVehiculoPorId(self, id_vehiculo):
        daovehiculo = DaoVehiculo()
        return daovehiculo.buscarVehiculoPorId(id_vehiculo)

    def actualizarVehiculo(self, patente, marca, modelo, año, precio_diario, estado):
        daovehiculo = DaoVehiculo()
        return daovehiculo.actualizarVehiculo(Vehiculo(patente, marca, modelo, año, precio_diario, estado))

    def eliminarVehiculo(self, patente):
        daovehiculo = DaoVehiculo()
        return daovehiculo.eliminarVehiculo(patente)

    def listarVehiculos(self):
        daovehiculo = DaoVehiculo()
        return daovehiculo.listarVehiculos()

    def listarVehiculosDisponibles(self):
        daovehiculo = DaoVehiculo()
        return daovehiculo.listarVehiculosDisponibles()