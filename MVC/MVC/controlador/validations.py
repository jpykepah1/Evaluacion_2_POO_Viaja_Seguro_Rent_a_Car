from dto.dto_user import UserDTO
from dto.dto_cliente import ClienteDTO
from dto.dto_vehiculo import VehiculoDTO
from dto.dto_arriendo import ArriendoDTO
from modelo.empleado import Empleado
import getpass
from datetime import datetime, timedelta
from utils.validador_formatos import *
import logging
from servicio.indicador_service import IndicadorService

logger = logging.getLogger(__name__)

def validarLogin(username, password):
    logger.debug("Validando credenciales para usuario: %s", username)
    userdto = UserDTO()
    return userdto.validarLogin(username, password)

def inicial(empleado_actual):
    """Menú principal después del login"""
    logger.info("Sesión iniciada para: %s %s (%s)", 
                empleado_actual.getNombre(), empleado_actual.getApellido(), empleado_actual.getCargo())
    
    while True:
        print(f"""
=== MENÚ PRINCIPAL ===
Usuario: {empleado_actual.getNombre()} {empleado_actual.getApellido()} - Cargo: {empleado_actual.getCargo()}

1. Gestión de Empleados
2. Gestión de Clientes
3. Gestión de Vehículos
4. Gestión de Arriendos
5. Generar Informes
6. Cerrar Sesión
""")
        opcion = input("Seleccione una opción: ")
        
        if opcion == '1':
            if empleado_actual.getCargo() == 'gerente':
                logger.info("Acceso a gestión de empleados por: %s", empleado_actual.getRun())
                gestion_empleados()
            else:
                logger.warning("Intento de acceso no autorizado a gestión de empleados por: %s", empleado_actual.getRun())
                print("❌ Solo los gerentes pueden gestionar empleados")
        elif opcion == '2':
            logger.info("Acceso a gestión de clientes por: %s", empleado_actual.getRun())
            gestion_clientes()
        elif opcion == '3':
            logger.info("Acceso a gestión de vehículos por: %s", empleado_actual.getRun())
            gestion_vehiculos()
        elif opcion == '4':
            logger.info("Acceso a gestión de arriendos por: %s", empleado_actual.getRun())
            gestion_arriendos(empleado_actual)
        elif opcion == '5':
            logger.info("Acceso a generación de informes por: %s", empleado_actual.getRun())
            generar_informes()
        elif opcion == '6':
            logger.info("Sesión cerrada por: %s", empleado_actual.getRun())
            print("👋 Sesión cerrada")
            break
        else:
            logger.warning("Opción inválida seleccionada en menú principal: %s", opcion)
            print("❌ Opción no válida")

def obtener_dato_validado(funcion_validacion, mensaje, mensaje_error, formato_esperado=""):
    """Función auxiliar para obtener datos validados"""
    while True:
        dato = input(mensaje)
        es_valido, mensaje_val = funcion_validacion(dato)
        
        if es_valido:
            # Para RUN, devuelve el formato estandarizado
            if funcion_validacion == validar_run:
                logger.debug("Dato validado exitosamente: %s", mensaje_val)
                return mensaje_val
            logger.debug("Dato validado exitosamente: %s", dato)
            return dato
        else:
            logger.debug("Validación fallida: %s - %s", dato, mensaje_val)
            print(f"❌ {mensaje_val}")
            if formato_esperado:
                print(f"💡 Formato esperado: {formato_esperado}")

def gestion_empleados():
    """Gestión de empleados (solo para gerentes)"""
    logger.info("Iniciando gestión de empleados")
    userdto = UserDTO()
    while True:
        print("""
=== GESTIÓN DE EMPLEADOS ===
1. Agregar Empleado
2. Buscar Empleado
3. Actualizar Empleado
4. Eliminar Empleado
5. Listar Todos los Empleados
6. Volver al Menú Principal
""")
        opcion = input("Seleccione una opción: ")
        
        if opcion == '1':
            logger.info("Iniciando proceso de agregar empleado")
            print("\n--- AGREGAR EMPLEADO ---")
            
            # Validar RUN
            run = obtener_dato_validado(
                validar_run, 
                "RUN: ", 
                "RUN inválido",
                "12345678-9 o 12.345.678-9"
            )
            
            # Validar nombre
            nombre = obtener_dato_validado(
                validar_nombre,
                "Nombre: ",
                "Nombre inválido",
                "Solo letras (2-50 caracteres)"
            )
            
            # Validar apellido
            apellido = obtener_dato_validado(
                validar_nombre,
                "Apellido: ",
                "Apellido inválido",
                "Solo letras (2-50 caracteres)"
            )
            
            # Validar contraseña con política de seguridad fuerte
            while True:
                password = getpass.getpass("Contraseña: ")
                es_valido, mensaje = validar_password_segura(password)
                if es_valido:
                    break
                logger.debug("Contraseña inválida: %s", mensaje)
                print(f"[ERROR] {mensaje}")
            
            # Validar cargo
            cargo = obtener_dato_validado(
                validar_cargo,
                "Cargo (gerente/empleado): ",
                "Cargo inválido",
                "gerente o empleado"
            ).lower()
            
            # Validar entrada SQL antes de guardar
            if not (validar_entrada_sql(run) and validar_entrada_sql(nombre) and validar_entrada_sql(apellido) and validar_entrada_sql(cargo)):
                logger.warning("Intento de inyección SQL detectado al agregar empleado: run=%s, nombre=%s, apellido=%s", run, nombre, apellido)
                print("[ERROR] Datos sospechosos detectados. Operación cancelada.")
                continue
                
            if userdto.agregarUsuario(run, nombre, apellido, password, cargo):
                logger.info("Empleado agregado exitosamente: %s %s (%s)", nombre, apellido, run)
                print("[OK] Empleado agregado correctamente")
            else:
                logger.error("Error al agregar empleado: %s", run)
                print("[ERROR] Error al agregar empleado")
                
        elif opcion == '2':
            logger.info("Buscando empleado")
            print("\n--- BUSCAR EMPLEADO ---")
            run = obtener_dato_validado(
                validar_run,
                "RUN del empleado: ",
                "RUN inválido"
            )
            empleado = userdto.buscarUsuario(run)
            if empleado:
                logger.debug("Empleado encontrado: %s", run)
                print(f"✅ Empleado encontrado:")
                print(f"   RUN: {empleado.getRun()}")
                print(f"   Nombre: {empleado.getNombre()} {empleado.getApellido()}")
                print(f"   Cargo: {empleado.getCargo()}")
            else:
                logger.debug("Empleado no encontrado: %s", run)
                print("❌ Empleado no encontrado")
                
        elif opcion == '3':
            logger.info("Actualizando empleado")
            print("\n--- ACTUALIZAR EMPLEADO ---")
            run = obtener_dato_validado(
                validar_run,
                "RUN del empleado a actualizar: ",
                "RUN inválido"
            )
            empleado_existente = userdto.buscarUsuario(run)
            if empleado_existente:
                logger.debug("Empleado encontrado para actualización: %s", run)
                print(f"Empleado actual: {empleado_existente.getNombre()} {empleado_existente.getApellido()}")
                
                # Validar nombre
                nombre = obtener_dato_validado(
                    validar_nombre,
                    f"Nuevo nombre [{empleado_existente.getNombre()}]: ",
                    "Nombre inválido"
                ) or empleado_existente.getNombre()
                
                # Validar apellido
                apellido = obtener_dato_validado(
                    validar_nombre,
                    f"Nuevo apellido [{empleado_existente.getApellido()}]: ",
                    "Apellido inválido"
                ) or empleado_existente.getApellido()
                
                # Validar contraseña con política de seguridad fuerte
                password = getpass.getpass("Nueva contraseña (dejar en blanco para no cambiar): ")
                if password:
                    while True:
                        es_valido, mensaje = validar_password_segura(password)
                        if es_valido:
                            from utils.encoder import Encoder
                            password = Encoder().encode(password)
                            break
                        logger.debug("Contraseña inválida durante actualización: %s", mensaje)
                        print(f"❌ {mensaje}")
                        password = getpass.getpass("Nueva contraseña (dejar en blanco para no cambiar): ")
                        if not password:
                            password = empleado_existente.getPassword()
                            break
                else:
                    password = empleado_existente.getPassword()
                
                # Validar cargo
                cargo = obtener_dato_validado(
                    validar_cargo,
                    f"Nuevo cargo [{empleado_existente.getCargo()}]: ",
                    "Cargo inválido"
                ) or empleado_existente.getCargo()
                
                if userdto.actualizarUsuario(run, nombre, apellido, password, cargo):
                    logger.info("Empleado actualizado exitosamente: %s", run)
                    print("✅ Empleado actualizado correctamente")
                else:
                    logger.error("Error al actualizar empleado: %s", run)
                    print("❌ Error al actualizar empleado")
            else:
                logger.debug("Empleado no encontrado para actualización: %s", run)
                print("❌ Empleado no encontrado")
                
        elif opcion == '4':
            logger.info("Eliminando empleado")
            print("\n--- ELIMINAR EMPLEADO ---")
            run = obtener_dato_validado(
                validar_run,
                "RUN del empleado a eliminar: ",
                "RUN inválido"
            )
            empleado = userdto.buscarUsuario(run)
            if empleado:
                logger.debug("Empleado encontrado para eliminación: %s", run)
                confirmacion = input(f"¿Está seguro de eliminar a {empleado.getNombre()} {empleado.getApellido()}? (s/n): ")
                if confirmacion.lower() == 's':
                    if userdto.eliminarUsuario(run):
                        logger.info("Empleado eliminado exitosamente: %s", run)
                        print("✅ Empleado eliminado correctamente")
                    else:
                        logger.error("Error al eliminar empleado: %s", run)
                        print("❌ Error al eliminar empleado")
            else:
                logger.debug("Empleado no encontrado para eliminación: %s", run)
                print("❌ Empleado no encontrado")
                
        elif opcion == '5':
            logger.info("Listando todos los empleados")
            print("\n--- LISTA DE EMPLEADOS ---")
            empleados = userdto.listarUsuarios()
            if empleados:
                logger.debug("Listados %d empleados", len(empleados))
                for i, empleado in enumerate(empleados, 1):
                    print(f"{i}. {empleado.getNombre()} {empleado.getApellido()} - RUN: {empleado.getRun()} - Cargo: {empleado.getCargo()}")
            else:
                logger.debug("No hay empleados registrados")
                print("📝 No hay empleados registrados")
                
        elif opcion == '6':
            logger.info("Saliendo de gestión de empleados")
            break
        else:
            logger.warning("Opción inválida en gestión de empleados: %s", opcion)
            print("❌ Opción no válida")

def gestion_clientes():
    """Gestión completa de clientes"""
    logger.info("Iniciando gestión de clientes")
    from dto.dto_cliente import ClienteDTO
    clientedto = ClienteDTO()
    
    while True:
        print("""
=== GESTIÓN DE CLIENTES ===
1. Agregar Cliente
2. Buscar Cliente
3. Actualizar Cliente
4. Eliminar Cliente
5. Listar Todos los Clientes
6. Volver al Menú Principal
""")
        opcion = input("Seleccione una opción: ")
        
        if opcion == '1':
            logger.info("Agregando nuevo cliente")
            print("\n--- AGREGAR CLIENTE ---")
            
            # Validar RUN
            run = obtener_dato_validado(
                validar_run,
                "RUN: ",
                "RUN inválido"
            )
            
            # Validar nombre
            nombre = obtener_dato_validado(
                validar_nombre,
                "Nombre: ",
                "Nombre inválido"
            )
            
            # Validar apellido
            apellido = obtener_dato_validado(
                validar_nombre,
                "Apellido: ",
                "Apellido inválido"
            )
            
            # Validar dirección
            direccion = obtener_dato_validado(
                validar_direccion,
                "Dirección: ",
                "Dirección inválida",
                "5-100 caracteres"
            )
            
            # Validar teléfono
            telefono = obtener_dato_validado(
                validar_telefono,
                "Teléfono: ",
                "Teléfono inválido",
                "9 dígitos (ej: 912345678)"
            )
            
            # Validar entrada SQL antes de guardar
            if not (validar_entrada_sql(run) and validar_entrada_sql(nombre) and validar_entrada_sql(apellido) and validar_entrada_sql(direccion)):
                logger.warning("Intento de inyección SQL detectado al agregar cliente: run=%s, nombre=%s, apellido=%s", run, nombre, apellido)
                print("[ERROR] Datos sospechosos detectados. Operación cancelada.")
                continue
            
            if clientedto.agregarCliente(run, nombre, apellido, direccion, telefono):
                logger.info("Cliente agregado exitosamente: %s %s (%s)", nombre, apellido, run)
                print("[OK] Cliente agregado correctamente")
            else:
                logger.error("Error al agregar cliente: %s", run)
                print("[ERROR] Error al agregar cliente")
                
        elif opcion == '2':
            logger.info("Buscando cliente")
            print("\n--- BUSCAR CLIENTE ---")
            run = obtener_dato_validado(
                validar_run,
                "RUN del cliente: ",
                "RUN inválido"
            )
            cliente = clientedto.buscarCliente(run)
            if cliente:
                logger.debug("Cliente encontrado: %s", run)
                print(f"✅ Cliente encontrado:")
                print(f"   RUN: {cliente.getRun()}")
                print(f"   Nombre: {cliente.getNombre()} {cliente.getApellido()}")
                print(f"   Dirección: {cliente.getDireccion()}")
                print(f"   Teléfono: {cliente.getTelefono()}")
            else:
                logger.debug("Cliente no encontrado: %s", run)
                print("❌ Cliente no encontrado")
                
        elif opcion == '3':
            logger.info("Actualizando cliente")
            print("\n--- ACTUALIZAR CLIENTE ---")
            run = obtener_dato_validado(
                validar_run,
                "RUN del cliente a actualizar: ",
                "RUN inválido"
            )
            cliente_existente = clientedto.buscarCliente(run)
            if cliente_existente:
                logger.debug("Cliente encontrado para actualización: %s", run)
                print(f"Cliente actual: {cliente_existente.getNombre()} {cliente_existente.getApellido()}")
                
                # Validar nombre
                nombre = obtener_dato_validado(
                    validar_nombre,
                    f"Nuevo nombre [{cliente_existente.getNombre()}]: ",
                    "Nombre inválido"
                ) or cliente_existente.getNombre()
                
                # Validar apellido
                apellido = obtener_dato_validado(
                    validar_nombre,
                    f"Nuevo apellido [{cliente_existente.getApellido()}]: ",
                    "Apellido inválido"
                ) or cliente_existente.getApellido()
                
                # Validar dirección
                direccion = obtener_dato_validado(
                    validar_direccion,
                    f"Nueva dirección [{cliente_existente.getDireccion()}]: ",
                    "Dirección inválida"
                ) or cliente_existente.getDireccion()
                
                # Validar teléfono
                telefono = obtener_dato_validado(
                    validar_telefono,
                    f"Nuevo teléfono [{cliente_existente.getTelefono()}]: ",
                    "Teléfono inválido"
                ) or cliente_existente.getTelefono()
                
                if clientedto.actualizarCliente(run, nombre, apellido, direccion, telefono):
                    logger.info("Cliente actualizado exitosamente: %s", run)
                    print("✅ Cliente actualizado correctamente")
                else:
                    logger.error("Error al actualizar cliente: %s", run)
                    print("❌ Error al actualizar cliente")
            else:
                logger.debug("Cliente no encontrado para actualización: %s", run)
                print("❌ Cliente no encontrado")
                
        elif opcion == '4':
            logger.info("Eliminando cliente")
            print("\n--- ELIMINAR CLIENTE ---")
            run = obtener_dato_validado(
                validar_run,
                "RUN del cliente a eliminar: ",
                "RUN inválido"
            )
            
            cliente = clientedto.buscarCliente(run)
            if cliente:
                logger.debug("Cliente encontrado para eliminación: %s", run)
                print(f"🔍 Cliente encontrado: {cliente.getNombre()} {cliente.getApellido()}")
                confirmacion = input(f"¿Está seguro de eliminar a {cliente.getNombre()} {cliente.getApellido()}? (s/N): ")
                if confirmacion.lower() == 's':
                    if clientedto.eliminarCliente(run):
                        logger.info("Cliente eliminado exitosamente: %s", run)
                        print("✅ Cliente eliminado correctamente")
                    else:
                        logger.error("Error al eliminar cliente: %s", run)
                        print("❌ Error al eliminar cliente - Puede que tenga arriendos asociados")
                else:
                    logger.debug("Eliminación de cliente cancelada: %s", run)
                    print("❌ Eliminación cancelada")
            else:
                logger.debug("Cliente no encontrado para eliminación: %s", run)
                print("❌ Cliente no encontrado")
                
        elif opcion == '5':
            logger.info("Listando todos los clientes")
            print("\n--- LISTA DE CLIENTES ---")
            clientes = clientedto.listarClientes()
            if clientes:
                logger.debug("Listados %d clientes", len(clientes))
                for i, cliente in enumerate(clientes, 1):
                    print(f"{i}. {cliente.getNombre()} {cliente.getApellido()} - RUN: {cliente.getRun()} - Tel: {cliente.getTelefono()}")
            else:
                logger.debug("No hay clientes registrados")
                print("📝 No hay clientes registrados")
                
        elif opcion == '6':
            logger.info("Saliendo de gestión de clientes")
            break
        else:
            logger.warning("Opción inválida en gestión de clientes: %s", opcion)
            print("❌ Opción no válida")

def gestion_vehiculos():
    """Gestión completa de vehículos"""
    logger.info("Iniciando gestión de vehículos")
    vehiculodto = VehiculoDTO()
    while True:
        print("""
=== GESTIÓN DE VEHÍCULOS ===
1. Agregar Vehículo
2. Buscar Vehículo
3. Actualizar Vehículo
4. Eliminar Vehículo
5. Listar Todos los Vehículos
6. Listar Vehículos Disponibles
7. Volver al Menú Principal
""")
        opcion = input("Seleccione una opción: ")
        
        if opcion == '1':
            logger.info("Agregando nuevo vehículo")
            print("\n--- AGREGAR VEHÍCULO ---")
            
            # Validar patente
            patente = obtener_dato_validado(
                validar_patente,
                "Patente: ",
                "Patente inválida",
                "ABCD12 o ABC123"
            ).upper()
            
            while True:
                marca = input("Marca: ")
                marca = sanitizar_texto(marca)
                if marca:
                    break
                print("❌ Marca inválida (no puede estar vacía)")

            while True:
                modelo = input("Modelo: ")
                modelo = sanitizar_texto(modelo)
                if modelo:
                    break
                print("❌ Modelo inválido (no puede estar vacío)")
            
            # Validar año
            año = obtener_dato_validado(
                validar_año,
                "Año: ",
                "Año inválido",
                f"1900-{datetime.now().year + 1}"
            )
            año = int(año)
            
            # Validar precio
            precio_diario = obtener_dato_validado(
                validar_precio,
                "Precio diario: ",
                "Precio inválido",
                "Número mayor a 0"
            )
            precio_diario = float(precio_diario)
                
            # Validar estado
            estado = obtener_dato_validado(
                validar_estado_vehiculo,
                "Estado (disponible/mantencion) [disponible]: ",
                "Estado inválido",
                "disponible o mantencion"
            ).lower() or "disponible"
            
            if vehiculodto.agregarVehiculo(patente, marca, modelo, año, precio_diario, estado):
                logger.info("Vehículo agregado exitosamente: %s %s (%s)", marca, modelo, patente)
                print("✅ Vehículo agregado correctamente")
            else:
                logger.error("Error al agregar vehículo: %s", patente)
                print("❌ Error al agregar vehículo")
                
        elif opcion == '2':
            logger.info("Buscando vehículo")
            print("\n--- BUSCAR VEHÍCULO ---")
            patente = obtener_dato_validado(
                validar_patente,
                "Patente del vehículo: ",
                "Patente inválida"
            ).upper()
            vehiculo = vehiculodto.buscarVehiculo(patente)
            if vehiculo:
                logger.debug("Vehículo encontrado: %s", patente)
                print(f"✅ Vehículo encontrado:")
                print(f"   Patente: {vehiculo.getPatente()}")
                print(f"   Marca: {vehiculo.getMarca()}")
                print(f"   Modelo: {vehiculo.getModelo()}")
                print(f"   Año: {vehiculo.getAño()}")
                print(f"   Precio diario: ${vehiculo.getPrecioDiario():,.0f}")
                print(f"   Estado: {vehiculo.getEstado()}")
            else:
                logger.debug("Vehículo no encontrado: %s", patente)
                print("❌ Vehículo no encontrado")
                
        elif opcion == '3':
            logger.info("Actualizando vehículo")
            print("\n--- ACTUALIZAR VEHÍCULO ---")
            patente = obtener_dato_validado(
                validar_patente,
                "Patente del vehículo a actualizar: ",
                "Patente inválida"
            ).upper()
            vehiculo_existente = vehiculodto.buscarVehiculo(patente)
            if vehiculo_existente:
                logger.debug("Vehículo encontrado para actualización: %s", patente)
                print(f"Vehículo actual: {vehiculo_existente.getMarca()} {vehiculo_existente.getModelo()} - {vehiculo_existente.getPatente()}")
                
                marca = input(f"Nueva marca [{vehiculo_existente.getMarca()}]: ")
                if marca:
                    marca = sanitizar_texto(marca)
                else:
                    marca = vehiculo_existente.getMarca()

                modelo = input(f"Nuevo modelo [{vehiculo_existente.getModelo()}]: ")
                if modelo:
                    modelo = sanitizar_texto(modelo)
                else:
                    modelo = vehiculo_existente.getModelo()
                
                # Validar año
                año_input = input(f"Nuevo año [{vehiculo_existente.getAño()}]: ")
                if año_input:
                    año = obtener_dato_validado(
                        lambda x: validar_año(x),
                        "",
                        "Año inválido"
                    )
                    año = int(año)
                else:
                    año = vehiculo_existente.getAño()
                
                # Validar precio
                precio_input = input(f"Nuevo precio diario [{vehiculo_existente.getPrecioDiario():,.0f}]: ")
                if precio_input:
                    precio_diario = obtener_dato_validado(
                        validar_precio,
                        "",
                        "Precio inválido"
                    )
                    precio_diario = float(precio_diario)
                else:
                    precio_diario = vehiculo_existente.getPrecioDiario()
                    
                # Validar estado
                estado = obtener_dato_validado(
                    validar_estado_vehiculo,
                    f"Nuevo estado [{vehiculo_existente.getEstado()}]: ",
                    "Estado inválido"
                ) or vehiculo_existente.getEstado()
                
                if vehiculodto.actualizarVehiculo(patente, marca, modelo, año, precio_diario, estado):
                    logger.info("Vehículo actualizado exitosamente: %s", patente)
                    print("✅ Vehículo actualizado correctamente")
                else:
                    logger.error("Error al actualizar vehículo: %s", patente)
                    print("❌ Error al actualizar vehículo")
            else:
                logger.debug("Vehículo no encontrado para actualización: %s", patente)
                print("❌ Vehículo no encontrado")
                
        elif opcion == '4':
            logger.info("Eliminando vehículo")
            print("\n--- ELIMINAR VEHÍCULO ---")
            patente = obtener_dato_validado(
                validar_patente,
                "Patente del vehículo a eliminar: ",
                "Patente inválida"
            ).upper()
            vehiculo = vehiculodto.buscarVehiculo(patente)
            if vehiculo:
                logger.debug("Vehículo encontrado para eliminación: %s", patente)
                confirmacion = input(f"¿Está seguro de eliminar el vehículo {vehiculo.getMarca()} {vehiculo.getModelo()} ({vehiculo.getPatente()})? (s/n): ")
                if confirmacion.lower() == 's':
                    if vehiculodto.eliminarVehiculo(patente):
                        logger.info("Vehículo eliminado exitosamente: %s", patente)
                        print("✅ Vehículo eliminado correctamente")
                    else:
                        logger.error("Error al eliminar vehículo: %s", patente)
                        print("❌ Error al eliminar vehículo")
            else:
                logger.debug("Vehículo no encontrado para eliminación: %s", patente)
                print("❌ Vehículo no encontrado")
                
        elif opcion == '5':
            logger.info("Listando todos los vehículos")
            print("\n--- LISTA DE VEHÍCULOS ---")
            vehiculos = vehiculodto.listarVehiculos()
            if vehiculos:
                logger.debug("Listados %d vehículos", len(vehiculos))
                for i, vehiculo in enumerate(vehiculos, 1):
                    estado_icon = "🟢" if vehiculo.getEstado() == "disponible" else "🟡" if vehiculo.getEstado() == "mantencion" else "🔴"
                    print(f"{i}. {vehiculo.getMarca()} {vehiculo.getModelo()} - {vehiculo.getPatente()} - Año: {vehiculo.getAño()} - Precio: ${vehiculo.getPrecioDiario():,.0f} - {estado_icon} {vehiculo.getEstado()}")
            else:
                logger.debug("No hay vehículos registrados")
                print("📝 No hay vehículos registrados")
                
        elif opcion == '6':
            logger.info("Listando vehículos disponibles")
            print("\n--- VEHÍCULOS DISPONIBLES ---")
            vehiculos = vehiculodto.listarVehiculosDisponibles()
            if vehiculos:
                logger.debug("Listados %d vehículos disponibles", len(vehiculos))
                for i, vehiculo in enumerate(vehiculos, 1):
                    print(f"{i}. {vehiculo.getMarca()} {vehiculo.getModelo()} - {vehiculo.getPatente()} - Año: {vehiculo.getAño()} - Precio: ${vehiculo.getPrecioDiario():,.0f}")
            else:
                logger.debug("No hay vehículos disponibles")
                print("📝 No hay vehículos disponibles")
                
        elif opcion == '7':
            logger.info("Saliendo de gestión de vehículos")
            break
        else:
            logger.warning("Opción inválida en gestión de vehículos: %s", opcion)
            print("❌ Opción no válida")

def gestion_arriendos(empleado_actual):
    """Gestión de arriendos"""
    logger.info("Iniciando gestión de arriendos por: %s", empleado_actual.getRun())
    arriendodto = ArriendoDTO()
    clientedto = ClienteDTO()
    vehiculodto = VehiculoDTO()
    
    while True:
        print("""
=== GESTIÓN DE ARRIENDOS ===
1. Agregar Arriendo
2. Buscar Arriendo
3. Cancelar Arriendo
4. Listar Todos los Arriendos
5. Listar Arriendos por Fecha
6. Volver al Menú Principal
""")
        opcion = input("Seleccione una opción: ")
        
        if opcion == '1':
            logger.info("Agregando nuevo arriendo")
            print("\n--- AGREGAR ARRIENDO ---")
            
            # Listar clientes
            print("\n--- CLIENTES DISPONIBLES ---")
            clientes = clientedto.listarClientes()
            if not clientes:
                logger.warning("No hay clientes registrados para crear arriendo")
                print("❌ No hay clientes registrados. Debe registrar clientes primero.")
                continue
            for cliente in clientes:
                print(f"  ID: {cliente.getIdCliente()} - {cliente.getNombre()} {cliente.getApellido()}")
            
            try:
                id_cliente = int(input("\nID del cliente: "))
            except ValueError:
                logger.warning("ID de cliente inválido")
                print("❌ ID debe ser un número")
                continue
            
            # Listar vehículos disponibles
            print("\n--- VEHÍCULOS DISPONIBLES ---")
            vehiculos = vehiculodto.listarVehiculosDisponibles()
            if not vehiculos:
                logger.warning("No hay vehículos disponibles para arriendo")
                print("❌ No hay vehículos disponibles")
                continue
            for vehiculo in vehiculos:
                print(f"  ID: {vehiculo.getIdVehiculo()} - {vehiculo.getMarca()} {vehiculo.getModelo()} - ${vehiculo.getPrecioDiario():,.0f}/día")
            
            try:
                id_vehiculo = int(input("\nID del vehículo: "))
                
                # Validar fecha de inicio
                fecha_inicio = obtener_dato_validado(
                    validar_fecha,
                    "Fecha de inicio (YYYY-MM-DD): ",
                    "Fecha inválida",
                    "YYYY-MM-DD"
                )
                
                # Validar fecha de fin
                fecha_fin = obtener_dato_validado(
                    validar_fecha,
                    "Fecha de fin (YYYY-MM-DD): ",
                    "Fecha inválida",
                    "YYYY-MM-DD"
                )
                
                # Obtener valor UF para la fecha de inicio
                print(f"Buscando valor de UF para la fecha: {fecha_inicio}...")
                indicador_uf = IndicadorService.obtener_uf_por_fecha(fecha_inicio)
                
                # Validar que se obtuvo la UF correctamente
                if indicador_uf is None:
                    logger.error("No se pudo obtener la UF. Arriendo cancelado.")
                    print("❌ No se pudo obtener el valor de la UF. No se puede registrar el arriendo.")
                    continue
                
                valor_uf_obtenido = indicador_uf.getValor()
                fecha_uf_obtenida = indicador_uf.getFechaCorta()
                print(f"✅ UF encontrada (fecha {fecha_uf_obtenida}): ${valor_uf_obtenido:,.2f}")
                
                # Calcular días y costo
                fecha_ini = datetime.strptime(fecha_inicio, '%Y-%m-%d')
                fecha_f = datetime.strptime(fecha_fin, '%Y-%m-%d')
                dias = (fecha_f - fecha_ini).days
                
                if dias <= 0:
                    logger.warning("Fechas inválidas para arriendo: inicio %s, fin %s", fecha_inicio, fecha_fin)
                    print("❌ La fecha fin debe ser posterior a la fecha inicio")
                    continue
                
                vehiculo = vehiculodto.buscarVehiculoPorId(id_vehiculo)
                if not vehiculo:
                    logger.warning("Vehículo no encontrado para arriendo: ID %s", id_vehiculo)
                    print("❌ Vehículo no encontrado")
                    continue
                
                # El precio_diario del vehículo está en UF
                precio_diario_uf = vehiculo.getPrecioDiario()
                costo_total_pesos = (dias * precio_diario_uf) * valor_uf_obtenido
                
                print(f"\n📋 Resumen del arriendo:")
                print(f"   Días: {dias}")
                print(f"   Precio por día (UF): {precio_diario_uf} UF")
                print(f"   Valor UF consultado ({fecha_uf_obtenida}): ${valor_uf_obtenido:,.2f}")
                print(f"   Costo total (Pesos): {dias} días * {precio_diario_uf} UF * ${valor_uf_obtenido:,.2f} = ${costo_total_pesos:,.0f} CLP")
                
                confirmacion = input("\n¿Confirmar arriendo? (s/n): ")
                if confirmacion.lower() == 's':
                    if arriendodto.agregarArriendo(id_vehiculo, id_cliente, empleado_actual.getIdEmpleado(), 
                                                  fecha_inicio, fecha_fin, costo_total_pesos,
                                                  valor_uf_fecha=valor_uf_obtenido,
                                                  fecha_uf_consulta=fecha_uf_obtenida):
                        # Cambiar estado del vehículo a arrendado
                        vehiculodto.actualizarVehiculo(vehiculo.getPatente(), vehiculo.getMarca(), 
                                                      vehiculo.getModelo(), vehiculo.getAño(), 
                                                      vehiculo.getPrecioDiario(), "arrendado")
                        logger.info("Arriendo agregado exitosamente: vehículo %s, cliente %s", id_vehiculo, id_cliente)
                        print("✅ Arriendo agregado correctamente")
                    else:
                        logger.error("Error al agregar arriendo: vehículo %s, cliente %s", id_vehiculo, id_cliente)
                        print("❌ Error al agregar arriendo")
                        
            except ValueError as e:
                logger.error("Error de valor en arriendo: %s", str(e))
                print(f"❌ Error en los datos ingresados: {e}")
            except Exception as e:
                logger.error("Error inesperado en arriendo: %s", str(e))
                print(f"❌ Error: {e}")
                
        elif opcion == '2':
            logger.info("Buscando arriendo")
            print("\n--- BUSCAR ARRIENDO ---")
            try:
                id_arriendo = int(input("ID del arriendo: "))
                arriendo = arriendodto.buscarArriendo(id_arriendo)
                if arriendo:
                    logger.debug("Arriendo encontrado: %s", id_arriendo)
                    print(f"✅ Arriendo encontrado:")
                    print(f"   ID: {arriendo.getIdArriendo()}")
                    print(f"   ID Vehículo: {arriendo.getIdVehiculo()}")
                    print(f"   ID Cliente: {arriendo.getIdCliente()}")
                    print(f"   Fecha inicio: {arriendo.getFechaInicio()}")
                    print(f"   Fecha fin: {arriendo.getFechaFin()}")
                    print(f"   Costo total: ${arriendo.getCostoTotal():,.0f}")
                    print(f"   Estado: {arriendo.getEstado()}")
                else:
                    logger.debug("Arriendo no encontrado: %s", id_arriendo)
                    print("❌ Arriendo no encontrado")
            except ValueError:
                logger.warning("ID de arriendo inválido")
                print("❌ ID debe ser un número")
                
        elif opcion == '3':
            logger.info("Cancelando arriendo")
            print("\n--- CANCELAR ARRIENDO ---")
            try:
                id_arriendo = int(input("ID del arriendo a cancelar: "))
                arriendo = arriendodto.buscarArriendo(id_arriendo)
                if arriendo:
                    if arriendo.getEstado() == "activo":
                        # Verificar si se puede cancelar (hasta 4 horas antes)
                        fecha_inicio = datetime.strptime(str(arriendo.getFechaInicio()), '%Y-%m-%d')
                        ahora = datetime.now()
                        diferencia = fecha_inicio - ahora
                        
                        if diferencia.total_seconds() > 4 * 3600:  # 4 horas en segundos
                            confirmacion = input(f"¿Está seguro de cancelar el arriendo ID {id_arriendo}? (s/n): ")
                            if confirmacion.lower() == 's':
                                if arriendodto.actualizarArriendo(id_arriendo, arriendo.getIdVehiculo(), 
                                                                arriendo.getIdCliente(), arriendo.getIdEmpleado(),
                                                                arriendo.getFechaInicio(), arriendo.getFechaFin(),
                                                                arriendo.getCostoTotal(), "cancelado",
                                                                valor_uf_fecha=arriendo.getValorUfFecha(),
                                                                fecha_uf_consulta=arriendo.getFechaUfConsulta()):
                                    # Liberar vehículo
                                    vehiculo = vehiculodto.buscarVehiculoPorId(arriendo.getIdVehiculo())
                                    if vehiculo:
                                        vehiculodto.actualizarVehiculo(vehiculo.getPatente(), vehiculo.getMarca(), 
                                                                      vehiculo.getModelo(), vehiculo.getAño(), 
                                                                      vehiculo.getPrecioDiario(), "disponible")
                                    logger.info("Arriendo cancelado exitosamente: %s", id_arriendo)
                                    print("✅ Arriendo cancelado correctamente")
                                else:
                                    logger.error("Error al cancelar arriendo: %s", id_arriendo)
                                    print("❌ Error al cancelar arriendo")
                        else:
                            logger.warning("Intento de cancelación fuera de plazo: arriendo %s", id_arriendo)
                            print("❌ No se puede cancelar el arriendo. Debe cancelarse al menos 4 horas antes.")
                    else:
                        logger.warning("Intento de cancelar arriendo en estado %s: %s", arriendo.getEstado(), id_arriendo)
                        print(f"❌ El arriendo ya está {arriendo.getEstado()}")
                else:
                    logger.debug("Arriendo no encontrado para cancelación: %s", id_arriendo)
                    print("❌ Arriendo no encontrado")
            except ValueError:
                logger.warning("ID de arriendo inválido para cancelación")
                print("❌ ID debe ser un número")
                
        elif opcion == '4':
            logger.info("Listando todos los arriendos")
            print("\n--- LISTA DE ARRIENDOS ---")
            present_list = arriendodto.listarArriendosPresentacion()
            if present_list:
                logger.debug("Listados %d arriendos", len(present_list))
                for item in present_list:
                    arriendo = item['arriendo']
                    veh_info = item.get('vehiculo_info', f"Vehículo ID {arriendo.getIdVehiculo()}")
                    cli_info = item.get('cliente_info', f"Cliente ID {arriendo.getIdCliente()}")
                    estado_icon = "🟢" if arriendo.getEstado() == "activo" else "🟡" if arriendo.getEstado() == "finalizado" else "🔴"
                    print(f"ID: {arriendo.getIdArriendo()} - {veh_info} - Cliente: {cli_info}")
                    print(f"   Fechas: {arriendo.getFechaInicio()} a {arriendo.getFechaFin()} - Costo: ${arriendo.getCostoTotal():,.0f} - {estado_icon} {arriendo.getEstado()}\n")
            else:
                logger.debug("No hay arriendos registrados")
                print("📝 No hay arriendos registrados")
                
        elif opcion == '5':
            logger.info("Listando arriendos por fecha")
            print("\n--- ARRIENDOS POR FECHA ---")
            fecha = obtener_dato_validado(
                validar_fecha,
                "Ingrese fecha (YYYY-MM-DD): ",
                "Fecha inválida",
                "YYYY-MM-DD"
            )
            present_list = arriendodto.listarArriendosPorFechaPresentacion(fecha)
            if present_list:
                logger.debug("Listados %d arriendos para fecha %s", len(present_list), fecha)
                print(f"Arriendos para la fecha {fecha}:")
                for item in present_list:
                    arriendo = item['arriendo']
                    veh_info = item.get('vehiculo_info', f"Vehículo ID {arriendo.getIdVehiculo()}")
                    cli_info = item.get('cliente_info', f"Cliente ID {arriendo.getIdCliente()}")
                    estado_icon = "🟢" if arriendo.getEstado() == "activo" else "🟡" if arriendo.getEstado() == "finalizado" else "🔴"
                    print(f"  {veh_info} - Cliente: {cli_info} - {estado_icon} {arriendo.getEstado()}")
            else:
                logger.debug("No hay arriendos para fecha %s", fecha)
                print(f"📝 No hay arriendos para la fecha {fecha}")
                
        elif opcion == '6':
            logger.info("Saliendo de gestión de arriendos")
            break
        else:
            logger.warning("Opción inválida en gestión de arriendos: %s", opcion)
            print("❌ Opción no válida")

def generar_informes():
    """Generación de informes"""
    logger.info("Iniciando generación de informes")
    clientedto = ClienteDTO()
    vehiculodto = VehiculoDTO()
    userdto = UserDTO()
    arriendodto = ArriendoDTO()
    
    while True:
        print("""
=== GENERACIÓN DE INFORMES ===
1. Informe de Clientes
2. Informe de Vehículos
3. Informe de Empleados
4. Informe de Arriendos
5. Informe General del Sistema
6. Volver al Menú Principal
""")
        opcion = input("Seleccione una opción: ")
        
        if opcion == '1':
            logger.info("Generando informe de clientes")
            print("\n" + "="*50)
            print("           INFORME DE CLIENTES")
            print("="*50)
            clientes = clientedto.listarClientes()
            logger.debug("Informe clientes - Total: %d", len(clientes))
            print(f"Total de clientes: {len(clientes)}")
            print("-" * 50)
            for cliente in clientes:
                print(f"RUN: {cliente.getRun()}")
                print(f"Nombre: {cliente.getNombre()} {cliente.getApellido()}")
                print(f"Teléfono: {cliente.getTelefono()}")
                print(f"Dirección: {cliente.getDireccion()}")
                print("-" * 30)
                
        elif opcion == '2':
            logger.info("Generando informe de vehículos")
            print("\n" + "="*50)
            print("           INFORME DE VEHÍCULOS")
            print("="*50)
            vehiculos = vehiculodto.listarVehiculos()
            disponibles = vehiculodto.listarVehiculosDisponibles()
            arrendados = [v for v in vehiculos if v.getEstado() == "arrendado"]
            mantencion = [v for v in vehiculos if v.getEstado() == "mantencion"]
            
            logger.debug("Informe vehículos - Total: %d, Disponibles: %d, Arrendados: %d, Mantención: %d", 
                        len(vehiculos), len(disponibles), len(arrendados), len(mantencion))
            
            print(f"Total de vehículos: {len(vehiculos)}")
            print(f"Disponibles: {len(disponibles)}")
            print(f"Arrendados: {len(arrendados)}")
            print(f"En mantención: {len(mantencion)}")
            print("-" * 50)
            
            for vehiculo in vehiculos:
                estado_icon = "🟢" if vehiculo.getEstado() == "disponible" else "🔴" if vehiculo.getEstado() == "arrendado" else "🟡"
                print(f"{estado_icon} {vehiculo.getPatente()} - {vehiculo.getMarca()} {vehiculo.getModelo()} - Año: {vehiculo.getAño()} - ${vehiculo.getPrecioDiario():,.0f}/día")
                
        elif opcion == '3':
            logger.info("Generando informe de empleados")
            print("\n" + "="*50)
            print("           INFORME DE EMPLEADOS")
            print("="*50)
            empleados = userdto.listarUsuarios()
            gerentes = [e for e in empleados if e.getCargo() == 'gerente']
            empleados_normales = [e for e in empleados if e.getCargo() == 'empleado']
            
            logger.debug("Informe empleados - Total: %d, Gerentes: %d, Empleados: %d", 
                        len(empleados), len(gerentes), len(empleados_normales))
            
            print(f"Total de empleados: {len(empleados)}")
            print(f"Gerentes: {len(gerentes)}")
            print(f"Empleados: {len(empleados_normales)}")
            print("-" * 50)
            
            for empleado in empleados:
                cargo_icon = "👑" if empleado.getCargo() == 'gerente' else "👨‍💼"
                print(f"{cargo_icon} {empleado.getNombre()} {empleado.getApellido()} - RUN: {empleado.getRun()} - {empleado.getCargo()}")
                
        elif opcion == '4':
            logger.info("Generando informe de arriendos")
            print("\n" + "="*50)
            print("           INFORME DE ARRIENDOS")
            print("="*50)
            # Usar solo la lista de presentación (evita consultas/llamadas dobles)
            present_list = arriendodto.listarArriendosPresentacion()
            arriendos = [ item['arriendo'] for item in present_list ]
            present_map = { item['arriendo'].getIdArriendo(): item for item in present_list }
            activos = [a for a in arriendos if a.getEstado() == "activo"]
            finalizados = [a for a in arriendos if a.getEstado() == "finalizado"]
            cancelados = [a for a in arriendos if a.getEstado() == "cancelado"]
            
            logger.debug("Informe arriendos - Total: %d, Activos: %d, Finalizados: %d, Cancelados: %d", 
                        len(arriendos), len(activos), len(finalizados), len(cancelados))
            
            print(f"Total de arriendos: {len(arriendos)}")
            print(f"Activos: {len(activos)}")
            print(f"Finalizados: {len(finalizados)}")
            print(f"Cancelados: {len(cancelados)}")
            print("-" * 50)
            
            if arriendos:
                ingresos_totales = sum(a.getCostoTotal() for a in arriendos if a.getEstado() != "cancelado")
                logger.debug("Ingresos totales calculados: $%s", ingresos_totales)
                print(f"Ingresos totales: ${ingresos_totales:,.0f}")
                print("-" * 30)
                
            for arriendo in arriendos:
                estado_icon = "🟢" if arriendo.getEstado() == "activo" else "🟡" if arriendo.getEstado() == "finalizado" else "🔴"
                pres = present_map.get(arriendo.getIdArriendo(), {})
                veh_info = pres.get('vehiculo_info', f"Vehículo ID {arriendo.getIdVehiculo()}")
                cli_info = pres.get('cliente_info', f"Cliente ID {arriendo.getIdCliente()}")
                print(f"{estado_icon} ID: {arriendo.getIdArriendo()} - {veh_info}")
                print(f"   Cliente: {cli_info} - ${arriendo.getCostoTotal():,.0f} - {arriendo.getEstado()}")
                
        elif opcion == '5':
            logger.info("Generando informe general del sistema")
            print("\n" + "="*60)
            print("              INFORME GENERAL DEL SISTEMA")
            print("="*60)
            
            # Estadísticas generales
            clientes = clientedto.listarClientes()
            vehiculos = vehiculodto.listarVehiculos()
            empleados = userdto.listarUsuarios()
            arriendos = arriendodto.listarArriendos()
            
            logger.info("Informe general - Clientes: %d, Vehículos: %d, Empleados: %d, Arriendos: %d", 
                       len(clientes), len(vehiculos), len(empleados), len(arriendos))
            
            print(f"📊 ESTADÍSTICAS GENERALES:")
            print(f"   👥 Clientes registrados: {len(clientes)}")
            print(f"   🚗 Vehículos en flota: {len(vehiculos)}")
            print(f"   👨‍💼 Empleados activos: {len(empleados)}")
            print(f"   📋 Arriendos totales: {len(arriendos)}")
            
            if arriendos:
                ingresos_totales = sum(a.getCostoTotal() for a in arriendos if a.getEstado() != "cancelado")
                arriendos_activos = len([a for a in arriendos if a.getEstado() == "activo"])
                logger.debug("Informe general - Ingresos: $%s, Arriendos activos: %d", ingresos_totales, arriendos_activos)
                print(f"   💰 Ingresos totales: ${ingresos_totales:,.0f}")
                print(f"   📅 Arriendos activos: {arriendos_activos}")
                
            print("\n🚗 ESTADO DE VEHÍCULOS:")
            disponibles = len([v for v in vehiculos if v.getEstado() == "disponible"])
            arrendados = len([v for v in vehiculos if v.getEstado() == "arrendado"])
            mantencion = len([v for v in vehiculos if v.getEstado() == "mantencion"])
            logger.debug("Estado vehículos - Disponibles: %d, Arrendados: %d, Mantención: %d", 
                        disponibles, arrendados, mantencion)
            print(f"   🟢 Disponibles: {disponibles}")
            print(f"   🔴 Arrendados: {arrendados}")
            print(f"   🟡 En mantención: {mantencion}")
            
            print("\n📈 ESTADO DE ARRIENDOS:")
            activos = len([a for a in arriendos if a.getEstado() == "activo"])
            finalizados = len([a for a in arriendos if a.getEstado() == "finalizado"])
            cancelados = len([a for a in arriendos if a.getEstado() == "cancelado"])
            logger.debug("Estado arriendos - Activos: %d, Finalizados: %d, Cancelados: %d", 
                        activos, finalizados, cancelados)
            print(f"   🟢 Activos: {activos}")
            print(f"   🟡 Finalizados: {finalizados}")
            print(f"   🔴 Cancelados: {cancelados}")
            print("="*60)
                
        elif opcion == '6':
            logger.info("Saliendo de generación de informes")
            break
        else:
            logger.warning("Opción inválida en generación de informes: %s", opcion)
            print("❌ Opción no válida")
