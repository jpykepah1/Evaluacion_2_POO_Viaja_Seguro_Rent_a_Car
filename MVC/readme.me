<h1 align="center">
  🚗 Sistema de Gestión de Arriendos - <i>Viaja Seguro Rent a Car</i>
</h1>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.12%2B-blue?logo=python&logoColor=white" alt="Python Badge"/>
  <img src="https://img.shields.io/badge/MySQL-Database-orange?logo=mysql&logoColor=white" alt="MySQL Badge"/>
  <img src="https://img.shields.io/badge/MVC-Architecture-green?logo=diagram-project&logoColor=white" alt="MVC Badge"/>
  <img src="https://img.shields.io/badge/Security-Bcrypt-red?logo=security&logoColor=white" alt="Security Badge"/>
  <img src="https://img.shields.io/badge/License-Academic-lightgrey" alt="Academic License Badge"/>
</p>

---

## 📋 Descripción del Proyecto

Sistema completo de gestión para una empresa de arriendo de vehículos, desarrollado en **Python** con arquitectura **MVC**, conexión a base de datos **MySQL** y enfoque en **seguridad informática**.

> **Contexto Académico:** Proyecto para la asignatura *“Programación Orientada a Objeto Seguro” (TI3021)*.  
> Implementa principios de **POO**, **patrones de diseño** y **conexión segura** a bases de datos.

---

## 🏗️ Arquitectura del Sistema

### Patrón MVC Implementado
```
MVC/
├── 📁 modelo/          # Entidades del negocio
├── 📁 dao/             # Data Access Object (Persistencia)
├── 📁 dto/             # Data Transfer Object (Transferencia)
├── 📁 controlador/     # Lógica de negocio
├── 📁 conex/           # Conexión a base de datos
├── 📁 utils/           # Utilidades
└── 🚀 main.py          # Punto de entrada
```

### Diagrama de Clases (Resumen)
```
Persona (Abstracta)
├── User (Empleado)
└── Cliente

Vehiculo
Arriendo

Conex (Conexión BD)
Encoder (Seguridad)
```

---

## 📁 Estructura Detallada del Código

### 1. Capa de Modelo (/modelo)
Ejemplo de clase base:
```python
class Persona(ABC):
    def __init__(self, run="", nombre="", apellido=""):
        self._run = run
        self._nombre = nombre
        self._apellido = apellido
    
    @abstractmethod
    def mostrar_info(self):
        pass
```
Otras clases: `User`, `Cliente`, `Vehiculo`, `Arriendo`.

---

### 2. Capa de Persistencia (/dao)
```python
class daoUser:
    def validarLogin(self, user):
        sql = "SELECT run, password FROM empleado WHERE run = %s"
    
    def agregarUsuario(self, user):
        sql = "INSERT INTO empleado (run, password, nombre, apellido, cargo) VALUES (%s, %s, %s, %s, %s)"
```
🧩 Archivos adicionales: `dao_cliente.py`, `dao_vehiculo.py`, `dao_arriendo.py`

---

### 3. Capa de Transferencia (/dto)
```python
class UserDTO:
    def validarLogin(self, username, clave):
        resultado = daouser.validarLogin(User(run=username))
        if resultado and Encoder().verify(clave, password_hash_db):
            return User(...)
```

---

### 4. Capa de Controlador (/controlador)
```python
def inicial(empleado_actual):
    while True:
        mostrar_menu_principal()
        opcion = input("Seleccione una opción: ")
        if opcion == '1': gestion_empleados()
        elif opcion == '2': gestion_clientes()
```

---

### 5. Utilidades (/utils)
```python
class Encoder:
    def encode(self, password):
        return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    
    def verify(self, password, hashed_password):
        return bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8'))
```

---

### 6. Conexión a BD (/conex)
```python
class Conex:
    def __init__(self, host="localhost", user="root", passwd="", database="viaja_seguro"):
        self.host = host
        self.user = user
        self.passwd = passwd
        self.database = database
        self.__myconn = None
        self.connect()
```

---

### 7. Punto de Entrada (main.py)
```python
def main():
    while True:
        print("=== SISTEMA DE GESTIÓN DE ARRIENDOS ===")
        menuAccesoUsuarios()
        opcion = input("Ingrese opción: ")
        if opcion == '1':
            username = input("RUN empleado: ")
            password = getpass.getpass("Contraseña: ")
            empleado = validarLogin(username, password)
            if empleado:
                inicial(empleado)
```

---

## 🔐 Sistema de Seguridad

### 🔑 Autenticación
- Login seguro con **RUN** y **contraseña**
- Límite de intentos (3)
- Contraseñas **encriptadas con bcrypt**
- Bloqueo automático tras múltiples fallos

### 🛡️ Autorización
- Roles: **Gerente** vs **Empleado**
- Permisos granulares
- Validación de sesiones

---

## 🧩 Tecnologías Utilizadas
- **Python 3.12+**
- **MySQL**
- **bcrypt**
- **pymysql**
- **Arquitectura MVC**

---

## 📦 Instalación y Ejecución
```bash
git clone https://github.com/usuario/viaja-seguro.git
cd viaja-seguro
python -m venv venv
source venv/bin/activate  # o .\venv\Scripts\activate
pip install -r requirements.txt
python main.py
```

---

## 👨‍💻 Autor
**Viaja Seguro Rent a Car - Sistema de Gestión**  
Desarrollado para fines académicos por estudiantes del ramo *Programación Orientada a Objeto Seguro (TI3021)*.

---
