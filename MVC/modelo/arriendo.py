from datetime import datetime

class Arriendo:
    _lista_arriendos = []
    
    def __init__(self, id_vehiculo=None, id_cliente=None, id_empleado=None, fecha_inicio=None, fecha_fin=None, 
                 costo_total=0.0, estado="activo", id_arriendo=None, create_time=None):
        self._id_arriendo = id_arriendo
        self._id_vehiculo = id_vehiculo
        self._id_cliente = id_cliente
        self._id_empleado = id_empleado
        self._fecha_inicio = fecha_inicio
        self._fecha_fin = fecha_fin
        self._costo_total = costo_total
        self._estado = estado
        self._create_time = create_time or datetime.now()
    
    # Getters y Setters
    def getIdArriendo(self):
        return self._id_arriendo
    
    def setIdArriendo(self, id_arriendo):
        self._id_arriendo = id_arriendo
    
    def getIdVehiculo(self):
        return self._id_vehiculo
    
    def setIdVehiculo(self, id_vehiculo):
        self._id_vehiculo = id_vehiculo
    
    def getIdCliente(self):
        return self._id_cliente
    
    def setIdCliente(self, id_cliente):
        self._id_cliente = id_cliente
    
    def getIdEmpleado(self):
        return self._id_empleado
    
    def setIdEmpleado(self, id_empleado):
        self._id_empleado = id_empleado
    
    def getFechaInicio(self):
        return self._fecha_inicio
    
    def setFechaInicio(self, fecha_inicio):
        self._fecha_inicio = fecha_inicio
    
    def getFechaFin(self):
        return self._fecha_fin
    
    def setFechaFin(self, fecha_fin):
        self._fecha_fin = fecha_fin
    
    def getCostoTotal(self):
        return self._costo_total
    
    def setCostoTotal(self, costo_total):
        self._costo_total = costo_total
    
    def getEstado(self):
        return self._estado
    
    def setEstado(self, estado):
        self._estado = estado
    
    def getCreateTime(self):
        return self._create_time
    
    def getListaArriendos(self):
        return self._lista_arriendos
    
    def __str__(self):
        return f"Arriendo #{self._id_arriendo}: ${self._costo_total} - {self._estado}"
