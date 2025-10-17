from controlador.validations import inicial, validarLogin
import getpass

def menuAccesoUsuarios():
    print("""
||------------------------||
||  Ingreso al Sistema    ||
||------------------------||
||1. Login de acceso      ||
||2. Crear cuenta usuario ||
||3. Salir del sistema    ||
||------------------------||
""")

def main():
    while True:  
        print("=== SISTEMA DE GESTIÓN DE ARRIENDOS ===")
        print("=== Viaja Seguro Rent a Car ===")
        menuAccesoUsuarios()
        opcion = input("Ingrese opción: ")

        if opcion == '1':
            intentos = 1
            while intentos <= 3:
                try:
                    print(f"\n--- Intento {intentos} de 3 ---")
                    username = input("Ingrese RUN de empleado: ")
                    password = getpass.getpass("Ingrese contraseña: ")
                   
                    empleado = validarLogin(username, password)
                    if empleado is not None:
                        print(f"\n✅ Bienvenido(a) Sr(a). : {empleado.getNombre()} {empleado.getApellido()}")
                        inicial(empleado)
                        break  
                    else:
                        print("❌ Usuario o contraseña incorrecta")
                        intentos += 1
                except Exception as e:
                    print("❌ Error, intentar nuevamente")
                    print(f"Error: {e}")
           
            if intentos > 3:
                print("🚫 Cuenta bloqueada por demasiados intentos fallidos")
                input("Presione Enter para continuar...")  
               
        elif opcion == '2':
            print("Para crear una nueva cuenta, contacte al administrador del sistema.")
            input("Presione Enter para continuar...")
                   
        elif opcion == '3':
            print("¡Hasta pronto!")
            break
        else:
            print("❌ Opción no válida. Por favor, seleccione 1, 2 o 3.")
            input("Presione Enter para continuar...")

if __name__ == "__main__":
    main()