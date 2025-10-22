from dao.dao_vehiculo import DaoVehiculo
from modelo.vehiculo import Vehiculo
from typing import Optional, List

class VehiculoDTO:
    """
    Data Transfer Object para la entidad Vehiculo.
    
    Se encarga de la transferencia de datos entre la capa de negocio
    y la capa de persistencia para los vehículos.
    """

    def agregarVehiculo(self, patente: str, marca: str, modelo: str, 
                       año: int, precio_diario: float, estado: str = "disponible") -> bool:
        """
        Agrega un nuevo vehículo al sistema.
        
        Args:
            patente (str): Patente del vehículo
            marca (str): Marca del vehículo
            modelo (str): Modelo del vehículo
            año (int): Año de fabricación del vehículo
            precio_diario (float): Precio de arriendo por día
            estado (str): Estado inicial del vehículo (default: "disponible")
            
        Returns:
            bool: True si el vehículo fue agregado exitosamente, False en caso contrario
        """
        daovehiculo = DaoVehiculo()
        return daovehiculo.agregarVehiculo(Vehiculo(
            patente=patente, 
            marca=marca, 
            modelo=modelo, 
            año=año, 
            precio_diario=precio_diario, 
            estado=estado
        ))

    def buscarVehiculo(self, patente: str) -> Optional[Vehiculo]:
        """
        Busca un vehículo por su patente.
        
        Args:
            patente (str): Patente del vehículo a buscar
            
        Returns:
            Optional[Vehiculo]: Instancia de Vehiculo si se encuentra, None en caso contrario
        """
        daovehiculo = DaoVehiculo()
        return daovehiculo.buscarVehiculo(patente)

    def buscarVehiculoPorId(self, id_vehiculo: int) -> Optional[Vehiculo]:
        """
        Busca un vehículo por su ID único.
        
        Args:
            id_vehiculo (int): ID del vehículo a buscar
            
        Returns:
            Optional[Vehiculo]: Instancia de Vehiculo si se encuentra, None en caso contrario
        """
        daovehiculo = DaoVehiculo()
        return daovehiculo.buscarVehiculoPorId(id_vehiculo)

    def actualizarVehiculo(self, patente: str, marca: str, modelo: str, 
                          año: int, precio_diario: float, estado: str) -> bool:
        """
        Actualiza la información de un vehículo existente.
        
        Args:
            patente (str): Patente del vehículo a actualizar
            marca (str): Nueva marca del vehículo
            modelo (str): Nuevo modelo del vehículo
            año (int): Nuevo año de fabricación del vehículo
            precio_diario (float): Nuevo precio de arriendo por día
            estado (str): Nuevo estado del vehículo
            
        Returns:
            bool: True si la actualización fue exitosa, False en caso contrario
        """
        daovehiculo = DaoVehiculo()
        return daovehiculo.actualizarVehiculo(Vehiculo(
            patente=patente, 
            marca=marca, 
            modelo=modelo, 
            año=año, 
            precio_diario=precio_diario, 
            estado=estado
        ))

    def eliminarVehiculo(self, patente: str) -> bool:
        """
        Elimina un vehículo del sistema.
        
        Args:
            patente (str): Patente del vehículo a eliminar
            
        Returns:
            bool: True si la eliminación fue exitosa, False en caso contrario
        """
        daovehiculo = DaoVehiculo()
        return daovehiculo.eliminarVehiculo(patente)

    def listarVehiculos(self) -> List[Vehiculo]:
        """
        Obtiene la lista completa de vehículos del sistema.
        
        Returns:
            List[Vehiculo]: Lista de todos los vehículos registrados
        """
        daovehiculo = DaoVehiculo()
        return daovehiculo.listarVehiculos()

    def listarVehiculosDisponibles(self) -> List[Vehiculo]:
        """
        Obtiene la lista de vehículos disponibles para arriendo.
        
        Returns:
            List[Vehiculo]: Lista de vehículos con estado 'disponible'
        """
        daovehiculo = DaoVehiculo()
        return daovehiculo.listarVehiculosDisponibles()
