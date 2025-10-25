-- Estructura de base de datos para MoneyPilot

-- Tabla de usuarios (autenticación y datos básicos)
CREATE TABLE public.usuarios (
  id_usuario SERIAL PRIMARY KEY,
  email VARCHAR(100) NOT NULL UNIQUE,
  password_hash VARCHAR(255) NOT NULL,
  -- nombre VARCHAR(100), -- Nombre completo opcional aquí (ya no se usa aquí, va en perfiles_usuario)
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Tabla de países de Latinoamérica (catálogo)
CREATE TABLE public.paises_latam (
  id_pais SERIAL PRIMARY KEY,
  codigo VARCHAR(2) NOT NULL UNIQUE,
  nombre VARCHAR(50) NOT NULL
);

-- Tabla de categorías de gastos (catálogo)
CREATE TABLE public.categorias_gastos (
  id_categoria_gasto SERIAL PRIMARY KEY,
  nombre VARCHAR(50) NOT NULL UNIQUE
);

-- Tabla de categorías de ingresos (catálogo)
CREATE TABLE public.categorias_ingresos (
  id_categoria_ingreso SERIAL PRIMARY KEY,
  nombre VARCHAR(50) NOT NULL UNIQUE
);

-- Tabla de fuentes de ingreso (catálogo)
CREATE TABLE public.fuentes_ingreso (
  id_fuente_ingreso SERIAL PRIMARY KEY,
  nombre VARCHAR(100) NOT NULL UNIQUE
);

-- Tabla de perfiles de usuario detallado (información personal y resumen financiero)
CREATE TABLE public.perfiles_usuario (
  id_perfil SERIAL PRIMARY KEY,
  id_usuario INTEGER NOT NULL UNIQUE, -- Relación 1 a 1 con usuarios
  -- Información Personal
  nombre VARCHAR(100),
  apellido VARCHAR(100),
  fecha_nacimiento DATE,
  id_pais_residencia INTEGER, -- FK a paises_latam
  acepta_terminos BOOLEAN DEFAULT FALSE,
  -- Información Financiera Resumen (del nuevo JSON)
  ingreso_mensual_estimado NUMERIC(12,2),
  gastos_fijos_mensuales NUMERIC(12,2),
  gastos_variables_mensuales NUMERIC(12,2),
  ahorro_actual NUMERIC(12,2) DEFAULT 0,
  deuda_total NUMERIC(12,2) DEFAULT 0,
  monto_meta_ahorro NUMERIC(12,2),
  plazo_meta_ahorro_meses INTEGER,
  ahorro_planificado_mensual NUMERIC(12,2),
  -- Campo para almacenar múltiples fuentes de ingreso seleccionadas (Opción 1: Array)
  fuentes_ingreso TEXT[], -- Almacena IDs o nombres de fuentes_ingreso como array de texto
  -- Campo para almacenar múltiples fuentes de ingreso seleccionadas (Opción 2: JSON)
  -- fuentes_ingreso JSONB, -- Almacena IDs o nombres de fuentes_ingreso como JSONB
  fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  ultima_actualizacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (id_usuario) REFERENCES usuarios(id_usuario) ON DELETE CASCADE,
  FOREIGN KEY (id_pais_residencia) REFERENCES paises_latam(id_pais) ON DELETE SET NULL -- O CASCADE si se borra el país
  -- No se puede tener FK compuesta (nombre, codigo) directamente en SQL estándar sin una PK compuesta en paises_latam
  -- Esta FK apunta solo al id_pais, que es único.
);

-- Tabla intermedia para relacionar perfiles con fuentes de ingreso seleccionadas (Opción 3: Tabla Intermedia)
-- Si se elige esta opción, comenta o elimina el campo 'fuentes_ingreso' de 'perfiles_usuario'.
-- CREATE TABLE public.perfiles_fuentes_ingreso (
--   id_perfil INTEGER NOT NULL,
--   id_fuente_ingreso INTEGER NOT NULL,
--   PRIMARY KEY (id_perfil, id_fuente_ingreso),
--   FOREIGN KEY (id_perfil) REFERENCES perfiles_usuario(id_perfil) ON DELETE CASCADE,
--   FOREIGN KEY (id_fuente_ingreso) REFERENCES fuentes_ingreso(id_fuente_ingreso) ON DELETE CASCADE
-- );

-- Tabla de eventos financieros (transacciones detalladas)
CREATE TABLE public.eventos_financieros (
  id_evento SERIAL PRIMARY KEY,
  id_usuario INTEGER NOT NULL, -- FK al usuario dueño del evento
  tipo VARCHAR(10) NOT NULL CHECK (tipo IN ('ingreso', 'gasto')), -- 'ingreso' o 'gasto'
  -- FK condicional: una transacción es de gasto O de ingreso
  id_categoria_gasto INTEGER NULL, -- FK a categorias_gastos (solo si tipo = 'gasto')
  id_categoria_ingreso INTEGER NULL, -- FK a categorias_ingresos (solo si tipo = 'ingreso')
  id_fuente_ingreso INTEGER NULL, -- FK a fuentes_ingreso (solo si tipo = 'ingreso')
  monto NUMERIC(12,2) NOT NULL,
  fecha DATE NOT NULL,
  descripcion TEXT,
  es_unico BOOLEAN DEFAULT FALSE, -- Para US1.3
  semana_inicio DATE, -- Fecha del lunes de la semana a la que pertenece (para agrupar)
  fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (id_usuario) REFERENCES usuarios(id_usuario) ON DELETE CASCADE,
  FOREIGN KEY (id_categoria_gasto) REFERENCES categorias_gastos(id_categoria_gasto) ON DELETE SET NULL,
  FOREIGN KEY (id_categoria_ingreso) REFERENCES categorias_ingresos(id_categoria_ingreso) ON DELETE SET NULL,
  FOREIGN KEY (id_fuente_ingreso) REFERENCES fuentes_ingreso(id_fuente_ingreso) ON DELETE SET NULL,
  -- Asegura que solo una de las categorías esté presente según el tipo
  CONSTRAINT chk_categoria_tipo CHECK (
    (tipo = 'gasto' AND id_categoria_gasto IS NOT NULL AND id_categoria_ingreso IS NULL) OR
    (tipo = 'ingreso' AND id_categoria_ingreso IS NOT NULL AND id_categoria_gasto IS NULL)
  )
);

-- Índices básicos para mejorar rendimiento en búsquedas comunes
CREATE INDEX idx_eventos_usuario_fecha ON eventos_financieros (id_usuario, fecha);
CREATE INDEX idx_eventos_usuario_tipo ON eventos_financieros (id_usuario, tipo);
CREATE INDEX idx_eventos_semana_inicio ON eventos_financieros (semana_inicio);
CREATE INDEX idx_perfiles_usuario_usuario ON perfiles_usuario (id_usuario);
CREATE INDEX idx_perfiles_usuario_pais_residencia ON perfiles_usuario (id_pais_residencia); -- Nuevo índice
-- CREATE INDEX idx_perfiles_fuentes_ingreso_perfil ON perfiles_fuentes_ingreso (id_perfil); -- Si usas tabla intermedia