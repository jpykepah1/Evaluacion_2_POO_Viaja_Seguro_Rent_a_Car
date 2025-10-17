from dto.dto_user import UserDTO
from dto.dto_cliente import ClienteDTO
from dto.dto_vehiculo import VehiculoDTO
from dto.dto_arriendo import ArriendoDTO
from modelo.empleado import Empleado
import getpass
from datetime import datetime, timedelta

def validarLogin(username, password):
    userdto = UserDTO()
    return userdto.validarLogin(username, password)

def inicial(empleado_actual):
    """Menú principal después del login"""
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
                gestion_empleados()
            else:
                print("❌ Solo los gerentes pueden gestionar empleados")
        elif opcion == '2':
            gestion_clientes()
        elif opcion == '3':
            gestion_vehiculos()
        elif opcion == '4':
            gestion_arriendos(empleado_actual)
        elif opcion == '5':
            generar_informes()
        elif opcion == '6':
            print("👋 Sesión cerrada")
            break
        else:
            print("❌ Opción no válida")

def gestion_empleados():
    """Gestión de empleados (solo para gerentes)"""
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
            print("\n--- AGREGAR EMPLEADO ---")
            run = input("RUN: ")
            nombre = input("Nombre: ")
            apellido = input("Apellido: ")
            password = getpass.getpass("Contraseña: ")
            cargo = input("Cargo (gerente/empleado): ").lower()
            
            if cargo not in ['gerente', 'empleado']:
                print("❌ Cargo no válido. Debe ser 'gerente' o 'empleado'")
                continue
                
            if userdto.agregarUsuario(run, nombre, apellido, password, cargo):
                print("✅ Empleado agregado correctamente")
            else:
                print("❌ Error al agregar empleado")
                
        elif opcion == '2':
            print("\n--- BUSCAR EMPLEADO ---")
            run = input("RUN del empleado: ")
            empleado = userdto.buscarUsuario(run)
            if empleado:
                print(f"✅ Empleado encontrado:")
                print(f"   RUN: {empleado.getRun()}")
                print(f"   Nombre: {empleado.getNombre()} {empleado.getApellido()}")
                print(f"   Cargo: {empleado.getCargo()}")
            else:
                print("❌ Empleado no encontrado")
                
        elif opcion == '3':
            print("\n--- ACTUALIZAR EMPLEADO ---")
            run = input("RUN del empleado a actualizar: ")
            empleado_existente = userdto.buscarUsuario(run)
            if empleado_existente:
                print(f"Empleado actual: {empleado_existente.getNombre()} {empleado_existente.getApellido()}")
                nombre = input(f"Nuevo nombre [{empleado_existente.getNombre()}]: ") or empleado_existente.getNombre()
                apellido = input(f"Nuevo apellido [{empleado_existente.getApellido()}]: ") or empleado_existente.getApellido()
                password = getpass.getpass("Nueva contraseña (dejar en blanco para no cambiar): ")
                cargo = input(f"Nuevo cargo [{empleado_existente.getCargo()}]: ") or empleado_existente.getCargo()
                
                if not password:  # Si no se cambia la contraseña, usar la existente
                    password = empleado_existente.getPassword()
                else:
                    from utils.encoder import Encoder
                    password = Encoder().encode(password)
                
                if userdto.actualizarUsuario(run, nombre, apellido, password, cargo):
                    print("✅ Empleado actualizado correctamente")
                else:
                    print("❌ Error al actualizar empleado")
            else:
                print("❌ Empleado no encontrado")
                
        elif opcion == '4':
            print("\n--- ELIMINAR EMPLEADO ---")
            run = input("RUN del empleado a eliminar: ")
            empleado = userdto.buscarUsuario(run)
            if empleado:
                confirmacion = input(f"¿Está seguro de eliminar a {empleado.getNombre()} {empleado.getApellido()}? (s/n): ")
                if confirmacion.lower() == 's':
                    if userdto.eliminarUsuario(run):
                        print("✅ Empleado eliminado correctamente")
                    else:
                        print("❌ Error al eliminar empleado")
            else:
                print("❌ Empleado no encontrado")
                
        elif opcion == '5':
            print("\n--- LISTA DE EMPLEADOS ---")
            empleados = userdto.listarUsuarios()
            if empleados:
                for i, empleado in enumerate(empleados, 1):
                    print(f"{i}. {empleado.getNombre()} {empleado.getApellido()} - RUN: {empleado.getRun()} - Cargo: {empleado.getCargo()}")
            else:
                print("📝 No hay empleados registrados")
                
        elif opcion == '6':
            break
        else:
            print("❌ Opción no válida")

def gestion_clientes():
    """Gestión completa de clientes"""
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
            print("\n--- AGREGAR CLIENTE ---")
            run = input("RUN: ")
            nombre = input("Nombre: ")
            apellido = input("Apellido: ")
            telefono = input("Teléfono: ")
            direccion = input("Dirección: ")

            if clientedto.agregarCliente(run, nombre, apellido, telefono, direccion):
                print("✅ Cliente agregado correctamente")
            else:
                print("❌ Error al agregar cliente")

        elif opcion == '2':
            print("\n--- BUSCAR CLIENTE ---")
            run = input("RUN del cliente: ")
            cliente = clientedto.buscarCliente(run)
            if cliente:
                print(f"✅ Cliente encontrado:")
                print(f"   ID: {cliente.getIdCliente()}")
                print(f"   RUN: {cliente.getRun()}")
                print(f"   Nombre: {cliente.getNombre()} {cliente.getApellido()}")
                print(f"   Teléfono: {cliente.getTelefono()}")
                print(f"   Dirección: {cliente.getDireccion()}")
            else:
                print("❌ Cliente no encontrado")

        elif opcion == '3':
            print("\n--- ACTUALIZAR CLIENTE ---")
            run = input("RUN del cliente a actualizar: ")
            cliente_existente = clientedto.buscarCliente(run)
            if cliente_existente:
                print(f"Cliente actual: {cliente_existente.getNombre()} {cliente_existente.getApellido()}")
                nombre = input(f"Nuevo nombre [{cliente_existente.getNombre()}]: ") or cliente_existente.getNombre()
                apellido = input(f"Nuevo apellido [{cliente_existente.getApellido()}]: ") or cliente_existente.getApellido()
                telefono = input(f"Nuevo teléfono [{cliente_existente.getTelefono()}]: ") or cliente_existente.getTelefono()
                direccion = input(f"Nueva dirección [{cliente_existente.getDireccion()}]: ") or cliente_existente.getDireccion()

                if clientedto.actualizarCliente(cliente_existente.getIdCliente(), cliente_existente.getRun(), nombre, apellido, telefono, direccion):
                    print("✅ Cliente actualizado correctamente")
                else:
                    print("❌ Error al actualizar cliente")
            else:
                print("❌ Cliente no encontrado")

        elif opcion == '4':
            print("\n--- ELIMINAR CLIENTE ---")
            run = input("RUN del cliente a eliminar: ")
            cliente = clientedto.buscarCliente(run)
            if cliente:
                confirmacion = input(f"¿Está seguro de eliminar a {cliente.getNombre()} {cliente.getApellido()}? (s/n): ")
                if confirmacion.lower() == 's':
                    if clientedto.eliminarCliente(cliente.getIdCliente()):
                        print("✅ Cliente eliminado correctamente")
                    else:
                        print("❌ Error al eliminar cliente")
            else:
                print("❌ Cliente no encontrado")

        elif opcion == '5':
            print("\n--- LISTA DE CLIENTES ---")
            clientes = clientedto.listarClientes()
            if clientes:
                for i, cliente in enumerate(clientes, 1):
                    print(f"{i}. {cliente.getNombre()} {cliente.getApellido()} - RUN: {cliente.getRun()} - ID: {cliente.getIdCliente()} - Tel: {cliente.getTelefono()}")
            else:
                print("📝 No hay clientes registrados")

        elif opcion == '6':
            break
        else:
            print("❌ Opción no válida")

def gestion_vehiculos():
    """Gestión completa de vehículos"""
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
            print("\n--- AGREGAR VEHÍCULO ---")
            patente = input("Patente: ").upper()
            marca = input("Marca: ")
            modelo = input("Modelo: ")
            try:
                año = int(input("Año: "))
                precio_diario = float(input("Precio diario: "))
            except ValueError:
                print("❌ Error: Año y precio deben ser números válidos")
                continue
                
            estado = input("Estado (disponible/mantencion) [disponible]: ").lower() or "disponible"
            
            if vehiculodto.agregarVehiculo(patente, marca, modelo, año, precio_diario, estado):
                print("✅ Vehículo agregado correctamente")
            else:
                print("❌ Error al agregar vehículo")
                
        elif opcion == '2':
            print("\n--- BUSCAR VEHÍCULO ---")
            patente = input("Patente del vehículo: ").upper()
            vehiculo = vehiculodto.buscarVehiculo(patente)
            if vehiculo:
                print(f"✅ Vehículo encontrado:")
                print(f"   Patente: {vehiculo.getPatente()}")
                print(f"   Marca: {vehiculo.getMarca()}")
                print(f"   Modelo: {vehiculo.getModelo()}")
                print(f"   Año: {vehiculo.getAño()}")
                print(f"   Precio diario: ${vehiculo.getPrecioDiario():,.0f}")
                print(f"   Estado: {vehiculo.getEstado()}")
            else:
                print("❌ Vehículo no encontrado")
                
        elif opcion == '3':
            print("\n--- ACTUALIZAR VEHÍCULO ---")
            patente = input("Patente del vehículo a actualizar: ").upper()
            vehiculo_existente = vehiculodto.buscarVehiculo(patente)
            if vehiculo_existente:
                print(f"Vehículo actual: {vehiculo_existente.getMarca()} {vehiculo_existente.getModelo()} - {vehiculo_existente.getPatente()}")
                marca = input(f"Nueva marca [{vehiculo_existente.getMarca()}]: ") or vehiculo_existente.getMarca()
                modelo = input(f"Nuevo modelo [{vehiculo_existente.getModelo()}]: ") or vehiculo_existente.getModelo()
                try:
                    año = input(f"Nuevo año [{vehiculo_existente.getAño()}]: ")
                    año = int(año) if año else vehiculo_existente.getAño()
                    precio_diario = input(f"Nuevo precio diario [{vehiculo_existente.getPrecioDiario():,.0f}]: ")
                    precio_diario = float(precio_diario) if precio_diario else vehiculo_existente.getPrecioDiario()
                except ValueError:
                    print("❌ Error: Año y precio deben ser números válidos")
                    continue
                    
                estado = input(f"Nuevo estado [{vehiculo_existente.getEstado()}]: ") or vehiculo_existente.getEstado()
                
                if vehiculodto.actualizarVehiculo(patente, marca, modelo, año, precio_diario, estado):
                    print("✅ Vehículo actualizado correctamente")
                else:
                    print("❌ Error al actualizar vehículo")
            else:
                print("❌ Vehículo no encontrado")
                
        elif opcion == '4':
            print("\n--- ELIMINAR VEHÍCULO ---")
            patente = input("Patente del vehículo a eliminar: ").upper()
            vehiculo = vehiculodto.buscarVehiculo(patente)
            if vehiculo:
                confirmacion = input(f"¿Está seguro de eliminar el vehículo {vehiculo.getMarca()} {vehiculo.getModelo()} ({vehiculo.getPatente()})? (s/n): ")
                if confirmacion.lower() == 's':
                    if vehiculodto.eliminarVehiculo(patente):
                        print("✅ Vehículo eliminado correctamente")
                    else:
                        print("❌ Error al eliminar vehículo")
            else:
                print("❌ Vehículo no encontrado")
                
        elif opcion == '5':
            print("\n--- LISTA DE VEHÍCULOS ---")
            vehiculos = vehiculodto.listarVehiculos()
            if vehiculos:
                for i, vehiculo in enumerate(vehiculos, 1):
                    estado_icon = "🟢" if vehiculo.getEstado() == "disponible" else "🟡" if vehiculo.getEstado() == "mantencion" else "🔴"
                    print(f"{i}. {vehiculo.getMarca()} {vehiculo.getModelo()} - {vehiculo.getPatente()} - Año: {vehiculo.getAño()} - Precio: ${vehiculo.getPrecioDiario():,.0f} - {estado_icon} {vehiculo.getEstado()}")
            else:
                print("📝 No hay vehículos registrados")
                
        elif opcion == '6':
            print("\n--- VEHÍCULOS DISPONIBLES ---")
            vehiculos = vehiculodto.listarVehiculosDisponibles()
            if vehiculos:
                for i, vehiculo in enumerate(vehiculos, 1):
                    print(f"{i}. {vehiculo.getMarca()} {vehiculo.getModelo()} - {vehiculo.getPatente()} - Año: {vehiculo.getAño()} - Precio: ${vehiculo.getPrecioDiario():,.0f}")
            else:
                print("📝 No hay vehículos disponibles")
                
        elif opcion == '7':
            break
        else:
            print("❌ Opción no válida")

def gestion_arriendos(empleado_actual):
    """Gestión de arriendos"""
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
            print("\n--- AGREGAR ARRIENDO ---")
            
            # Listar clientes
            print("\n--- CLIENTES DISPONIBLES ---")
            clientes = clientedto.listarClientes()
            if not clientes:
                print("❌ No hay clientes registrados. Debe registrar clientes primero.")
                continue
            for cliente in clientes:
                print(f"  ID: {cliente.getIdCliente()} - {cliente.getNombre()} {cliente.getApellido()}")
            
            try:
                id_cliente = int(input("\nID del cliente: "))
            except ValueError:
                print("❌ ID debe ser un número")
                continue
            
            # Listar vehículos disponibles
            print("\n--- VEHÍCULOS DISPONIBLES ---")
            vehiculos = vehiculodto.listarVehiculosDisponibles()
            if not vehiculos:
                print("❌ No hay vehículos disponibles")
                continue
            for vehiculo in vehiculos:
                print(f"  ID: {vehiculo.getIdVehiculo()} - {vehiculo.getMarca()} {vehiculo.getModelo()} - ${vehiculo.getPrecioDiario():,.0f}/día")
            
            try:
                id_vehiculo = int(input("\nID del vehículo: "))
                fecha_inicio = input("Fecha de inicio (YYYY-MM-DD): ")
                fecha_fin = input("Fecha de fin (YYYY-MM-DD): ")
                
                # Calcular días y costo
                fecha_ini = datetime.strptime(fecha_inicio, '%Y-%m-%d')
                fecha_f = datetime.strptime(fecha_fin, '%Y-%m-%d')
                dias = (fecha_f - fecha_ini).days
                
                if dias <= 0:
                    print("❌ La fecha fin debe ser posterior a la fecha inicio")
                    continue
                
                vehiculo = vehiculodto.buscarVehiculoPorId(id_vehiculo)
                if not vehiculo:
                    print("❌ Vehículo no encontrado")
                    continue
                    
                costo_total = dias * vehiculo.getPrecioDiario()
                
                print(f"\n📋 Resumen del arriendo:")
                print(f"   Días: {dias}")
                print(f"   Precio por día: ${vehiculo.getPrecioDiario():,.0f}")
                print(f"   Costo total: ${costo_total:,.0f}")
                
                confirmacion = input("\n¿Confirmar arriendo? (s/n): ")
                if confirmacion.lower() == 's':
                    if arriendodto.agregarArriendo(id_vehiculo, id_cliente, empleado_actual.getIdEmpleado(), 
                                                  fecha_inicio, fecha_fin, costo_total):
                        # Cambiar estado del vehículo a arrendado
                        vehiculodto.actualizarVehiculo(vehiculo.getPatente(), vehiculo.getMarca(), 
                                                      vehiculo.getModelo(), vehiculo.getAño(), 
                                                      vehiculo.getPrecioDiario(), "arrendado")
                        print("✅ Arriendo agregado correctamente")
                    else:
                        print("❌ Error al agregar arriendo")
                        
            except ValueError as e:
                print(f"❌ Error en los datos ingresados: {e}")
            except Exception as e:
                print(f"❌ Error: {e}")
                
        elif opcion == '2':
            print("\n--- BUSCAR ARRIENDO ---")
            try:
                id_arriendo = int(input("ID del arriendo: "))
                arriendo = arriendodto.buscarArriendo(id_arriendo)
                if arriendo:
                    print(f"✅ Arriendo encontrado:")
                    print(f"   ID: {arriendo.getIdArriendo()}")
                    print(f"   ID Vehículo: {arriendo.getIdVehiculo()}")
                    print(f"   ID Cliente: {arriendo.getIdCliente()}")
                    print(f"   Fecha inicio: {arriendo.getFechaInicio()}")
                    print(f"   Fecha fin: {arriendo.getFechaFin()}")
                    print(f"   Costo total: ${arriendo.getCostoTotal():,.0f}")
                    print(f"   Estado: {arriendo.getEstado()}")
                else:
                    print("❌ Arriendo no encontrado")
            except ValueError:
                print("❌ ID debe ser un número")
                
        elif opcion == '3':
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
                                                                arriendo.getCostoTotal(), "cancelado"):
                                    # Liberar vehículo
                                    vehiculo = vehiculodto.buscarVehiculoPorId(arriendo.getIdVehiculo())
                                    if vehiculo:
                                        vehiculodto.actualizarVehiculo(vehiculo.getPatente(), vehiculo.getMarca(), 
                                                                      vehiculo.getModelo(), vehiculo.getAño(), 
                                                                      vehiculo.getPrecioDiario(), "disponible")
                                    print("✅ Arriendo cancelado correctamente")
                                else:
                                    print("❌ Error al cancelar arriendo")
                        else:
                            print("❌ No se puede cancelar el arriendo. Debe cancelarse al menos 4 horas antes.")
                    else:
                        print(f"❌ El arriendo ya está {arriendo.getEstado()}")
                else:
                    print("❌ Arriendo no encontrado")
            except ValueError:
                print("❌ ID debe ser un número")
                
        elif opcion == '4':
            print("\n--- LISTA DE ARRIENDOS ---")
            arriendos = arriendodto.listarArriendos()
            if arriendos:
                for arriendo in arriendos:
                    estado_icon = "🟢" if arriendo.getEstado() == "activo" else "🟡" if arriendo.getEstado() == "finalizado" else "🔴"
                    print(f"ID: {arriendo.getIdArriendo()} - {arriendo.info_vehiculo} - Cliente: {arriendo.info_cliente}")
                    print(f"   Fechas: {arriendo.getFechaInicio()} a {arriendo.getFechaFin()} - Costo: ${arriendo.getCostoTotal():,.0f} - {estado_icon} {arriendo.getEstado()}\n")
            else:
                print("📝 No hay arriendos registrados")
                
        elif opcion == '5':
            print("\n--- ARRIENDOS POR FECHA ---")
            fecha = input("Ingrese fecha (YYYY-MM-DD): ")
            arriendos = arriendodto.listarArriendosPorFecha(fecha)
            if arriendos:
                print(f"Arriendos para la fecha {fecha}:")
                for arriendo in arriendos:
                    estado_icon = "🟢" if arriendo.getEstado() == "activo" else "🟡" if arriendo.getEstado() == "finalizado" else "🔴"
                    print(f"  {arriendo.info_vehiculo} - Cliente: {arriendo.info_cliente} - {estado_icon} {arriendo.getEstado()}")
            else:
                print(f"📝 No hay arriendos para la fecha {fecha}")
                
        elif opcion == '6':
            break
        else:
            print("❌ Opción no válida")

def generar_informes():
    """Generación de informes"""
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
            print("\n" + "="*50)
            print("           INFORME DE CLIENTES")
            print("="*50)
            clientes = clientedto.listarClientes()
            print(f"Total de clientes: {len(clientes)}")
            print("-" * 50)
            for cliente in clientes:
                print(f"RUN: {cliente.getRun()}")
                print(f"Nombre: {cliente.getNombre()} {cliente.getApellido()}")
                print(f"Teléfono: {cliente.getTelefono()}")
                print(f"Dirección: {cliente.getDireccion()}")
                print("-" * 30)
                
        elif opcion == '2':
            print("\n" + "="*50)
            print("           INFORME DE VEHÍCULOS")
            print("="*50)
            vehiculos = vehiculodto.listarVehiculos()
            disponibles = vehiculodto.listarVehiculosDisponibles()
            arrendados = [v for v in vehiculos if v.getEstado() == "arrendado"]
            mantencion = [v for v in vehiculos if v.getEstado() == "mantencion"]
            
            print(f"Total de vehículos: {len(vehiculos)}")
            print(f"Disponibles: {len(disponibles)}")
            print(f"Arrendados: {len(arrendados)}")
            print(f"En mantención: {len(mantencion)}")
            print("-" * 50)
            
            for vehiculo in vehiculos:
                estado_icon = "🟢" if vehiculo.getEstado() == "disponible" else "🔴" if vehiculo.getEstado() == "arrendado" else "🟡"
                print(f"{estado_icon} {vehiculo.getPatente()} - {vehiculo.getMarca()} {vehiculo.getModelo()} - Año: {vehiculo.getAño()} - ${vehiculo.getPrecioDiario():,.0f}/día")
                
        elif opcion == '3':
            print("\n" + "="*50)
            print("           INFORME DE EMPLEADOS")
            print("="*50)
            empleados = userdto.listarUsuarios()
            gerentes = [e for e in empleados if e.getCargo() == 'gerente']
            empleados_normales = [e for e in empleados if e.getCargo() == 'empleado']
            
            print(f"Total de empleados: {len(empleados)}")
            print(f"Gerentes: {len(gerentes)}")
            print(f"Empleados: {len(empleados_normales)}")
            print("-" * 50)
            
            for empleado in empleados:
                cargo_icon = "👑" if empleado.getCargo() == 'gerente' else "👨‍💼"
                print(f"{cargo_icon} {empleado.getNombre()} {empleado.getApellido()} - RUN: {empleado.getRun()} - {empleado.getCargo()}")
                
        elif opcion == '4':
            print("\n" + "="*50)
            print("           INFORME DE ARRIENDOS")
            print("="*50)
            arriendos = arriendodto.listarArriendos()
            activos = [a for a in arriendos if a.getEstado() == "activo"]
            finalizados = [a for a in arriendos if a.getEstado() == "finalizado"]
            cancelados = [a for a in arriendos if a.getEstado() == "cancelado"]
            
            print(f"Total de arriendos: {len(arriendos)}")
            print(f"Activos: {len(activos)}")
            print(f"Finalizados: {len(finalizados)}")
            print(f"Cancelados: {len(cancelados)}")
            print("-" * 50)
            
            if arriendos:
                ingresos_totales = sum(a.getCostoTotal() for a in arriendos if a.getEstado() != "cancelado")
                print(f"Ingresos totales: ${ingresos_totales:,.0f}")
                print("-" * 30)
                
            for arriendo in arriendos:
                estado_icon = "🟢" if arriendo.getEstado() == "activo" else "🟡" if arriendo.getEstado() == "finalizado" else "🔴"
                print(f"{estado_icon} ID: {arriendo.getIdArriendo()} - {arriendo.info_vehiculo}")
                print(f"   Cliente: {arriendo.info_cliente} - ${arriendo.getCostoTotal():,.0f} - {arriendo.getEstado()}")
                
        elif opcion == '5':
            print("\n" + "="*60)
            print("              INFORME GENERAL DEL SISTEMA")
            print("="*60)
            
            # Estadísticas generales
            clientes = clientedto.listarClientes()
            vehiculos = vehiculodto.listarVehiculos()
            empleados = userdto.listarUsuarios()
            arriendos = arriendodto.listarArriendos()
            
            print(f"📊 ESTADÍSTICAS GENERALES:")
            print(f"   👥 Clientes registrados: {len(clientes)}")
            print(f"   🚗 Vehículos en flota: {len(vehiculos)}")
            print(f"   👨‍💼 Empleados activos: {len(empleados)}")
            print(f"   📋 Arriendos totales: {len(arriendos)}")
            
            if arriendos:
                ingresos_totales = sum(a.getCostoTotal() for a in arriendos if a.getEstado() != "cancelado")
                arriendos_activos = len([a for a in arriendos if a.getEstado() == "activo"])
                print(f"   💰 Ingresos totales: ${ingresos_totales:,.0f}")
                print(f"   📅 Arriendos activos: {arriendos_activos}")
                
            print("\n🚗 ESTADO DE VEHÍCULOS:")
            disponibles = len([v for v in vehiculos if v.getEstado() == "disponible"])
            arrendados = len([v for v in vehiculos if v.getEstado() == "arrendado"])
            mantencion = len([v for v in vehiculos if v.getEstado() == "mantencion"])
            print(f"   🟢 Disponibles: {disponibles}")
            print(f"   🔴 Arrendados: {arrendados}")
            print(f"   🟡 En mantención: {mantencion}")
            
            print("\n📈 ESTADO DE ARRIENDOS:")
            activos = len([a for a in arriendos if a.getEstado() == "activo"])
            finalizados = len([a for a in arriendos if a.getEstado() == "finalizado"])
            cancelados = len([a for a in arriendos if a.getEstado() == "cancelado"])
            print(f"   🟢 Activos: {activos}")
            print(f"   🟡 Finalizados: {finalizados}")
            print(f"   🔴 Cancelados: {cancelados}")
            print("="*60)
                
        elif opcion == '6':
            break
        else:
            print("❌ Opción no válida")