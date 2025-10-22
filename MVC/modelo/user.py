from modelo.persona import Persona
from datetime import datetime
from typing import List, Optional, ClassVar

class User(Persona):
    """
    Representa a un empleado del sistema con credenciales de acceso.
    
    Hereda de Persona y añade funcionalidades específicas de usuario
    del sistema como contraseña, cargo y control de acceso.
    
    Attributes:
        _lista_users (ClassVar[List['User']]): Lista estática de todos los usuarios
    """
    _lista_users: ClassVar[List['User']] = []
    
    def __init__(self, run: str = "", nombre: str = "", apellido: str = "", 
                 password: str = "", cargo: str = "", id_empleado: Optional[int] = None, 
                 create_time: Optional[datetime] = None) -> None:
        """
        Inicializa una nueva instancia de User.
        
        Args:
            run (str): RUN del usuario en formato 12345678-9
            nombre (str): Nombre del usuario
            apellido (str): Apellido del usuario
            password (str): Contraseña (puede ser texto plano o hash)
            cargo (str): Cargo del usuario ('gerente' o 'empleado')
            id_empleado (Optional[int]): Identificador único en base de datos
            create_time (Optional[datetime]): Fecha y hora de creación del registro
        """
        super().__init__(run, nombre, apellido)
        self._password = password
        self._cargo = cargo
        self._id_empleado = id_empleado
        self._create_time = create_time or datetime.now()
    
    def mostrar_info(self) -> str:
        """
        Proporciona una representación en string de la información del usuario.
        
        Returns:
            str: Cadena con nombre, apellido y cargo del usuario
            
        Example:
            >>> user = User(nombre="Juan", apellido="Pérez", cargo="gerente")
            >>> user.mostrar_info()
            'Empleado: Juan Pérez - Cargo: gerente'
        """
        return f"Empleado: {self.getNombre()} {self.getApellido()} - Cargo: {self._cargo}"
    
    # Getters y Setters con type hints
    def getPassword(self) -> str:
        """Obtiene la contraseña del usuario."""
        return self._password
    
    def setPassword(self, password: str) -> None:
        """Establece la contraseña del usuario."""
        self._password = password
    
    def getCargo(self) -> str:
        """Obtiene el cargo del usuario."""
        return self._cargo
    
    def setCargo(self, cargo: str) -> None:
        """Establece el cargo del usuario."""
        self._cargo = cargo
    
    def getIdEmpleado(self) -> Optional[int]:
        """Obtiene el ID único del empleado en base de datos."""
        return self._id_empleado
    
    def setIdEmpleado(self, id_empleado: int) -> None:
        """Establece el ID único del empleado."""
        self._id_empleado = id_empleado
    
    @classmethod
    def getListaUser(cls) -> List['User']:
        """Obtiene la lista estática de todos los usuarios."""
        return cls._lista_users
    
    def getUsername(self) -> str:
        """Obtiene el nombre completo del usuario."""
        return f"{self.getNombre()} {self.getApellido()}"
    
    def __str__(self) -> str:
        """Representación en string del usuario."""
        return f"{self.getNombre()} {self.getApellido()} - {self._cargo}"
