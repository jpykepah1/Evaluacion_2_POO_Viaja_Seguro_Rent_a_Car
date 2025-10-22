from abc import ABC, abstractmethod
from typing import Optional

class Persona(ABC):
    """
    Clase abstracta que representa a una persona en el sistema.
    
    Define la estructura base para todas las entidades que representan
    personas, como empleados y clientes.
    
    Attributes:
        _run (str): RUN de la persona
        _nombre (str): Nombre de la persona
        _apellido (str): Apellido de la persona
    """
    
    def __init__(self, run: str = "", nombre: str = "", apellido: str = "") -> None:
        """
        Inicializa una nueva instancia de Persona.
        
        Args:
            run (str): RUN de la persona
            nombre (str): Nombre de la persona
            apellido (str): Apellido de la persona
        """
        self._run = run
        self._nombre = nombre
        self._apellido = apellido
    
    @abstractmethod
    def mostrar_info(self) -> str:
        """
        Método abstracto para mostrar información de la persona.
        
        Returns:
            str: Información formateada de la persona
            
        Note:
            Debe ser implementado por todas las clases hijas
        """
        pass
    
    # Getters y Setters con type hints
    def getRun(self) -> str:
        """Obtiene el RUN de la persona."""
        return self._run
    
    def setRun(self, run: str) -> None:
        """Establece el RUN de la persona."""
        self._run = run
    
    def getNombre(self) -> str:
        """Obtiene el nombre de la persona."""
        return self._nombre
    
    def setNombre(self, nombre: str) -> None:
        """Establece el nombre de la persona."""
        self._nombre = nombre
    
    def getApellido(self) -> str:
        """Obtiene el apellido de la persona."""
        return self._apellido
    
    def setApellido(self, apellido: str) -> None:
        """Establece el apellido de la persona."""
        self._apellido = apellido
    
    def __str__(self) -> str:
        """Representación en string de la persona."""
        return f"{self._nombre} {self._apellido} ({self._run})"
