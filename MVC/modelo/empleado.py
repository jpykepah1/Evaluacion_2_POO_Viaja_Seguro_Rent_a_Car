from modelo.persona import Persona
from datetime import datetime

class Empleado(Persona):
    _lista_empleados = []
    
    def __init__(self, run="", nombre="", apellido="", password="", cargo="", id_empleado=None, create_time=None):
        super().__init__(run, nombre, apellido)
        self._password = password
        self._cargo = cargo
        self._id_empleado = id_empleado
        self._create_time = create_time or datetime.now()
    
    def mostrar_info(self):
        return f"Empleado: {self.getNombre()} {self.getApellido()} - Cargo: {self._cargo}"
    
    # Getters y Setters
    def getPassword(self):
        return self._password
    
    def setPassword(self, password):
        self._password = password
    
    def getCargo(self):
        return self._cargo
    
    def setCargo(self, cargo):
        self._cargo = cargo
    
    def getIdEmpleado(self):
        return self._id_empleado
    
    def getListaEmpleados(self):
        return self._lista_empleados
    
    def __str__(self):
        return f"{self.getNombre()} {self.getApellido()} - {self._cargo}"