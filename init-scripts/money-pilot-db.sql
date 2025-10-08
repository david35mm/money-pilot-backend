-- Estructura de base de datos para MoneyPilot (MVP)
-- KISS: Simple, funcional, enfocada en el core del producto.

-- Tabla de usuarios (autenticación y datos básicos)
CREATE TABLE public.usuarios (
    id_usuario SERIAL PRIMARY KEY,
    email VARCHAR(100) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    nombre VARCHAR(100), -- Nombre completo opcional aquí
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Tabla de categorías para gastos/ingresos
CREATE TABLE public.categorias (
    id_categoria SERIAL PRIMARY KEY,
    nombre VARCHAR(50) NOT NULL,
    tipo VARCHAR(10) CHECK (tipo IN ('gasto', 'ingreso'))
);

-- Tabla de transacciones
CREATE TABLE public.transacciones (
    id_transaccion SERIAL PRIMARY KEY,
    id_usuario INTEGER NOT NULL,
    id_categoria INTEGER,
    monto NUMERIC(12,2) NOT NULL,
    fecha DATE NOT NULL,
    tipo VARCHAR(10) NOT NULL CHECK (tipo IN ('gasto', 'ingreso')),
    es_unico BOOLEAN DEFAULT FALSE, -- Para US1.3
    notas TEXT,
    FOREIGN KEY (id_usuario) REFERENCES usuarios(id_usuario) ON DELETE CASCADE,
    FOREIGN KEY (id_categoria) REFERENCES categorias(id_categoria)
);

-- Tabla de metas financieras
CREATE TABLE public.metas (
    id_meta SERIAL PRIMARY KEY,
    id_usuario INTEGER NOT NULL,
    descripcion VARCHAR(200) NOT NULL,
    monto_objetivo NUMERIC(12,2) NOT NULL,
    fecha_objetivo DATE NOT NULL,
    monto_actual NUMERIC(12,2) DEFAULT 0,
    estado VARCHAR(20) DEFAULT 'en_progreso' CHECK (estado IN ('en_progreso', 'cumplida', 'cancelada')),
    FOREIGN KEY (id_usuario) REFERENCES usuarios(id_usuario) ON DELETE CASCADE
);

-- Tabla de presupuestos
CREATE TABLE public.presupuestos (
    id_presupuesto SERIAL PRIMARY KEY,
    id_usuario INTEGER NOT NULL,
    id_categoria INTEGER NOT NULL,
    monto_maximo NUMERIC(12,2) NOT NULL,
    mes DATE NOT NULL, -- Fecha que representa el mes (ej. 2025-10-01)
    FOREIGN KEY (id_usuario) REFERENCES usuarios(id_usuario) ON DELETE CASCADE,
    FOREIGN KEY (id_categoria) REFERENCES categorias(id_categoria)
);

-- Tabla de alertas para presupuestos
CREATE TABLE public.alertas (
    id_alerta SERIAL PRIMARY KEY,
    id_usuario INTEGER NOT NULL,
    id_presupuesto INTEGER NOT NULL,
    umbral NUMERIC(3,2) DEFAULT 0.8, -- 80% por defecto (US2.2)
    disparada BOOLEAN DEFAULT FALSE,
    fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (id_usuario) REFERENCES usuarios(id_usuario) ON DELETE CASCADE,
    FOREIGN KEY (id_presupuesto) REFERENCES presupuestos(id_presupuesto)
);

-- Nueva tabla: Perfil de usuario detallado (para US1.2 y futuras funcionalidades)
CREATE TABLE public.perfiles_usuario (
    id_perfil SERIAL PRIMARY KEY,
    id_usuario INTEGER NOT NULL UNIQUE, -- Relación 1 a 1 con usuarios
    -- Información Personal (del JSON)
    nombre_completo VARCHAR(100),
    edad INTEGER CHECK (edad > 0 AND edad < 150),
    pais VARCHAR(50),
    ciudad VARCHAR(100),
    -- Información Financiera (del JSON - valores iniciales o promedio)
    ingreso_mensual NUMERIC(12,2),
    tipo_ingreso VARCHAR(20) CHECK (tipo_ingreso IN ('fijo', 'variable', 'mixto', 'otro')),
    -- NOTA: gastos_principales, deudas, ahorro_mensual se calculan dinámicamente
    -- desde transacciones/metas. No se almacenan fijos aquí.
    -- Metas (del JSON - principal)
    meta_principal VARCHAR(100), -- Ej: "crear_fondo_emergencia"
    plazo_meta VARCHAR(20), -- Ej: "6_meses"
    monto_objetivo_meta NUMERIC(12,2), -- Monto de la meta_principal
    -- Perfil de Conocimiento (del JSON)
    nivel_conocimiento_financiero INTEGER CHECK (nivel_conocimiento_financiero >= 1 AND nivel_conocimiento_financiero <= 5),
    tolerancia_riesgo VARCHAR(20) CHECK (tolerancia_riesgo IN ('bajo', 'medio', 'alto')),
    areas_interes TEXT, -- Almacenado como string separado por comas por simplicidad
    -- Preferencias (del JSON)
    tono_comunicacion VARCHAR(20) CHECK (tono_comunicacion IN ('amigable', 'formal', 'informativo')),
    idioma VARCHAR(5) DEFAULT 'es',
    notificaciones_diarias BOOLEAN DEFAULT TRUE,
    horario_preferido_notif TIME DEFAULT '08:00:00',
    canal_notif_preferido VARCHAR(10) DEFAULT 'push' CHECK (canal_notif_preferido IN ('push', 'email', 'sms')),
    -- Metadatos
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    ultima_actualizacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (id_usuario) REFERENCES usuarios(id_usuario) ON DELETE CASCADE
);

-- Indices basicos para mejorar rendimiento en busquedas comunes
CREATE INDEX idx_transacciones_usuario_fecha ON transacciones (id_usuario, fecha);
CREATE INDEX idx_transacciones_usuario_categoria ON transacciones (id_usuario, id_categoria);
CREATE INDEX idx_presupuestos_usuario_categoria ON presupuestos (id_usuario, id_categoria);
CREATE INDEX idx_metas_usuario_estado ON metas (id_usuario, estado);