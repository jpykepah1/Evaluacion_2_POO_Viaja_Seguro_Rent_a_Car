from controlador.validations import inicial, validarLogin
import getpass
import logging
from utils.logger import SistemaLogging
from typing import Optional

# Configurar sistema de logging
SistemaLogging.configurar(nivel=logging.INFO)
logger = logging.getLogger(__name__)

def menuAccesoUsuarios() -> None:
    """
    Muestra el menú de acceso principal del sistema.
    
    Este menú permite a los usuarios iniciar sesión, solicitar creación
    de cuentas o salir del sistema.
    """
    print("""
||------------------------||
||  Ingreso al Sistema    ||
||------------------------||
||1. Login de acceso      ||
||2. Crear cuenta usuario ||
||3. Salir del sistema    ||
||------------------------||
""")

def main() -> None:
    """
    Función principal que inicia la aplicación.
    
    Controla el flujo principal del sistema, mostrando el menú
    de acceso y gestionando las opciones seleccionadas por el usuario.
    
    El sistema permite hasta 3 intentos fallidos de login antes de
    bloquear el acceso temporalmente.
    """
    logger.info("Iniciando sistema de gestión de arriendos")
    
    while True:  
        print("=== SISTEMA DE GESTIÓN DE ARRIENDOS ===")
        print("=== Viaja Seguro Rent a Car ===")
        menuAccesoUsuarios()
        opcion = input("Ingrese opción: ")

        if opcion == '1':
            intentos = 1
            username: Optional[str] = None
            
            while intentos <= 3:
                try:
                    logger.debug("Intento de login #%d", intentos)
                    username = input("Ingrese RUN de empleado: ")
                    password = getpass.getpass("Ingrese contraseña: ")
                   
                    empleado = validarLogin(username, password)
                    if empleado is not None:
                        logger.info("Login exitoso para: %s %s", 
                                   empleado.getNombre(), empleado.getApellido())
                        print(f"\n✅ Bienvenido(a) Sr(a). : {empleado.getNombre()} {empleado.getApellido()}")
                        inicial(empleado)
                        break  
                    else:
                        logger.warning("Intento de login fallido para: %s (intento %d/3)", 
                                      username, intentos)
                        print("❌ Usuario o contraseña incorrecta")
                        intentos += 1
                except Exception as e:
                    logger.error("Error durante login: %s", str(e))
                    print("❌ Error, intentar nuevamente")
                    intentos += 1
           
            if intentos > 3:
                logger.warning("Cuenta bloqueada por múltiples intentos fallidos para: %s", 
                              username)
                print("🚫 Cuenta bloqueada por demasiados intentos fallidos")
                input("Presione Enter para continuar...")  
               
        elif opcion == '2':
            logger.info("Solicitada creación de nueva cuenta")
            print("Para crear una nueva cuenta, contacte al administrador del sistema.")
            input("Presione Enter para continuar...")
                   
        elif opcion == '3':
            logger.info("Sistema cerrado por el usuario")
            print("¡Hasta pronto!")
            break
        else:
            logger.warning("Opción inválida seleccionada: %s", opcion)
            print("❌ Opción no válida. Por favor, seleccione 1, 2 o 3.")
            input("Presione Enter para continuar...")

if __name__ == "__main__":
    main()
