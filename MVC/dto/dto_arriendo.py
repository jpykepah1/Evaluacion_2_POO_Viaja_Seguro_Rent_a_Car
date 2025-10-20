from dao.dao_arriendo import DaoArriendo
from modelo.arriendo import Arriendo

class ArriendoDTO:
    def agregarArriendo(self, id_vehiculo, id_cliente, id_empleado, fecha_inicio, fecha_fin, costo_total, estado="activo"):
        daoarriendo = DaoArriendo()
        return daoarriendo.agregarArriendo(Arriendo(id_vehiculo, id_cliente, id_empleado, fecha_inicio, fecha_fin, costo_total, estado))

    def buscarArriendo(self, id_arriendo):
        daoarriendo = DaoArriendo()
        return daoarriendo.buscarArriendo(id_arriendo)

    def actualizarArriendo(self, id_arriendo, id_vehiculo, id_cliente, id_empleado, fecha_inicio, fecha_fin, costo_total, estado):
        daoarriendo = DaoArriendo()
        return daoarriendo.actualizarArriendo(Arriendo(id_vehiculo, id_cliente, id_empleado, fecha_inicio, fecha_fin, costo_total, estado, id_arriendo))

    def eliminarArriendo(self, id_arriendo):
        daoarriendo = DaoArriendo()
        return daoarriendo.eliminarArriendo(id_arriendo)

    def listarArriendos(self):
        daoarriendo = DaoArriendo()
        return daoarriendo.listarArriendos()

    def listarArriendosPorFecha(self, fecha):
        daoarriendo = DaoArriendo()
        return daoarriendo.listarArriendosPorFecha(fecha)
