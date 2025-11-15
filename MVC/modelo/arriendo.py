from datetime import datetime
from typing import List, Optional, ClassVar

class Arriendo:
    """
    Representa un contrato de arriendo de un vehículo.
    
    Relaciona un vehículo, un cliente y un empleado en un período específico
    con un costo total calculado.
    
    Attributes:
        _lista_arriendos (ClassVar[List['Arriendo']]): Lista estática de todos los arriendos
    """
    _lista_arriendos: ClassVar[List['Arriendo']] = []
    
    def __init__(self, id_vehiculo: Optional[int] = None, id_cliente: Optional[int] = None, 
                 id_empleado: Optional[int] = None, fecha_inicio: Optional[str] = None, 
                 fecha_fin: Optional[str] = None, costo_total: float = 0.0, 
                 estado: str = "activo", id_arriendo: Optional[int] = None, 
                 create_time: Optional[datetime] = None, valor_uf_fecha: float = 0.0, 
                 fecha_uf_consulta: Optional[str] = None) -> None:
        """
        Inicializa una nueva instancia de Arriendo.
        
        Args:
            id_vehiculo (Optional[int]): ID del vehículo arrendado
            id_cliente (Optional[int]): ID del cliente que arrienda
            id_empleado (Optional[int]): ID del empleado que gestiona el arriendo
            fecha_inicio (Optional[str]): Fecha de inicio del arriendo (YYYY-MM-DD)
            fecha_fin (Optional[str]): Fecha de fin del arriendo (YYYY-MM-DD)
            costo_total (float): Costo total calculado del arriendo
            estado (str): Estado del arriendo (activo, finalizado, cancelado)
            id_arriendo (Optional[int]): Identificador único en base de datos
            create_time (Optional[datetime]): Fecha y hora de creación del registro
            valor_uf_fecha (float): Valor de la UF al momento del arriendo
            fecha_uf_consulta (Optional[str]): Fecha del indicador UF consultado
        """
        self._id_arriendo = id_arriendo
        self._id_vehiculo = id_vehiculo
        self._id_cliente = id_cliente
        self._id_empleado = id_empleado
        self._fecha_inicio = fecha_inicio
        self._fecha_fin = fecha_fin
        self._costo_total = costo_total
        self._estado = estado
        self._create_time = create_time or datetime.now()
        self._valor_uf_fecha = valor_uf_fecha
        self._fecha_uf_consulta = fecha_uf_consulta
    
    # Getters y Setters con type hints
    def getIdArriendo(self) -> Optional[int]:
        """Obtiene el ID único del arriendo en base de datos."""
        return self._id_arriendo
    
    def setIdArriendo(self, id_arriendo: int) -> None:
        """Establece el ID único del arriendo."""
        self._id_arriendo = id_arriendo
    
    def getIdVehiculo(self) -> Optional[int]:
        """Obtiene el ID del vehículo arrendado."""
        return self._id_vehiculo
    
    def setIdVehiculo(self, id_vehiculo: int) -> None:
        """Establece el ID del vehículo arrendado."""
        self._id_vehiculo = id_vehiculo
    
    def getIdCliente(self) -> Optional[int]:
        """Obtiene el ID del cliente que arrienda."""
        return self._id_cliente
    
    def setIdCliente(self, id_cliente: int) -> None:
        """Establece el ID del cliente que arrienda."""
        self._id_cliente = id_cliente
    
    def getIdEmpleado(self) -> Optional[int]:
        """Obtiene el ID del empleado que gestiona el arriendo."""
        return self._id_empleado
    
    def setIdEmpleado(self, id_empleado: int) -> None:
        """Establece el ID del empleado que gestiona el arriendo."""
        self._id_empleado = id_empleado
    
    def getFechaInicio(self) -> Optional[str]:
        """Obtiene la fecha de inicio del arriendo."""
        return self._fecha_inicio
    
    def setFechaInicio(self, fecha_inicio: str) -> None:
        """Establece la fecha de inicio del arriendo."""
        self._fecha_inicio = fecha_inicio
    
    def getFechaFin(self) -> Optional[str]:
        """Obtiene la fecha de fin del arriendo."""
        return self._fecha_fin
    
    def setFechaFin(self, fecha_fin: str) -> None:
        """Establece la fecha de fin del arriendo."""
        self._fecha_fin = fecha_fin
    
    def getCostoTotal(self) -> float:
        """Obtiene el costo total del arriendo."""
        return self._costo_total
    
    def setCostoTotal(self, costo_total: float) -> None:
        """Establece el costo total del arriendo."""
        self._costo_total = costo_total
    
    def getEstado(self) -> str:
        """Obtiene el estado actual del arriendo."""
        return self._estado
    
    def setEstado(self, estado: str) -> None:
        """Establece el estado actual del arriendo."""
        self._estado = estado
    
    def getCreateTime(self) -> Optional[datetime]:
        """Obtiene la fecha y hora de creación del registro."""
        return self._create_time
    
    def getValorUfFecha(self) -> float:
        """Obtiene el valor de la UF al momento del arriendo."""
        return self._valor_uf_fecha
    
    def setValorUfFecha(self, valor_uf_fecha: float) -> None:
        """Establece el valor de la UF."""
        self._valor_uf_fecha = valor_uf_fecha
    
    def getFechaUfConsulta(self) -> Optional[str]:
        """Obtiene la fecha del indicador UF consultado."""
        return self._fecha_uf_consulta
    
    def setFechaUfConsulta(self, fecha_uf_consulta: str) -> None:
        """Establece la fecha del indicador UF."""
        self._fecha_uf_consulta = fecha_uf_consulta
    
    @classmethod
    def getListaArriendos(cls) -> List['Arriendo']:
        """Obtiene la lista estática de todos los arriendos."""
        return cls._lista_arriendos
    
    def __str__(self) -> str:
        """Representación en string del arriendo."""
        return f"Arriendo #{self._id_arriendo}: ${self._costo_total} - {self._estado}"
