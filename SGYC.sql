-- ====================================
-- 1. ROLES, USUARIOS Y PERMISOS
-- ====================================

CREATE TABLE roles (
    id_rol SERIAL PRIMARY KEY,
    nombre VARCHAR(50) NOT NULL UNIQUE,
    descripcion TEXT
);

CREATE TABLE permisos (
    id_permiso SERIAL PRIMARY KEY,
    nombre VARCHAR(50) NOT NULL UNIQUE,
    descripcion TEXT
);

CREATE TABLE roles_permisos (
    id_rol INTEGER REFERENCES roles(id_rol) ON DELETE CASCADE,
    id_permiso INTEGER REFERENCES permisos(id_permiso) ON DELETE CASCADE,
    PRIMARY KEY (id_rol, id_permiso)
);

-- ====================================
-- 2. LÍNEAS DE PRODUCCIÓN
-- ====================================

CREATE TABLE lineas (
    id_linea SERIAL PRIMARY KEY,
    nombre VARCHAR(50) NOT NULL UNIQUE,
    descripcion TEXT
);

-- Insertar líneas principales
INSERT INTO lineas (nombre, descripcion) VALUES
('MOTOS', 'Línea de producción de motocicletas'),
('SOFASA', 'Línea de producción de vehículos Sofasa');

-- ====================================
-- 3. USUARIOS
-- ====================================

CREATE TABLE usuarios (
    id_usuario SERIAL PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    contraseña TEXT NOT NULL,
    rol_id INTEGER REFERENCES roles(id_rol) ON DELETE SET NULL,
    linea_id INTEGER REFERENCES lineas(id_linea) ON DELETE SET NULL
);

-- Usuario administrador inicial
INSERT INTO usuarios (nombre, email, contraseña)
VALUES ('Administrador Principal', 'admin@inventario.com', 'admin123');

-- ====================================
-- 4. MATERIALES Y GESTIÓN
-- ====================================

CREATE TABLE materiales (
    id_material SERIAL PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    referencia VARCHAR(50) UNIQUE NOT NULL,
    descripcion TEXT,
    apertura VARCHAR(10) CHECK (apertura IN ('abierto', 'cerrado')),
    diametro DECIMAL(10,2),
    longitud DECIMAL(10,2),
    creado_por INTEGER REFERENCES usuarios(id_usuario) ON DELETE SET NULL,
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    linea_id INTEGER REFERENCES lineas(id_linea) ON DELETE SET NULL
);

-- ====================================
-- 5. TINAS
-- ====================================

CREATE TABLE tinas (
    id_tina SERIAL PRIMARY KEY,
    tipo VARCHAR(20) CHECK (tipo IN ('pequeña', 'grande')),
    estado VARCHAR(20) CHECK (estado IN ('llena', 'vacía')),
    fecha DATE NOT NULL,
    material_id INTEGER REFERENCES materiales(id_material) ON DELETE SET NULL,
    operario_id INTEGER REFERENCES usuarios(id_usuario) ON DELETE SET NULL
);

-- ====================================
-- 6. ROLLOS
-- ====================================

CREATE TABLE rollos (
    id_rollo SERIAL PRIMARY KEY,
    descripcion TEXT,
    cantidad DECIMAL(10,2),
    fecha_uso DATE NOT NULL,
    fecha_entrega DATE NOT NULL,
    material_id INTEGER REFERENCES materiales(id_material) ON DELETE SET NULL,
    cortador_id INTEGER REFERENCES usuarios(id_usuario) ON DELETE SET NULL
);

-- ====================================
-- 7. TARJETAS (Producción / Kaban)
-- ====================================

CREATE TABLE tarjetas (
    id_tarjeta SERIAL PRIMARY KEY,
    tipo VARCHAR(20) CHECK (tipo IN ('produccion', 'kaban')),
    estado VARCHAR(50),
    descripcion TEXT,
    fecha DATE NOT NULL,
    material_id INTEGER REFERENCES materiales(id_material) ON DELETE SET NULL,
    tina_id INTEGER REFERENCES tinas(id_tina) ON DELETE SET NULL,
    rollo_id INTEGER REFERENCES rollos(id_rollo) ON DELETE SET NULL,
    usuario_id INTEGER REFERENCES usuarios(id_usuario) ON DELETE SET NULL
);

-- ====================================
-- 8. VERIFICACIONES
-- ====================================

CREATE TABLE verificaciones (
    id_verificacion SERIAL PRIMARY KEY,
    tipo VARCHAR(20) CHECK (tipo IN ('cortador', 'calidad')),
    descripcion TEXT,
    fecha DATE NOT NULL,
    usuario_id INTEGER REFERENCES usuarios(id_usuario) ON DELETE SET NULL,
    material_id INTEGER REFERENCES materiales(id_material) ON DELETE SET NULL,
    tina_id INTEGER REFERENCES tinas(id_tina) ON DELETE SET NULL
);

-- ====================================
-- 9. REGISTROS DE CORTE
-- ====================================

CREATE TABLE registros_corte (
    id_registro SERIAL PRIMARY KEY,
    fecha DATE NOT NULL,
    descripcion TEXT,
    cortador_id INTEGER REFERENCES usuarios(id_usuario) ON DELETE SET NULL,
    material_id INTEGER REFERENCES materiales(id_material) ON DELETE SET NULL,
    UNIQUE (fecha, cortador_id, material_id)
);

-- ====================================
-- 10. REPORTES DE CALIDAD
-- ====================================

CREATE TABLE reportes_calidad (
    id_reporte SERIAL PRIMARY KEY,
    fecha DATE NOT NULL,
    descripcion TEXT NOT NULL,
    tipo_objetado VARCHAR(30),
    id_objeto INTEGER,
    calidad_id INTEGER REFERENCES usuarios(id_usuario) ON DELETE SET NULL
);

-- ====================================
-- 11. PERMISOS Y ASIGNACIÓN DE ROLES
-- ====================================

INSERT INTO permisos (nombre, descripcion) VALUES
('crear_usuario', 'Puede crear nuevos usuarios'),
('editar_usuario', 'Puede editar usuarios'),
('ver_usuarios', 'Visualizar usuarios'),
('registrar_material', 'Registrar materiales'),
('ver_materiales', 'Visualizar materiales'),
('registrar_tina', 'Registrar tinas'),
('ver_tinas', 'Visualizar tinas'),
('registrar_rollo', 'Registrar rollos'),
('ver_rollos', 'Visualizar rollos'),
('registrar_tarjeta', 'Registrar tarjetas'),
('ver_tarjetas', 'Visualizar tarjetas'),
('registrar_verificacion', 'Registrar verificación'),
('ver_verificaciones', 'Visualizar verificaciones'),
('registrar_corte', 'Registrar corte'),
('ver_registros_corte', 'Visualizar registros de corte'),
('registrar_reporte_calidad', 'Registrar reporte de calidad');

INSERT INTO roles (nombre, descripcion) VALUES
('Administrador', 'Acceso completo'),
('Jefe', 'Solo visualización'),
('Calidad', 'Registro de verificación y defectos'),
('Cortador', 'Registro de rollos, cortes y tarjetas');

-- Permisos por rol
INSERT INTO roles_permisos (id_rol, id_permiso)
SELECT 1, id_permiso FROM permisos;

INSERT INTO roles_permisos (id_rol, id_permiso)
SELECT 2, id_permiso FROM permisos WHERE nombre LIKE 'ver_%';

INSERT INTO roles_permisos (id_rol, id_permiso) VALUES
(3, 6), (3, 7), (3, 12), (3, 13), (3, 16);

INSERT INTO roles_permisos (id_rol, id_permiso) VALUES
(4, 6), (4, 7), (4, 8), (4, 9), (4, 10), (4, 11), (4, 14), (4, 15);