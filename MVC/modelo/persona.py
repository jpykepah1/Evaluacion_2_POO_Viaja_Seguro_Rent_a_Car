from abc import ABC, abstractmethod

class Persona(ABC):
    def __init__(self, run="", nombre="", apellido=""):
        self._run = run
        self._nombre = nombre
        self._apellido = apellido
    
    @abstractmethod
    def mostrar_info(self):
        pass
    
    # Getters y Setters
    def getRun(self):
        return self._run
    
    def setRun(self, run):
        self._run = run
    
    def getNombre(self):
        return self._nombre
    
    def setNombre(self, nombre):
        self._nombre = nombre
    
    def getApellido(self):
        return self._apellido
    
    def setApellido(self, apellido):
        self._apellido = apellido
    
    def __str__(self):
        return f"{self._nombre} {self._apellido} ({self._run})"
