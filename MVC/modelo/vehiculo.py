from datetime import datetime

class Vehiculo:
    _lista_vehiculos = []
    
    def __init__(self, patente="", marca="", modelo="", año=0, precio_diario=0.0, estado="disponible", id_vehiculo=None, create_time=None):
        self._patente = patente
        self._marca = marca
        self._modelo = modelo
        self._año = año
        self._precio_diario = precio_diario
        self._estado = estado
        self._id_vehiculo = id_vehiculo
        self._create_time = create_time or datetime.now()
    
    # Getters y Setters
    def getPatente(self):
        return self._patente
    
    def setPatente(self, patente):
        self._patente = patente
    
    def getMarca(self):
        return self._marca
    
    def setMarca(self, marca):
        self._marca = marca
    
    def getModelo(self):
        return self._modelo
    
    def setModelo(self, modelo):
        self._modelo = modelo
    
    def getAño(self):
        return self._año
    
    def setAño(self, año):
        self._año = año
    
    def getPrecioDiario(self):
        return self._precio_diario
    
    def setPrecioDiario(self, precio_diario):
        self._precio_diario = precio_diario
    
    def getEstado(self):
        return self._estado
    
    def setEstado(self, estado):
        self._estado = estado
    
    def getIdVehiculo(self):
        return self._id_vehiculo
    
    def setIdVehiculo(self, id_vehiculo):
        self._id_vehiculo = id_vehiculo
    
    def getListaVehiculos(self):
        return self._lista_vehiculos
    
    def __str__(self):
        return f"{self._marca} {self._modelo} ({self._patente}) - {self._estado} - ${self._precio_diario}/día"
