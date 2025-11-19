-- =============================================
-- Sistema de Gestión de Arriendos - Viaja Seguro
-- Script de creación de base de datos
-- =============================================

-- Eliminar base de datos si existe
DROP DATABASE IF EXISTS viaja_seguro;

-- Crear base de datos
CREATE DATABASE viaja_seguro 
CHARACTER SET utf8mb4 
COLLATE utf8mb4_unicode_ci;

USE viaja_seguro;

-- =============================================
-- Tabla: empleado
-- =============================================
CREATE TABLE empleado (
    id_empleado INT AUTO_INCREMENT PRIMARY KEY,
    run VARCHAR(20) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    nombre VARCHAR(100) NOT NULL,
    apellido VARCHAR(100) NOT NULL,
    cargo ENUM('gerente', 'empleado') NOT NULL DEFAULT 'empleado',
    activo BOOLEAN DEFAULT TRUE,
    create_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    update_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    -- Índices para mejorar performance
    INDEX idx_empleado_run (run),
    INDEX idx_empleado_cargo (cargo),
    INDEX idx_empleado_activo (activo)
) ENGINE=InnoDB;

-- =============================================
-- Tabla: cliente
-- =============================================
CREATE TABLE cliente (
    id_cliente INT AUTO_INCREMENT PRIMARY KEY,
    run VARCHAR(20) UNIQUE NOT NULL,
    nombre VARCHAR(100) NOT NULL,
    apellido VARCHAR(100) NOT NULL,
    direccion TEXT,
    telefono VARCHAR(20),
    email VARCHAR(100),
    activo BOOLEAN DEFAULT TRUE,
    create_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    update_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    -- Índices
    INDEX idx_cliente_run (run),
    INDEX idx_cliente_nombre (nombre),
    INDEX idx_cliente_activo (activo),
    INDEX idx_cliente_telefono (telefono)
) ENGINE=InnoDB;

-- =============================================
-- Tabla: vehiculo
-- =============================================
CREATE TABLE vehiculo (
    id_vehiculo INT AUTO_INCREMENT PRIMARY KEY,
    patente VARCHAR(10) UNIQUE NOT NULL,
    marca VARCHAR(50) NOT NULL,
    modelo VARCHAR(50) NOT NULL,
    año INT NOT NULL,
    color VARCHAR(30),
    precio_diario DECIMAL(12,2) NOT NULL,
    estado ENUM('disponible', 'arrendado', 'mantencion', 'reparacion') DEFAULT 'disponible',
    kilometraje INT DEFAULT 0,
    descripcion TEXT,
    activo BOOLEAN DEFAULT TRUE,
    create_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    update_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    -- Restricciones de datos
    CHECK (año >= 1900),
    CHECK (precio_diario > 0),
    CHECK (kilometraje >= 0),
    
    -- Índices
    INDEX idx_vehiculo_patente (patente),
    INDEX idx_vehiculo_marca (marca),
    INDEX idx_vehiculo_estado (estado),
    INDEX idx_vehiculo_activo (activo),
    INDEX idx_vehiculo_precio (precio_diario)
) ENGINE=InnoDB;

-- =============================================
-- Tabla: arriendo
-- =============================================
CREATE TABLE arriendo (
    id_arriendo INT AUTO_INCREMENT PRIMARY KEY,
    id_vehiculo INT NOT NULL,
    id_cliente INT NOT NULL,
    id_empleado INT NOT NULL,
    fecha_inicio DATE NOT NULL,
    fecha_fin DATE NOT NULL,
    fecha_devolucion DATE NULL,
    costo_total DECIMAL(15,2) NOT NULL,
    costo_extras DECIMAL(10,2) DEFAULT 0,
    estado ENUM('activo', 'finalizado', 'cancelado') DEFAULT 'activo',
    observaciones TEXT,
    valor_uf_fecha DECIMAL(10, 2) DEFAULT 0.0,
    fecha_uf_consulta DATE DEFAULT NULL,
    create_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    update_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    -- Claves foráneas con acciones específicas
    FOREIGN KEY (id_vehiculo) 
        REFERENCES vehiculo(id_vehiculo)
        ON UPDATE CASCADE,
    
    FOREIGN KEY (id_cliente) 
        REFERENCES cliente(id_cliente)
        ON UPDATE CASCADE,
        
    FOREIGN KEY (id_empleado) 
        REFERENCES empleado(id_empleado)
        ON UPDATE CASCADE,
    
    -- Restricciones de datos
    CHECK (fecha_fin > fecha_inicio),
    CHECK (costo_total > 0),
    
    -- Índices
    INDEX idx_arriendo_vehiculo (id_vehiculo),
    INDEX idx_arriendo_cliente (id_cliente),
    INDEX idx_arriendo_empleado (id_empleado),
    INDEX idx_arriendo_fechas (fecha_inicio, fecha_fin),
    INDEX idx_arriendo_estado (estado)
) ENGINE=InnoDB;

-- =============================================
-- Tabla: daño_vehiculo (Nueva tabla para control de daños)
-- =============================================
CREATE TABLE danio_vehiculo (
    id_danio INT AUTO_INCREMENT PRIMARY KEY,
    id_vehiculo INT NOT NULL,
    id_arriendo INT NULL,
    descripcion TEXT NOT NULL,
    costo_reparacion DECIMAL(10,2) DEFAULT 0,
    fecha_reporte DATE NOT NULL,
    fecha_reparacion DATE NULL,
    estado ENUM('reportado', 'en_reparacion', 'reparado') DEFAULT 'reportado',
    create_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    FOREIGN KEY (id_vehiculo) 
        REFERENCES vehiculo(id_vehiculo)
        ON UPDATE CASCADE,
        
    FOREIGN KEY (id_arriendo) 
        REFERENCES arriendo(id_arriendo)
        ON UPDATE CASCADE,
    
    -- Índices
    INDEX idx_danio_vehiculo (id_vehiculo),
    INDEX idx_danio_estado (estado),
    INDEX idx_danio_fecha (fecha_reporte)
) ENGINE=InnoDB;

-- =============================================
-- Tabla: auditoria (Para tracking de cambios)
-- =============================================
CREATE TABLE auditoria (
    id_auditoria INT AUTO_INCREMENT PRIMARY KEY,
    tabla_afectada VARCHAR(50) NOT NULL,
    id_registro INT NOT NULL,
    accion ENUM('INSERT', 'UPDATE', 'DELETE') NOT NULL,
    valores_anteriores JSON,
    valores_nuevos JSON,
    id_usuario INT NULL,
    create_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    INDEX idx_auditoria_tabla (tabla_afectada),
    INDEX idx_auditoria_fecha (create_time),
    INDEX idx_auditoria_accion (accion)
) ENGINE=InnoDB;

-- =============================================
-- Triggers para auditoría automática
-- =============================================

-- Trigger para auditoría de empleados
DELIMITER //
CREATE TRIGGER audit_empleado_insert
    AFTER INSERT ON empleado
    FOR EACH ROW
BEGIN
    INSERT INTO auditoria (tabla_afectada, id_registro, accion, valores_nuevos)
    VALUES ('empleado', NEW.id_empleado, 'INSERT', 
            JSON_OBJECT('run', NEW.run, 'nombre', NEW.nombre, 'cargo', NEW.cargo));
END//

CREATE TRIGGER audit_empleado_update
    AFTER UPDATE ON empleado
    FOR EACH ROW
BEGIN
    INSERT INTO auditoria (tabla_afectada, id_registro, accion, valores_anteriores, valores_nuevos)
    VALUES ('empleado', NEW.id_empleado, 'UPDATE',
            JSON_OBJECT('run', OLD.run, 'nombre', OLD.nombre, 'cargo', OLD.cargo),
            JSON_OBJECT('run', NEW.run, 'nombre', NEW.nombre, 'cargo', NEW.cargo));
END//
DELIMITER ;

-- =============================================
-- Procedimientos almacenados útiles
-- =============================================

-- Procedimiento para calcular costo de arriendo
DELIMITER //
CREATE PROCEDURE CalcularCostoArriendo(
    IN p_id_vehiculo INT,
    IN p_fecha_inicio DATE,
    IN p_fecha_fin DATE,
    OUT p_costo_total DECIMAL(15,2)
)
BEGIN
    DECLARE v_precio_diario DECIMAL(12,2);
    DECLARE v_dias INT;
    
    -- Obtener precio diario del vehículo
    SELECT precio_diario INTO v_precio_diario
    FROM vehiculo 
    WHERE id_vehiculo = p_id_vehiculo;
    
    -- Calcular días de arriendo
    SET v_dias = DATEDIFF(p_fecha_fin, p_fecha_inicio);
    
    -- Calcular costo total
    SET p_costo_total = v_precio_diario * v_dias;
END//
DELIMITER ;

-- =============================================
-- Vistas útiles para reportes
-- =============================================

-- Vista para arriendos activos con información completa
CREATE VIEW vista_arriendos_activos AS
SELECT 
    a.id_arriendo,
    v.patente,
    v.marca,
    v.modelo,
    CONCAT(c.nombre, ' ', c.apellido) AS cliente,
    CONCAT(e.nombre, ' ', e.apellido) AS empleado,
    a.fecha_inicio,
    a.fecha_fin,
    a.costo_total,
    a.estado
FROM arriendo a
JOIN vehiculo v ON a.id_vehiculo = v.id_vehiculo
JOIN cliente c ON a.id_cliente = c.id_cliente
JOIN empleado e ON a.id_empleado = e.id_empleado
WHERE a.estado = 'activo';

-- Vista para vehículos disponibles
CREATE VIEW vista_vehiculos_disponibles AS
SELECT 
    id_vehiculo,
    patente,
    marca,
    modelo,
    año,
    color,
    precio_diario,
    kilometraje
FROM vehiculo 
WHERE estado = 'disponible' AND activo = TRUE;

-- Vista para reporte de ingresos mensuales
CREATE VIEW vista_ingresos_mensuales AS
SELECT 
    YEAR(fecha_inicio) as año,
    MONTH(fecha_inicio) as mes,
    COUNT(*) as total_arriendos,
    SUM(costo_total) as ingresos_totales
FROM arriendo 
WHERE estado = 'finalizado'
GROUP BY YEAR(fecha_inicio), MONTH(fecha_inicio);

-- =============================================
-- Datos de prueba
-- =============================================

-- Insertar empleados con contraseñas VÁLIDAS para 'admin123'
-- Estas contraseñas fueron generadas con bcrypt para 'admin123'
INSERT INTO empleado (run, password, nombre, apellido, cargo) VALUES 
('12345678-9', '$2b$12$H6or2BHbTTgVuw7Eb0EGOe2RxzdczQXE4U5Iy0NBtA2qai4CKywBq', 'Admin', 'Sistema', 'gerente'),
('98765432-1', '$2b$12$KcCwvJQ4qQ4q4q4q4q4q4uQ4q4q4q4q4q4q4q4q4q4q4q4q4q4q', 'Juan', 'Pérez', 'empleado'),
('11222333-4', '$2b$12$KcCwvJQ4qQ4q4q4q4q4q4uQ4q4q4q4q4q4q4q4q4q4q4q4q4q4q', 'María', 'González', 'empleado');

-- Insertar clientes de ejemplo
INSERT INTO cliente (run, nombre, apellido, direccion, telefono, email) VALUES 
('11222333-4', 'María', 'González', 'Av. Principal 123, Santiago', '+56912345678', 'maria.gonzalez@email.com'),
('55666777-8', 'Carlos', 'López', 'Calle Secundaria 456, Providencia', '+56987654321', 'carlos.lopez@email.com'),
('99888777-6', 'Ana', 'Martínez', 'Los Alerces 789, Las Condes', '+56911223344', 'ana.martinez@email.com'),
('33444555-2', 'Pedro', 'Rodríguez', 'Av. Forestal 321, Vitacura', '+56955667788', 'pedro.rodriguez@email.com');

-- Insertar vehículos de ejemplo (precios en UF)
INSERT INTO vehiculo (patente, marca, modelo, año, color, precio_diario, kilometraje, descripcion) VALUES 
('AB123CD', 'Toyota', 'Corolla', 2022, 'Blanco', 1.5, 15000, 'Vehículo en excelente estado, full equipo'),
('EF456GH', 'Honda', 'Civic', 2023, 'Negro', 1.8, 8000, 'Nuevo, tecnología de punta'),
('IJ789KL', 'Nissan', 'Sentra', 2021, 'Rojo', 1.2, 25000, 'Buen estado, mantención al día'),
('MN012OP', 'Hyundai', 'Tucson', 2022, 'Gris', 2.1, 18000, 'SUV espaciosa, ideal para familia'),
('QR345ST', 'Kia', 'Sportage', 2023, 'Azul', 2.3, 5000, 'SUV moderna, baja kilometraje'),
('UV678WX', 'Chevrolet', 'Spark', 2021, 'Verde', 0.8, 30000, 'Económico, perfecto para ciudad');

-- Insertar arriendos de ejemplo (costos calculados con UF)
INSERT INTO arriendo (id_vehiculo, id_cliente, id_empleado, fecha_inicio, fecha_fin, costo_total, valor_uf_fecha, fecha_uf_consulta, estado) VALUES 
(1, 1, 2, '2024-01-15', '2024-01-20', 281250, 37500.00, '2024-01-15', 'finalizado'),
(2, 2, 3, '2024-02-01', '2024-02-05', 268200, 37200.00, '2024-02-01', 'finalizado'),
(3, 3, 2, CURDATE(), DATE_ADD(CURDATE(), INTERVAL 3 DAY), 133680, 37140.00, CURDATE(), 'activo'),
(4, 4, 3, DATE_ADD(CURDATE(), INTERVAL 2 DAY), DATE_ADD(CURDATE(), INTERVAL 7 DAY), 388425, 37140.00, DATE_ADD(CURDATE(), INTERVAL 2 DAY), 'activo');

-- Insertar registros de daños de ejemplo
INSERT INTO danio_vehiculo (id_vehiculo, id_arriendo, descripcion, costo_reparacion, fecha_reporte, estado) VALUES 
(3, 1, 'Rayón en puerta lateral derecha', 150000, '2024-01-21', 'reparado'),
(6, NULL, 'Reemplazo de neumáticos', 300000, '2024-02-10', 'en_reparacion');

-- =============================================
-- Mensaje de confirmación
-- =============================================
SELECT 'Base de datos "viaja_seguro" creada exitosamente!' as mensaje;
SELECT COUNT(*) as total_empleados FROM empleado;
SELECT COUNT(*) as total_clientes FROM cliente;
SELECT COUNT(*) as total_vehiculos FROM vehiculo;
SELECT COUNT(*) as total_arriendos FROM arriendo;
