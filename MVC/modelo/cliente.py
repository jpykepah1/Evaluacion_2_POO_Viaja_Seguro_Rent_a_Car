from modelo.persona import Persona
from datetime import datetime

class Cliente(Persona):
    _lista_clientes = []
    
    def __init__(self, run="", nombre="", apellido="", direccion="", telefono="", id_cliente=None, create_time=None):
        super().__init__(run, nombre, apellido)
        self._direccion = direccion
        self._telefono = telefono
        self._id_cliente = id_cliente
        self._create_time = create_time or datetime.now()
    
    def mostrar_info(self):
        return f"Cliente: {self.getNombre()} {self.getApellido()} - Tel: {self._telefono}"
    
    # Getters y Setters
    def getDireccion(self):
        return self._direccion
    
    def setDireccion(self, direccion):
        self._direccion = direccion
    
    def getTelefono(self):
        return self._telefono
    
    def setTelefono(self, telefono):
        self._telefono = telefono
    
    def getIdCliente(self):
        return self._id_cliente
    
    def setIdCliente(self, id_cliente):
        self._id_cliente = id_cliente
    
    def getListaClientes(self):
        return self._lista_clientes
    
    def __str__(self):
        return f"{self.getNombre()} {self.getApellido()} - {self._telefono}"