# Changelog

## [Unreleased]

### Added - 2025-11-19

#### 🛡️ Seguridad Avanzada
- **Nueva función `validar_entrada_sql()`** en `validador_formatos.py`
  - Detección de palabras clave SQL: SELECT, INSERT, UPDATE, DELETE, DROP, UNION, EXEC
  - Prevención de comentarios SQL: --, #, /* */
  - Rechazo de patrones maliciosos: OR 1=1, AND 1=1, WAITFOR, DELAY
  - Respeto de límites de longitud (máximo 255 caracteres)
  - Logging automático de intentos sospechosos

- **Nueva función `validar_password_segura()`** en `validador_formatos.py`
  - Requisito de mínimo 8 caracteres
  - Al menos una mayúscula, una minúscula, un dígito y un carácter especial
  - Retorna tupla (bool, mensaje) con detalles del error
  - Integrada en creación y actualización de empleados

- **Nueva función `sanitizar_texto()`** en `validador_formatos.py`
  - Remueve caracteres potencialmente peligrosos: ; \ ' " - # *
  - Útil para preparar datos antes de registrarlos

- **Nueva función `cifrar_datos_sensibles()`** en `validador_formatos.py`
  - Wrapper para cifrado de datos sensibles
  - Usa `utils.encoder.Encoder` si está disponible

#### 📋 Integración de Seguridad en Controlador
- `controlador/validations.py` - Integración de validaciones:
  - Línea ~131: Reemplazo de `validar_password()` con `validar_password_segura()` en sección "Agregar Empleado"
  - Línea ~146: Agregado `validar_entrada_sql()` en todos los campos antes de `agregarUsuario()`
  - Línea ~208: Reemplazo de `validar_password()` con `validar_password_segura()` en sección "Actualizar Empleado"
  - Línea ~341: Agregado `validar_entrada_sql()` en todos los campos antes de `agregarCliente()`

#### ✅ Suite Completa de Pruebas
- **Nuevo archivo `test_security_functions.py`**
  - 18 pruebas unitarias cobriendo todas las funciones de seguridad
  - Clase TestValidarEntradaSQL (7 pruebas): validación, palabras clave, comentarios, patrones, longitud, entrada vacía
  - Clase TestValidarPasswordSegura (6 pruebas): contraseña válida, longitud, mayúscula, minúscula, dígito, carácter especial
  - Clase TestSanitizarTexto (5 pruebas): caracteres peligrosos, caracteres seguros, backslash, hash, entrada vacía
  - Clase TestIntegration (1 prueba): flujo completo de detección de entrada maliciosa
  - **Resultado**: 18/18 pruebas pasadas ✅

#### 📝 Cambios de Presentación
- Reemplazados emojis con mensajes de texto para mejor compatibilidad cross-platform
- Formato: `[OK]`, `[ERROR]`, `[TEST]` en lugar de ✅, ❌, 🧪
- Mejora de compatibilidad en consolas Windows y sistemas legacy

#### 📖 Documentación
- **Nuevo archivo `SECURITY_INTEGRATION_SUMMARY.md`**
  - Resumen completo de cambios de seguridad
  - Ejemplos de uso y casos de prueba
  - Impacto en la aplicación y próximos pasos

### Changed - 2025-11-19

#### Refactorización de Validaciones
- Todos los mensajes de validación actualizados a formato de texto plano
- Mejorada compatibilidad en diferentes sistemas operativos
- Logging consistente de intentos de seguridad

### Comportamiento de Seguridad

#### Entrada Sospechosa
- Log: `WARNING:root:Entrada sospechosa para SQL detectada: [texto]`
- UI: `[ERROR] Datos sospechosos detectados. Operación cancelada.`
- Acción: Cancela operación sin insertar datos

#### Contraseña Débil
- Log: `DEBUG:root:Contraseña inválida: [razón específica]`
- UI: `[ERROR] [Requisito fallido]` (p.ej., "Debe contener al menos 8 caracteres")
- Acción: Solicita nueva contraseña

#### Entrada Válida
- Log: `INFO:root:Empleado/Cliente agregado exitosamente...`
- UI: `[OK] Empleado/Cliente agregado correctamente`
- Acción: Procede normalmente

### Puntos de Aplicación Actual

1. **Agregar Empleado**
   - Validación de contraseña fuerte (obligatoria)
   - Validación SQL en: run, nombre, apellido, cargo
   - Logging de intentos fallidos

2. **Actualizar Empleado**
   - Validación de contraseña fuerte (si cambia)

3. **Agregar Cliente**
   - Validación SQL en: run, nombre, apellido, dirección
   - Logging de intentos fallidos

### Próximos Pasos Recomendados

#### Corto Plazo
- Extender `validar_entrada_sql()` a:
  - Entrada de vehículos (patente, marca, modelo)
  - Entrada de arriendos (fecha, observaciones)
  - Búsquedas y filtros

#### Mediano Plazo
- Implementar rate limiting para fallos de contraseña
- Agregar auditoría detallada de intentos de seguridad
- Crear panel de administración para visualizar logs

#### Largo Plazo
- Implementar 2FA (autenticación de dos factores)
- Integrar OWASP Security Guidelines
- Realizar auditoría de seguridad profesional

---

## [Previous Versions]

### 2025-11-19 (Previous Release)
- Soporte ES3 UF en arriendos
- Optimización de base de datos (JOIN queries)
- Refactorización de DAO/DTO
- Mejora de rendimiento (eliminación de N+1 queries)

### Initial Release
- Arquitectura MVC con Python
- Autenticación de usuarios con bcrypt
- Gestión de empleados, clientes, vehículos y arriendos
- Interfaz CLI
- Base de datos MySQL
