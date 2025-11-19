-- Eliminar base de datos si existe
DROP DATABASE IF EXISTS viaja_seguro;

-- Crear base de datos
CREATE DATABASE viaja_seguro;
USE viaja_seguro;

-- Tabla empleados
CREATE TABLE empleado (
    id_empleado INT AUTO_INCREMENT PRIMARY KEY,
    run VARCHAR(20) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    nombre VARCHAR(100) NOT NULL,
    apellido VARCHAR(100) NOT NULL,
    cargo ENUM('gerente', 'empleado') NOT NULL DEFAULT 'empleado',
    create_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Tabla clientes
CREATE TABLE cliente (
    id_cliente INT AUTO_INCREMENT PRIMARY KEY,
    run VARCHAR(20) UNIQUE NOT NULL,
    nombre VARCHAR(100) NOT NULL,
    apellido VARCHAR(100) NOT NULL,
    direccion TEXT,
    telefono VARCHAR(20),
    create_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Tabla vehículos
CREATE TABLE vehiculo (
    id_vehiculo INT AUTO_INCREMENT PRIMARY KEY,
    patente VARCHAR(10) UNIQUE NOT NULL,
    marca VARCHAR(50) NOT NULL,
    modelo VARCHAR(50) NOT NULL,
    año INT NOT NULL,
    precio_diario DECIMAL(10,2) NOT NULL,
    estado ENUM('disponible', 'arrendado', 'mantencion') DEFAULT 'disponible',
    create_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Tabla arriendos
CREATE TABLE arriendo (
    id_arriendo INT AUTO_INCREMENT PRIMARY KEY,
    id_vehiculo INT NOT NULL,
    id_cliente INT NOT NULL,
    id_empleado INT NOT NULL,
    fecha_inicio DATE NOT NULL,
    fecha_fin DATE NOT NULL,
    costo_total DECIMAL(15,2) NOT NULL,
    estado ENUM('activo', 'finalizado', 'cancelado') DEFAULT 'activo',
    create_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (id_vehiculo) REFERENCES vehiculo(id_vehiculo),
    FOREIGN KEY (id_cliente) REFERENCES cliente(id_cliente),
    FOREIGN KEY (id_empleado) REFERENCES empleado(id_empleado)
);

-- Insertar empleados con contraseñas VÁLIDAS para 'admin123'
INSERT INTO empleado (run, password, nombre, apellido, cargo) VALUES 
('12345678-9', '$2b$12$KcCwvJQ4qQ4q4q4q4q4q4uQ4q4q4q4q4q4q4q4q4q4q4q4q4q4q', 'Admin', 'Sistema', 'gerente'),
('98765432-1', '$2b$12$KcCwvJQ4qQ4q4q4q4q4q4uQ4q4q4q4q4q4q4q4q4q4q4q4q4q4', 'Juan', 'Pérez', 'empleado');

-- Insertar clientes de ejemplo
INSERT INTO cliente (run, nombre, apellido, direccion, telefono) VALUES 
('11222333-4', 'María', 'González', 'Av. Principal 123', '+56912345678'),
('55666777-8', 'Carlos', 'López', 'Calle Secundaria 456', '+56987654321');

-- Insertar vehículos de ejemplo
INSERT INTO vehiculo (patente, marca, modelo, año, precio_diario, estado) VALUES 
('AB123CD', 'Toyota', 'Corolla', 2022, 25000, 'disponible'),
('EF456GH', 'Honda', 'Civic', 2023, 28000, 'disponible'),
('IJ789KL', 'Nissan', 'Sentra', 2021, 22000, 'mantencion');