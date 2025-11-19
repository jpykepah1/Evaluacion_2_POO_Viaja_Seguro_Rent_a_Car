from dao.dao_arriendo import DaoArriendo
from modelo.arriendo import Arriendo
from typing import Optional, List
from dto.dto_cliente import ClienteDTO
from dto.dto_vehiculo import VehiculoDTO

class ArriendoDTO:
    """
    Data Transfer Object para la entidad Arriendo.
    
    Se encarga de la transferencia de datos entre la capa de negocio
    y la capa de persistencia para los arriendos.
    """

    def agregarArriendo(self, id_vehiculo: int, id_cliente: int, id_empleado: int, 
                       fecha_inicio: str, fecha_fin: str, costo_total: float, 
                       estado: str = "activo", valor_uf_fecha: float = 0.0, 
                       fecha_uf_consulta: Optional[str] = None) -> bool:
        """
        Agrega un nuevo arriendo al sistema.
        
        Args:
            id_vehiculo (int): ID del vehículo arrendado
            id_cliente (int): ID del cliente que arrienda
            id_empleado (int): ID del empleado que gestiona el arriendo
            fecha_inicio (str): Fecha de inicio del arriendo (YYYY-MM-DD)
            fecha_fin (str): Fecha de fin del arriendo (YYYY-MM-DD)
            costo_total (float): Costo total calculado del arriendo
            estado (str): Estado inicial del arriendo (default: "activo")
            valor_uf_fecha (float): Valor de la UF al momento del arriendo
            fecha_uf_consulta (Optional[str]): Fecha del indicador UF consultado
            
        Returns:
            bool: True si el arriendo fue agregado exitosamente, False en caso contrario
        """
        daoarriendo = DaoArriendo()
        return daoarriendo.agregarArriendo(Arriendo(
            id_vehiculo=id_vehiculo, 
            id_cliente=id_cliente, 
            id_empleado=id_empleado, 
            fecha_inicio=fecha_inicio, 
            fecha_fin=fecha_fin, 
            costo_total=costo_total, 
            estado=estado,
            valor_uf_fecha=valor_uf_fecha,
            fecha_uf_consulta=fecha_uf_consulta
        ))

    def buscarArriendo(self, id_arriendo: int) -> Optional[Arriendo]:
        """
        Busca un arriendo por su ID único.
        
        Args:
            id_arriendo (int): ID del arriendo a buscar
            
        Returns:
            Optional[Arriendo]: Instancia de Arriendo si se encuentra, None en caso contrario
        """
        daoarriendo = DaoArriendo()
        return daoarriendo.buscarArriendo(id_arriendo)

    def actualizarArriendo(self, id_arriendo: int, id_vehiculo: int, id_cliente: int, 
                          id_empleado: int, fecha_inicio: str, fecha_fin: str, 
                          costo_total: float, estado: str, valor_uf_fecha: float = 0.0, 
                          fecha_uf_consulta: Optional[str] = None) -> bool:
        """
        Actualiza la información de un arriendo existente.
        
        Args:
            id_arriendo (int): ID del arriendo a actualizar
            id_vehiculo (int): Nuevo ID del vehículo arrendado
            id_cliente (int): Nuevo ID del cliente que arrienda
            id_empleado (int): Nuevo ID del empleado que gestiona el arriendo
            fecha_inicio (str): Nueva fecha de inicio del arriendo (YYYY-MM-DD)
            fecha_fin (str): Nueva fecha de fin del arriendo (YYYY-MM-DD)
            costo_total (float): Nuevo costo total del arriendo
            estado (str): Nuevo estado del arriendo
            valor_uf_fecha (float): Nuevo valor de la UF al momento del arriendo
            fecha_uf_consulta (Optional[str]): Nueva fecha del indicador UF consultado
            
        Returns:
            bool: True si la actualización fue exitosa, False en caso contrario
        """
        daoarriendo = DaoArriendo()
        return daoarriendo.actualizarArriendo(Arriendo(
            id_vehiculo=id_vehiculo, 
            id_cliente=id_cliente, 
            id_empleado=id_empleado, 
            fecha_inicio=fecha_inicio, 
            fecha_fin=fecha_fin, 
            costo_total=costo_total, 
            estado=estado, 
            id_arriendo=id_arriendo,
            valor_uf_fecha=valor_uf_fecha,
            fecha_uf_consulta=fecha_uf_consulta
        ))

    def eliminarArriendo(self, id_arriendo: int) -> bool:
        """
        Elimina un arriendo del sistema.
        
        Args:
            id_arriendo (int): ID del arriendo a eliminar
            
        Returns:
            bool: True si la eliminación fue exitosa, False en caso contrario
        """
        daoarriendo = DaoArriendo()
        return daoarriendo.eliminarArriendo(id_arriendo)

    def listarArriendos(self) -> List[Arriendo]:
        """
        Obtiene la lista completa de arriendos del sistema.
        
        Returns:
            List[Arriendo]: Lista de todos los arriendos registrados
        """
        daoarriendo = DaoArriendo()
        return daoarriendo.listarArriendos()

    def listarArriendosPresentacion(self) -> List[dict]:
        """
        Retorna una lista preparada para presentación donde cada elemento es un dict:
        { 'arriendo': Arriendo, 'vehiculo_info': str, 'cliente_info': str }
        """
        daoarriendo = DaoArriendo()
        resultados = daoarriendo.listarArriendosConRelacion()
        lista = []
        for item in resultados:
            a = item['arriendo']
            veh_info = f"{item.get('veh_patente')} - {item.get('veh_marca')} {item.get('veh_modelo')}" if item.get('veh_patente') else f"Vehículo ID {a.getIdVehiculo()}"
            cli_info = f"{item.get('cli_nombre')} {item.get('cli_apellido')}" if item.get('cli_nombre') else f"Cliente ID {a.getIdCliente()}"
            lista.append({
                'arriendo': a,
                'vehiculo_info': veh_info,
                'cliente_info': cli_info
            })
        return lista

    def listarArriendosPorFecha(self, fecha: str) -> List[Arriendo]:
        """
        Obtiene la lista de arriendos que coinciden con una fecha específica.
        
        Args:
            fecha (str): Fecha a buscar (YYYY-MM-DD)
            
        Returns:
            List[Arriendo]: Lista de arriendos que empiezan o terminan en la fecha especificada
        """
        daoarriendo = DaoArriendo()
        return daoarriendo.listarArriendosPorFecha(fecha)

    def listarArriendosPorFechaPresentacion(self, fecha: str) -> List[dict]:
        """
        Versión para presentación de `listarArriendosPorFecha`.
        Devuelve lista de dicts con las mismas claves que `listarArriendosPresentacion`.
        """
        daoarriendo = DaoArriendo()
        resultados = daoarriendo.listarArriendosPorFechaConRelacion(fecha)
        lista = []
        for item in resultados:
            a = item['arriendo']
            veh_info = f"{item.get('veh_patente')} - {item.get('veh_marca')} {item.get('veh_modelo')}" if item.get('veh_patente') else f"Vehículo ID {a.getIdVehiculo()}"
            cli_info = f"{item.get('cli_nombre')} {item.get('cli_apellido')}" if item.get('cli_nombre') else f"Cliente ID {a.getIdCliente()}"
            lista.append({
                'arriendo': a,
                'vehiculo_info': veh_info,
                'cliente_info': cli_info
            })
        return lista
