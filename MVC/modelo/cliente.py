from modelo.persona import Persona
from datetime import datetime
from typing import List, Optional, ClassVar

class Cliente(Persona):
    """
    Representa a un cliente del sistema de arriendos.
    
    Hereda de Persona y añade información de contacto como dirección y teléfono.
    
    Attributes:
        _lista_clientes (ClassVar[List['Cliente']]): Lista estática de todos los clientes
    """
    _lista_clientes: ClassVar[List['Cliente']] = []
    
    def __init__(self, run: str = "", nombre: str = "", apellido: str = "", 
                 direccion: str = "", telefono: str = "", id_cliente: Optional[int] = None, 
                 create_time: Optional[datetime] = None) -> None:
        """
        Inicializa una nueva instancia de Cliente.
        
        Args:
            run (str): RUN del cliente en formato 12345678-9
            nombre (str): Nombre del cliente
            apellido (str): Apellido del cliente
            direccion (str): Dirección de contacto del cliente
            telefono (str): Teléfono de contacto del cliente (9 dígitos)
            id_cliente (Optional[int]): Identificador único en base de datos
            create_time (Optional[datetime]): Fecha y hora de creación del registro
        """
        super().__init__(run, nombre, apellido)
        self._direccion = direccion
        self._telefono = telefono
        self._id_cliente = id_cliente
        self._create_time = create_time or datetime.now()
    
    def mostrar_info(self) -> str:
        """
        Proporciona una representación en string de la información del cliente.
        
        Returns:
            str: Cadena con nombre, apellido y teléfono del cliente
            
        Example:
            >>> cliente = Cliente(nombre="Juan", apellido="Pérez", telefono="912345678")
            >>> cliente.mostrar_info()
            'Cliente: Juan Pérez - Tel: 912345678'
        """
        return f"Cliente: {self.getNombre()} {self.getApellido()} - Tel: {self._telefono}"
    
    # Getters y Setters con type hints
    def getDireccion(self) -> str:
        """Obtiene la dirección del cliente."""
        return self._direccion
    
    def setDireccion(self, direccion: str) -> None:
        """Establece la dirección del cliente."""
        self._direccion = direccion
    
    def getTelefono(self) -> str:
        """Obtiene el teléfono del cliente."""
        return self._telefono
    
    def setTelefono(self, telefono: str) -> None:
        """Establece el teléfono del cliente."""
        self._telefono = telefono
    
    def getIdCliente(self) -> Optional[int]:
        """Obtiene el ID único del cliente en base de datos."""
        return self._id_cliente
    
    def setIdCliente(self, id_cliente: int) -> None:
        """Establece el ID único del cliente."""
        self._id_cliente = id_cliente
    
    @classmethod
    def getListaClientes(cls) -> List['Cliente']:
        """Obtiene la lista estática de todos los clientes."""
        return cls._lista_clientes
    
    def __str__(self) -> str:
        """Representación en string del cliente."""
        return f"{self.getNombre()} {self.getApellido()} - {self._telefono}"
