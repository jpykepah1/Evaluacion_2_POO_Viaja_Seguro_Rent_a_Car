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

## 🆕 Actualizaciones recientes (2025-11-19)

- Agregado soporte ES3/UF en arriendos: se almacenan `valor_uf_fecha` y `fecha_uf_consulta` para auditoría.
- El cálculo de costo ahora usa la UF consultada: `costo_clp = (dias * precio_diario_en_uf) * valor_uf`.
- Se mejoró el rendimiento de listados: el DAO ahora devuelve arriendos con campos de vehículo/cliente en una sola consulta (evita N+1 queries).
- Se añadieron validaciones de seguridad en `MVC/validador_formatos.py` (detección básica de inyección SQL, sanitización, validación de contraseñas y wrapper de cifrado).

> Nota: `vehiculo.precio_diario` en los datos de ejemplo está expresado en UF; revise su migración si tenía valores en CLP.

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
├── 📁 controlador/     # Lógica de negocio (Validaciones, Menu)
├── 📁 conex/           # Conexión a base de datos (PyMySQL)
├── 📁 utils/           # Utilidades (encoder)
└── 🚀 main.py          # Punto de entrada del sistema
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

## 🔐 Seguridad Implementada

### Autenticación
- Inicio de sesión con **RUN** y **contraseña cifrada (bcrypt)**  
- Límite de intentos fallidos (3)  
- Cierre de sesión y control de roles

### Autorización
- **Gerente:** acceso total a todos los módulos  
- **Empleado:** acceso restringido

### 🛡️ Validaciones de Seguridad Avanzadas (2025-11-19)

Se han integrado **4 nuevas funciones de seguridad** en `validador_formatos.py`:

#### 1. **Detección de Inyección SQL** (`validar_entrada_sql()`)
- Detecta palabras clave SQL sospechosas: `SELECT`, `INSERT`, `UPDATE`, `DELETE`, `DROP`, `UNION`
- Identifica comentarios SQL: `--`, `#`, `/* */`
- Previene patrones comunes: `OR 1=1`, `AND 1=1`
- Rechaza entradas demasiado largas (>255 caracteres)
- **Aplicado en**: Creación de empleados y clientes

```python
# Ejemplos
validar_entrada_sql("Juan'; DROP TABLE empleado; --")  # ❌ Rechazado
validar_entrada_sql("Juan Perez")                        # ✅ Aceptado
```

#### 2. **Política de Contraseña Fuerte** (`validar_password_segura()`)
- Requiere mínimo **8 caracteres**
- Al menos una **mayúscula**, una **minúscula**, un **dígito** y un **carácter especial**
- **Aplicado en**: Creación y actualización de empleados

```python
# Ejemplos
validar_password_segura("Pass123!")          # ✅ Aceptado
validar_password_segura("weak")               # ❌ Muy corta
validar_password_segura("NoDigits!")          # ❌ Sin dígitos
validar_password_segura("nouppercase123!")   # ❌ Sin mayúscula
```

#### 3. **Sanitización de Texto** (`sanitizar_texto()`)
- Remueve caracteres potencialmente peligrosos: `;`, `\`, `'`, `"`, `-`, `#`, `*`
- Útil para preparar datos antes de registrarlos

```python
sanitizar_texto("user'; DROP--")  # Resultado: "user DROP"
```

#### 4. **Cifrado de Datos Sensibles** (`cifrar_datos_sensibles()`)
- Wrapper para cifrado usando `utils.encoder.Encoder`
- Protege información sensible cuando es necesaria

### 📋 Flujo de Seguridad en Operaciones Críticas

**Al agregar un empleado:**
1. Valida contraseña según política fuerte ✅
2. Verifica entrada SQL en todos los campos ✅
3. Si hay patrones sospechosos: registra advertencia + cancela operación
4. Si todo es válido: procede con la inserción

**Ejemplo de intento de inyección:**
```
[INPUT] Nombre: "Juan'; DROP TABLE empleado; --"
[LOG] Intento de inyección SQL detectado...
[OUTPUT] "[ERROR] Datos sospechosos detectados. Operación cancelada."
```

### ✅ Suite de Pruebas (18 tests)

Archivo: `test_security_functions.py`
- 7 pruebas para detección de inyección SQL
- 6 pruebas para validación de contraseñas fuertes
- 5 pruebas para sanitización de texto
- 1 prueba de integración

**Resultado**: **18/18 tests pasados** ✅

```bash
python -m unittest test_security_functions.py -v
```

---

## 💾 Estructura de Base de Datos (Resumen)
```
viaja_seguro
├── empleado
├── cliente
├── vehiculo
└── arriendo
```
# 🔧 Archivos de Diagnóstico y Utilidad

## 📁 Archivos de Soporte Técnico

El proyecto incluye varios archivos de diagnóstico y utilidad que fueron creados durante el desarrollo para resolver problemas específicos y verificar el funcionamiento del sistema.

## 1. `diagnostico_final.py` - Verificador Completo del Sistema

### **Propósito**
Archivo de diagnóstico integral que verifica todos los componentes críticos del sistema antes de ponerlo en producción.

### **Funcionalidades Implementadas**

```python
def test_simple():
    """
    Prueba básica de conexión a la base de datos
    Verifica que:
    - La conexión se establece correctamente
    - Las consultas SQL funcionan
    - Los datos pueden ser recuperados
    """
    try:
        conex = Conex()
        conn = conex.getConex()
        cursor = conn.cursor()
        
        # Consulta simple para verificar conexión
        cursor.execute("SELECT run, password FROM empleado WHERE run = '12345678-9'")
        result = cursor.fetchone()
        
        print("✅ Consulta exitosa")
        print(f"RUN: {result[0]}")
        print(f"Password hash: {result[1][:30]}...")
        
        cursor.close()
        return True
    except Exception as e:
        print(f"❌ Error: {e}")
        return False
```

```python
def test_login_simple():
    """
    Prueba específica del sistema de login
    Verifica que:
    - El DAO de usuarios funciona correctamente
    - La validación de credenciales opera como se espera
    - El objeto User se crea correctamente
    """
    try:
        from dao.dao_user import daoUser
        from modelo.user import User
        
        dao = daoUser()
        user = User(run='12345678-9')
        result = dao.validarLogin(user)
        
        if result:
            print("✅ validarLogin exitoso")
            print(f"Datos retornados: {len(result)} elementos")
            return True
        else:
            print("❌ validarLogin retornó None")
            return False
    except Exception as e:
        print(f"❌ Error en test_login_simple: {e}")
        import traceback
        traceback.print_exc()
        return False
```

### **Uso Práctico**
```bash
# Ejecutar diagnóstico completo
python diagnostico_final.py

# Salida esperada:
🔍 DIAGNÓSTICO FINAL
========================================
✅ Consulta exitosa
RUN: 12345678-9
Password hash: $2b$12$KcCwvJQ4qQ4q4q4q4q4q4u...
✅ validarLogin exitoso
Datos retornados: 6 elementos
========================================
🎉 Diagnóstico exitoso - El sistema debería funcionar
```

### **Casos de Uso**
- ✅ **Despliegue inicial**: Verificar que todo funciona antes del primer uso
- ✅ **Solución de problemas**: Diagnosticar errores específicos
- ✅ **Después de cambios**: Validar que modificaciones no rompan funcionalidades
- ✅ **Documentación técnica**: Mostrar el estado actual del sistema

---

## 2. `generar_password.py` - Generador de Contraseñas Seguras

### **Propósito**
Herramienta para generar y verificar contraseñas encriptadas con bcrypt, esencial para la configuración inicial de usuarios.

### **Funcionalidades Principales**

```python
def generar_password(password_texto):
    """
    Genera un hash bcrypt seguro a partir de una contraseña en texto plano
    Usa 12 rounds de encriptación para equilibrio entre seguridad y rendimiento
    
    Args:
        password_texto (str): Contraseña en texto plano a encriptar
    
    Returns:
        str: Hash bcrypt de la contraseña
    """
    salt = bcrypt.gensalt(rounds=12)
    hashed = bcrypt.hashpw(password_texto.encode('utf-8'), salt)
    return hashed.decode('utf-8')
```

```python
def verificar_password(password_texto, password_hash):
    """
    Verifica si una contraseña en texto plano coincide con un hash bcrypt
    
    Args:
        password_texto (str): Contraseña a verificar
        password_hash (str): Hash almacenado para comparar
    
    Returns:
        bool: True si la contraseña coincide, False en caso contrario
    """
    return bcrypt.checkpw(password_texto.encode('utf-8'), password_hash.encode('utf-8'))
```

### **Ejemplo de Uso**
```bash
# Ejecutar generador de contraseñas
python generar_password.py

# Salida esperada:
==================================================
GENERADOR DE CONTRASEÑAS
==================================================
Contraseña en texto: admin123
Hash generado: $2b$12$KcCwvJQ4qQ4q4q4q4q4q4uQ4q4q4q4q4q4q4q4q4q4q4q4q4q4q
Longitud del hash: 60
Verificación: True

📋 Para usar en SQL:
INSERT INTO empleado (run, password, nombre, apellido, cargo) VALUES 
('12345678-9', '$2b$12$KcCwvJQ4qQ4q4q4q4q4q4uQ4q4q4q4q4q4q4q4q4q4q4q4q4q4q', 'Admin', 'Sistema', 'gerente');
```

### **Características de Seguridad**
- **Salt automático**: Cada hash es único incluso para contraseñas idénticas
- **12 rounds**: Balance óptimo entre seguridad y rendimiento
- **Resistente a ataques**: Protección contra fuerza bruta y rainbow tables
- **Verificación segura**: Comparación timing-attack resistant

### **Casos de Uso**
- 🔐 **Configuración inicial**: Generar hashes para usuarios predeterminados
- 🔄 **Reset de contraseñas**: Crear nuevas contraseñas encriptadas
- 🧪 **Testing**: Verificar que el sistema de encriptación funciona
- 📚 **Educación**: Demostrar cómo funciona bcrypt

---

## 3. `test_diagnostico.py` - Suite Completa de Pruebas

### **Propósito**
Sistema de diagnóstico comprehensivo que prueba cada capa de la aplicación de forma independiente y combinada.

### **Módulos de Prueba**

```python
def test_conexion():
    """
    Prueba la conexión a la base de datos
    Verifica:
    - Instanciación de la clase Conex
    - Establecimiento de conexión MySQL
    - Disponibilidad de la base de datos
    """
    try:
        from conex.conn import Conex
        conex = Conex()
        if conex.getConex():
            print("✅ Conexión a BD: OK")
            return True
        else:
            print("❌ Conexión a BD: FALLÓ")
            return False
    except Exception as e:
        print(f"❌ Error en conexión: {e}")
        return False
```

```python
def test_tablas():
    """
    Verifica la estructura de la base de datos
    Comprueba:
    - Existencia de tablas necesarias
    - Integridad de los datos de prueba
    - Formato correcto de contraseñas encriptadas
    """
    try:
        from conex.conn import Conex
        conex = Conex()
        conn = conex.getConex()
        cursor = conn.cursor()
        
        # Verificar tabla empleado
        cursor.execute("SELECT COUNT(*) as count FROM empleado")
        resultado = cursor.fetchone()
        print(f"✅ Tabla empleado: {resultado['count']} registros")
        
        # Verificar datos de empleado
        cursor.execute("SELECT run, nombre, apellido, cargo, LENGTH(password) as pass_len FROM empleado")
        empleados = cursor.fetchall()
        for emp in empleados:
            print(f"   👤 {emp['run']}: {emp['nombre']} {emp['apellido']} - {emp['cargo']} (pass: {emp['pass_len']} chars)")
        
        cursor.close()
        return True
    except Exception as e:
        print(f"❌ Error en tablas: {e}")
        return False
```

```python
def test_login():
    """
    Prueba integral del sistema de autenticación
    Valida:
    - Proceso completo de login
    - Verificación de credenciales
    - Creación de objetos User
    - Mensajes de error apropiados
    """
    try:
        from dto.dto_user import UserDTO
        dto = UserDTO()
        
        print("\n🔐 Probando login...")
        resultado = dto.validarLogin('12345678-9', 'admin123')
        
        if resultado:
            print(f"✅ Login exitoso!")
            print(f"   Usuario: {resultado.getNombre()} {resultado.getApellido()}")
            print(f"   Cargo: {resultado.getCargo()}")
            return True
        else:
            print("❌ Login fallido")
            return False
    except Exception as e:
        print(f"❌ Error en login: {e}")
        return False
```

### **Ejecución Completa**
```bash
python test_diagnostico.py

# Salida de ejemplo:
🔍 INICIANDO DIAGNÓSTICO COMPLETO
==================================================
✅ Conexión a MySQL establecida correctamente
✅ Base de datos: viaja_seguro
✅ Conexión a BD: OK
✅ Conexión a MySQL establecida correctamente
✅ Base de datos: viaja_seguro
✅ Tabla empleado: 2 registros
   👤 12345678-9: Admin Sistema - gerente (pass: 60 chars)
   👤 98765432-1: Juan Pérez - empleado (pass: 60 chars)

🔐 Probando login...
🔍 Intentando login para RUN: 12345678-9
✅ Conexión a MySQL establecida correctamente
✅ Usuario encontrado: Admin Sistema
🔍 Hash encontrado en BD: $2b$12$KcCwvJQ4qQ4q4q4q4...
🔍 Verificando contraseña...
✅ Contraseña correcta para Admin Sistema
✅ Login exitoso!
   Usuario: Admin Sistema
   Cargo: gerente
==================================================
🎉 TODAS LAS PRUEBAS PASARON! El sistema está listo.
```

### **Ventajas del Diagnóstico**
- **Pruebas modulares**: Cada componente se prueba individualmente
- **Información detallada**: Mensajes claros sobre lo que se está probando
- **Tolerancia a fallos**: Continúa ejecutándose incluso si una prueba falla
- **Debugging fácil**: Identifica exactamente dónde están los problemas

---

## 4. `test_imports.py` - Validador de Dependencias

### **Propósito**
Verifica que todas las importaciones entre módulos funcionen correctamente, detectando problemas de estructura de paquetes y dependencias circulares.

### **Código Principal**

```python
import sys
import os

# Agregar el directorio actual al path para importaciones relativas
sys.path.append(os.path.dirname(__file__))

try:
    from modelo.user import User
    print("✅ User importado correctamente")
    
    from dao.dao_user import daoUser
    print("✅ daoUser importado correctamente")
    
    from dto.dto_user import UserDTO
    print("✅ UserDTO importado correctamente")
    
    from conex.conn import Conex
    print("✅ Conex importado correctamente")
    
    print("🎉 Todas las importaciones funcionan!")
    
except ImportError as e:
    print(f"❌ Error de importación: {e}")
except Exception as e:
    print(f"❌ Otro error: {e}")
```

### **Qué Verifica**
- ✅ **Estructura de paquetes**: Que los `__init__.py` estén presentes
- ✅ **Importaciones relativas**: Que los módulos se puedan importar entre sí
- ✅ **Dependencias circulares**: Que no haya importaciones circulares
- ✅ **Nombres de clases**: Que los nombres coincidan exactamente
- ✅ **Jerarquía de archivos**: Que la estructura de directorios sea correcta

### **Ejecución y Salida**
```bash
python test_imports.py

# Salida exitosa:
✅ User importado correctamente
✅ daoUser importado correctamente
✅ UserDTO importado correctamente
✅ Conex importado correctamente
🎉 Todas las importaciones funcionan!

# Salida con error:
❌ Error de importación: cannot import name 'User' from 'modelo.user'
```

### **Problemas Comunes que Detecta**

1. **Archivos faltantes**:
   ```
   ❌ Error de importación: No module named 'modelo.user'
   ```

2. **Clases mal nombradas**:
   ```
   ❌ Error de importación: cannot import name 'User' from 'modelo.user'
   ```

3. **Problemas de path**:
   ```
   ❌ Error de importación: attempted relative import with no known parent package
   ```

4. **Dependencias circulares**:
   ```
   ❌ Error de importación: cannot import name 'X' from partially initialized module 'Y'
   ```

---

## 🛠️ Flujo de Trabajo Recomendado

### Para Nuevos Desarrolladores
1. **Ejecutar `test_imports.py`** - Verificar que el entorno está configurado correctamente
2. **Ejecutar `test_diagnostico.py`** - Validar que todos los componentes funcionan
3. **Usar `generar_password.py`** si es necesario crear nuevos usuarios
4. **Ejecutar `diagnostico_final.py`** antes de cualquier despliegue

### Para Solución de Problemas
1. **Ejecutar `test_imports.py`** - Identificar problemas de estructura
2. **Revisar errores específicos** con los mensajes detallados
3. **Usar `generar_password.py`** para regenerar contraseñas si es necesario
4. **Ejecutar `test_diagnostico.py`** para diagnóstico completo

### Para Mantenimiento
1. **Ejecutar diagnósticos regularmente** después de actualizaciones
2. **Usar `generar_password.py`** para rotar contraseñas
3. **Mantener los scripts actualizados** con nuevos módulos

## 📊 Resumen de Archivos de Utilidad

| Archivo | Propósito | Cuándo Usarlo |
|---------|-----------|---------------|
| `test_imports.py` | Verificar importaciones | Al clonar el proyecto o agregar nuevos módulos |
| `test_diagnostico.py` | Pruebas completas del sistema | Después de cambios importantes o para debug |
| `diagnostico_final.py` | Verificación pre-producción | Antes de desplegar a producción |
| `generar_password.py` | Generación de contraseñas | Al crear nuevos usuarios o resetear contraseñas |

Estos archivos son esenciales para mantener la salud del proyecto y facilitar el desarrollo colaborativo. Proporcionan verificación automática de que el sistema funciona correctamente y herramientas para resolver problemas comunes.

---

## 👨‍💻 Autor

**Viaja Seguro Rent a Car - Sistema de Gestión**  
Proyecto académico desarrollado por estudiantes de la asignatura  
*Programación Orientada a Objeto Seguro (TI3021)*.  

> 🚀 Implementación orientada a objetos, conexión segura MySQL, y patrón MVC en Python.

---
