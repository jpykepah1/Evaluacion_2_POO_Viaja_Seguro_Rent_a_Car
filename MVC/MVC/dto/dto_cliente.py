from dao.dao_cliente import DaoCliente
from modelo.cliente import Cliente
from typing import Optional, List

class ClienteDTO:
    """
    Data Transfer Object para la entidad Cliente.
    
    Se encarga de la transferencia de datos entre la capa de negocio
    y la capa de persistencia para los clientes.
    """

    def agregarCliente(self, run: str, nombre: str, apellido: str, 
                      direccion: str, telefono: str) -> bool:
        """
        Agrega un nuevo cliente al sistema.
        
        Args:
            run (str): RUN del cliente
            nombre (str): Nombre del cliente
            apellido (str): Apellido del cliente
            direccion (str): Dirección del cliente
            telefono (str): Teléfono del cliente
            
        Returns:
            bool: True si el cliente fue agregado exitosamente, False en caso contrario
        """
        daocliente = DaoCliente()
        return daocliente.agregarCliente(Cliente(
            run=run, 
            nombre=nombre, 
            apellido=apellido, 
            direccion=direccion, 
            telefono=telefono
        ))

    def buscarCliente(self, run: str) -> Optional[Cliente]:
        """
        Busca un cliente por su RUN.
        
        Args:
            run (str): RUN del cliente a buscar
            
        Returns:
            Optional[Cliente]: Instancia de Cliente si se encuentra, None en caso contrario
        """
        daocliente = DaoCliente()
        return daocliente.buscarCliente(run)

    def actualizarCliente(self, run: str, nombre: str, apellido: str, 
                         direccion: str, telefono: str) -> bool:
        """
        Actualiza la información de un cliente existente.
        
        Args:
            run (str): RUN del cliente a actualizar
            nombre (str): Nuevo nombre del cliente
            apellido (str): Nuevo apellido del cliente
            direccion (str): Nueva dirección del cliente
            telefono (str): Nuevo teléfono del cliente
            
        Returns:
            bool: True si la actualización fue exitosa, False en caso contrario
        """
        daocliente = DaoCliente()
        return daocliente.actualizarCliente(Cliente(
            run=run, 
            nombre=nombre, 
            apellido=apellido, 
            direccion=direccion, 
            telefono=telefono
        ))

    def eliminarCliente(self, run: str) -> bool:
        """
        Elimina un cliente del sistema.
        
        Args:
            run (str): RUN del cliente a eliminar
            
        Returns:
            bool: True si la eliminación fue exitosa, False en caso contrario
        """
        daocliente = DaoCliente()
        return daocliente.eliminarCliente(run)

    def listarClientes(self) -> List[Cliente]:
        """
        Obtiene la lista completa de clientes del sistema.
        
        Returns:
            List[Cliente]: Lista de todos los clientes registrados
        """
        daocliente = DaoCliente()
        return daocliente.listarClientes()

    def buscarClientePorId(self, id_cliente: int) -> Optional[Cliente]:
        """
        Busca un cliente por su ID.

        Args:
            id_cliente (int): ID del cliente a buscar

        Returns:
            Optional[Cliente]: Instancia de Cliente si se encuentra, None en caso contrario
        """
        daocliente = DaoCliente()
        return daocliente.buscarClientePorId(id_cliente)
