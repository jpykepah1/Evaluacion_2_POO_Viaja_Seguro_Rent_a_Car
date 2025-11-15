from datetime import datetime
from typing import List, Optional, ClassVar

class Vehiculo:
    """
    Representa un vehículo disponible para arriendo.
    
    Contiene información del vehículo como patente, marca, modelo, año,
    precio de arriendo y estado actual.
    
    Attributes:
        _lista_vehiculos (ClassVar[List['Vehiculo']]): Lista estática de todos los vehículos
    """
    _lista_vehiculos: ClassVar[List['Vehiculo']] = []
    
    def __init__(self, patente: str = "", marca: str = "", modelo: str = "", 
                 año: int = 0, precio_diario: float = 0.0, estado: str = "disponible", 
                 id_vehiculo: Optional[int] = None, create_time: Optional[datetime] = None) -> None:
        """
        Inicializa una nueva instancia de Vehiculo.
        
        Args:
            patente (str): Patente del vehículo (formato: ABCD12 o ABC123)
            marca (str): Marca del vehículo (ej: Toyota, Chevrolet)
            modelo (str): Modelo del vehículo (ej: Corolla, Cruze)
            año (int): Año de fabricación del vehículo
            precio_diario (float): Precio de arriendo por día en pesos chilenos
            estado (str): Estado actual del vehículo (disponible, arrendado, mantencion)
            id_vehiculo (Optional[int]): Identificador único en base de datos
            create_time (Optional[datetime]): Fecha y hora de creación del registro
        """
        self._patente = patente
        self._marca = marca
        self._modelo = modelo
        self._año = año
        self._precio_diario = precio_diario
        self._estado = estado
        self._id_vehiculo = id_vehiculo
        self._create_time = create_time or datetime.now()
    
    # Getters y Setters con type hints
    def getPatente(self) -> str:
        """Obtiene la patente del vehículo."""
        return self._patente
    
    def setPatente(self, patente: str) -> None:
        """Establece la patente del vehículo."""
        self._patente = patente
    
    def getMarca(self) -> str:
        """Obtiene la marca del vehículo."""
        return self._marca
    
    def setMarca(self, marca: str) -> None:
        """Establece la marca del vehículo."""
        self._marca = marca
    
    def getModelo(self) -> str:
        """Obtiene el modelo del vehículo."""
        return self._modelo
    
    def setModelo(self, modelo: str) -> None:
        """Establece el modelo del vehículo."""
        self._modelo = modelo
    
    def getAño(self) -> int:
        """Obtiene el año de fabricación del vehículo."""
        return self._año
    
    def setAño(self, año: int) -> None:
        """Establece el año de fabricación del vehículo."""
        self._año = año
    
    def getPrecioDiario(self) -> float:
        """Obtiene el precio de arriendo diario del vehículo."""
        return self._precio_diario
    
    def setPrecioDiario(self, precio_diario: float) -> None:
        """Establece el precio de arriendo diario del vehículo."""
        self._precio_diario = precio_diario
    
    def getEstado(self) -> str:
        """Obtiene el estado actual del vehículo."""
        return self._estado
    
    def setEstado(self, estado: str) -> None:
        """Establece el estado actual del vehículo."""
        self._estado = estado
    
    def getIdVehiculo(self) -> Optional[int]:
        """Obtiene el ID único del vehículo en base de datos."""
        return self._id_vehiculo
    
    def setIdVehiculo(self, id_vehiculo: int) -> None:
        """Establece el ID único del vehículo."""
        self._id_vehiculo = id_vehiculo
    
    @classmethod
    def getListaVehiculos(cls) -> List['Vehiculo']:
        """Obtiene la lista estática de todos los vehículos."""
        return cls._lista_vehiculos
    
    def __str__(self) -> str:
        """Representación en string del vehículo."""
        return f"{self._marca} {self._modelo} ({self._patente}) - {self._estado} - ${self._precio_diario}/día"
