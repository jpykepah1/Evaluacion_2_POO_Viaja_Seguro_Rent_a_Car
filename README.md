<h1 align="center">
  🚗 Sistema de Gestión de Arriendos - <i>Viaja Seguro Rent a Car</i>
</h1>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.12%2B-blue?logo=python&logoColor=white" alt="Python Badge"/>
  <img src="https://img.shields.io/badge/MySQL-Database-orange?logo=mysql&logoColor=white" alt="MySQL Badge"/>
  <img src="https://img.shields.io/badge/XAMPP-Localhost-brightgreen?logo=xampp&logoColor=white" alt="XAMPP Badge"/>
  <img src="https://img.shields.io/badge/PyMySQL-Connector-lightblue?logo=python&logoColor=white" alt="PyMySQL Badge"/>
  <img src="https://img.shields.io/badge/MVC-Architecture-green?logo=diagram-project&logoColor=white" alt="MVC Badge"/>
  <img src="https://img.shields.io/badge/Security-Bcrypt-red?logo=security&logoColor=white" alt="Security Badge"/>
  <img src="https://img.shields.io/badge/License-Academic-lightgrey" alt="Academic License Badge"/>
</p>

---

## 📋 Descripción del Proyecto

Sistema completo de gestión para una empresa de arriendo de vehículos, desarrollado en **Python** bajo una arquitectura **MVC**, utilizando **XAMPP** y **MySQL** como entorno de base de datos, y **PyMySQL** como conector backend seguro.

> **Contexto Académico:** Proyecto de la asignatura *“Programación Orientada a Objeto Seguro (TI3021)”*.  
> Implementa principios de **POO**, **seguridad de contraseñas** y **gestión modular** de usuarios, clientes, vehículos y arriendos.

---

## 🧩 Tecnologías Utilizadas

| Tecnología | Descripción |
|-------------|--------------|
| 🐍 **Python 3.12+** | Lenguaje principal del proyecto |
| 🧱 **MySQL (XAMPP)** | Motor de base de datos local |
| 🔗 **PyMySQL** | Librería para conexión con MySQL |
| 🧩 **MVC (Model-View-Controller)** | Arquitectura para separar capas |
| 🔐 **bcrypt** | Cifrado de contraseñas seguras |
| ⚙️ **DAO / DTO Patterns** | Acceso y transferencia de datos |
| 💻 **Terminal CLI** | Interfaz de usuario por consola |

---

## 📦 Instalación y Ejecución

### 1️⃣ Clonar el Repositorio
```bash
git clone https://github.com/usuario/viaja-seguro.git
cd viaja-seguro
```

### 2️⃣ Configurar la Base de Datos (XAMPP + MySQL)
1. Inicia **XAMPP** y activa **Apache** y **MySQL**.  
2. Abre **phpMyAdmin** y crea una base de datos llamada:
   ```sql
   CREATE DATABASE viaja_seguro;
   ```
3. Ejecuta el archivo `create.sql` incluido en el proyecto para generar las tablas.

### 3️⃣ Instalar las Dependencias
Crea un entorno virtual e instala los paquetes requeridos:
```bash
python -m venv venv
source venv/bin/activate      # En Linux/Mac
# o
venv\Scripts\activate       # En Windows

pip install -r requirements.txt
```

### 4️⃣ Configurar la Conexión (Archivo `/conex/conex.py`)
Asegúrate de que los parámetros coincidan con tu entorno XAMPP:
```python
class Conex:
    def __init__(self, host="localhost", user="root", passwd="", database="viaja_seguro"):
        self.host = host
        self.user = user
        self.passwd = passwd
        self.database = database
```

### 5️⃣ Ejecutar el Sistema
```bash
python main.py
```

Una vez ejecutado, accederás al menú principal del sistema de gestión.

---

## 👥 Roles de Usuario

| Rol | RUN | Contraseña | Permisos |
|------|------|-------------|-----------|
| 👨‍💼 **Gerente (Administrador)** | `12345678-9` | `admin123` | Acceso completo a todos los módulos del sistema |
| 👨‍🔧 **Empleado (Usuario Normal)** | `98765432-1` | `admin123` | Gestión de clientes, vehículos y arriendos (sin acceso a gestión de empleados) |

---

## 🏗️ Arquitectura del Sistema

### Patrón MVC Implementado
```
MVC/
├── 📁 modelo/          # Entidades del negocio
├── 📁 dao/             # Data Access Object (Persistencia)
├── 📁 dto/             # Data Transfer Object (Transferencia)
├── 📁 controlador/     # Lógica de negocio
├── 📁 conex/           # Conexión a base de datos (PyMySQL)
├── 📁 utils/           # Utilidades (Seguridad, validaciones, encoder)
└── 🚀 main.py          # Punto de entrada del sistema
```

---

## 🔐 Seguridad Implementada

### Autenticación
- Inicio de sesión con **RUN** y **contraseña cifrada (bcrypt)**  
- Límite de intentos fallidos (3)  
- Cierre de sesión y control de roles

### Autorización
- **Gerente:** acceso total a todos los módulos  
- **Empleado:** acceso restringido

---

## 💾 Estructura de Base de Datos (Resumen)
```
viaja_seguro
├── empleado
├── cliente
├── vehiculo
└── arriendo
```

---

## 👨‍💻 Autor

**Viaja Seguro Rent a Car - Sistema de Gestión**  
Proyecto académico desarrollado por estudiantes de la asignatura  
*Programación Orientada a Objeto Seguro (TI3021)*.  

> 🚀 Implementación orientada a objetos, conexión segura MySQL, y patrón MVC en Python.

---
