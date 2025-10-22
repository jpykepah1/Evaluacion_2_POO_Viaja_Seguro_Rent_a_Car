from dao.dao_arriendo import DaoArriendo
from modelo.arriendo import Arriendo
from typing import Optional, List

class ArriendoDTO:
    """
    Data Transfer Object para la entidad Arriendo.
    
    Se encarga de la transferencia de datos entre la capa de negocio
    y la capa de persistencia para los arriendos.
    """

    def agregarArriendo(self, id_vehiculo: int, id_cliente: int, id_empleado: int, 
                       fecha_inicio: str, fecha_fin: str, costo_total: float, 
                       estado: str = "activo") -> bool:
        """
        Agrega un nuevo arriendo al sistema.
        
        Args:
            id_vehiculo (int): ID del vehículo arrendado
            id_cliente (int): ID del cliente que arrienda
            id_empleado (int): ID del empleado que gestiona el arriendo
            fecha_inicio (str): Fecha de inicio del arriendo (YYYY-MM-DD)
            fecha_fin (str): Fecha de fin del arriendo (YYYY-MM-DD)
            costo_total (float): Costo total calculado del arriendo
            estado (str): Estado inicial del arriendo (default: "activo")
            
        Returns:
            bool: True si el arriendo fue agregado exitosamente, False en caso contrario
        """
        daoarriendo = DaoArriendo()
        return daoarriendo.agregarArriendo(Arriendo(
            id_vehiculo=id_vehiculo, 
            id_cliente=id_cliente, 
            id_empleado=id_empleado, 
            fecha_inicio=fecha_inicio, 
            fecha_fin=fecha_fin, 
            costo_total=costo_total, 
            estado=estado
        ))

    def buscarArriendo(self, id_arriendo: int) -> Optional[Arriendo]:
        """
        Busca un arriendo por su ID único.
        
        Args:
            id_arriendo (int): ID del arriendo a buscar
            
        Returns:
            Optional[Arriendo]: Instancia de Arriendo si se encuentra, None en caso contrario
        """
        daoarriendo = DaoArriendo()
        return daoarriendo.buscarArriendo(id_arriendo)

    def actualizarArriendo(self, id_arriendo: int, id_vehiculo: int, id_cliente: int, 
                          id_empleado: int, fecha_inicio: str, fecha_fin: str, 
                          costo_total: float, estado: str) -> bool:
        """
        Actualiza la información de un arriendo existente.
        
        Args:
            id_arriendo (int): ID del arriendo a actualizar
            id_vehiculo (int): Nuevo ID del vehículo arrendado
            id_cliente (int): Nuevo ID del cliente que arrienda
            id_empleado (int): Nuevo ID del empleado que gestiona el arriendo
            fecha_inicio (str): Nueva fecha de inicio del arriendo (YYYY-MM-DD)
            fecha_fin (str): Nueva fecha de fin del arriendo (YYYY-MM-DD)
            costo_total (float): Nuevo costo total del arriendo
            estado (str): Nuevo estado del arriendo
            
        Returns:
            bool: True si la actualización fue exitosa, False en caso contrario
        """
        daoarriendo = DaoArriendo()
        return daoarriendo.actualizarArriendo(Arriendo(
            id_vehiculo=id_vehiculo, 
            id_cliente=id_cliente, 
            id_empleado=id_empleado, 
            fecha_inicio=fecha_inicio, 
            fecha_fin=fecha_fin, 
            costo_total=costo_total, 
            estado=estado, 
            id_arriendo=id_arriendo
        ))

    def eliminarArriendo(self, id_arriendo: int) -> bool:
        """
        Elimina un arriendo del sistema.
        
        Args:
            id_arriendo (int): ID del arriendo a eliminar
            
        Returns:
            bool: True si la eliminación fue exitosa, False en caso contrario
        """
        daoarriendo = DaoArriendo()
        return daoarriendo.eliminarArriendo(id_arriendo)

    def listarArriendos(self) -> List[Arriendo]:
        """
        Obtiene la lista completa de arriendos del sistema.
        
        Returns:
            List[Arriendo]: Lista de todos los arriendos registrados
        """
        daoarriendo = DaoArriendo()
        return daoarriendo.listarArriendos()

    def listarArriendosPorFecha(self, fecha: str) -> List[Arriendo]:
        """
        Obtiene la lista de arriendos que coinciden con una fecha específica.
        
        Args:
            fecha (str): Fecha a buscar (YYYY-MM-DD)
            
        Returns:
            List[Arriendo]: Lista de arriendos que empiezan o terminan en la fecha especificada
        """
        daoarriendo = DaoArriendo()
        return daoarriendo.listarArriendosPorFecha(fecha)
