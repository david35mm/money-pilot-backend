CREATE TABLE public.usuarios (
  id_usuario SERIAL PRIMARY KEY,
  email VARCHAR(100) NOT NULL UNIQUE,
  password_hash VARCHAR(255) NOT NULL,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE public.paises_latam (
  id_pais SERIAL PRIMARY KEY,
  codigo VARCHAR(2) NOT NULL UNIQUE,
  nombre VARCHAR(50) NOT NULL
);

CREATE TABLE public.categorias_gastos (
  id_categoria_gasto SERIAL PRIMARY KEY,
  nombre VARCHAR(50) NOT NULL UNIQUE
);

CREATE TABLE public.categorias_ingresos (
  id_categoria_ingreso SERIAL PRIMARY KEY,
  nombre VARCHAR(50) NOT NULL UNIQUE
);

CREATE TABLE public.fuentes_ingreso (
  id_fuente_ingreso SERIAL PRIMARY KEY,
  nombre VARCHAR(100) NOT NULL UNIQUE
);

CREATE TABLE public.perfiles_usuario (
  id_perfil SERIAL PRIMARY KEY,
  id_usuario INTEGER NOT NULL UNIQUE REFERENCES usuarios(id_usuario) ON DELETE CASCADE,
  nombre VARCHAR(100),
  apellido VARCHAR(100),
  fecha_nacimiento DATE,
  id_pais_residencia INTEGER REFERENCES paises_latam(id_pais) ON DELETE SET NULL,
  acepta_terminos BOOLEAN DEFAULT FALSE,
  ingreso_mensual_estimado NUMERIC(12,2),
  gastos_fijos_mensuales NUMERIC(12,2),
  gastos_variables_mensuales NUMERIC(12,2),
  ahorro_actual NUMERIC(12,2),
  deuda_total NUMERIC(12,2),
  monto_meta_ahorro NUMERIC(12,2),
  plazo_meta_ahorro_meses INTEGER,
  ahorro_planificado_mensual NUMERIC(12,2),
  fuentes_ingreso TEXT[],
  fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  ultima_actualizacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE OR REPLACE FUNCTION actualizar_ultima_actualizacion()
RETURNS TRIGGER AS $$
BEGIN
  NEW.ultima_actualizacion = CURRENT_TIMESTAMP;
  RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trigger_actualizar_fecha_perfil
BEFORE UPDATE ON public.perfiles_usuario
FOR EACH ROW
EXECUTE FUNCTION actualizar_ultima_actualizacion();

CREATE TABLE public.eventos_financieros (
  id_evento SERIAL PRIMARY KEY,
  id_usuario INTEGER NOT NULL REFERENCES usuarios(id_usuario) ON DELETE CASCADE,
  tipo VARCHAR(10) NOT NULL CHECK (tipo IN ('ingreso', 'gasto')),
  id_categoria_gasto INTEGER REFERENCES categorias_gastos(id_categoria_gasto) ON DELETE SET NULL,
  id_categoria_ingreso INTEGER REFERENCES categorias_ingresos(id_categoria_ingreso) ON DELETE SET NULL,
  id_fuente_ingreso INTEGER REFERENCES fuentes_ingreso(id_fuente_ingreso) ON DELETE SET NULL,
  monto NUMERIC(12,2) NOT NULL,
  fecha DATE NOT NULL,
  descripcion TEXT,
  es_unico BOOLEAN DEFAULT FALSE,
  semana_inicio DATE,
  fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  CONSTRAINT chk_categoria_tipo CHECK (
    (tipo = 'gasto' AND id_categoria_gasto IS NOT NULL AND id_categoria_ingreso IS NULL) OR
    (tipo = 'ingreso' AND id_categoria_ingreso IS NOT NULL AND id_categoria_gasto IS NULL)
  )
);

CREATE INDEX idx_eventos_usuario_fecha ON eventos_financieros (id_usuario, fecha);
CREATE INDEX idx_eventos_usuario_tipo ON eventos_financieros (id_usuario, tipo);
CREATE INDEX idx_eventos_semana_inicio ON eventos_financieros (semana_inicio);
CREATE INDEX idx_perfiles_usuario_usuario ON perfiles_usuario (id_usuario);
CREATE INDEX idx_perfiles_usuario_pais_residencia ON perfiles_usuario (id_pais_residencia);

INSERT INTO public.paises_latam (codigo, nombre) VALUES
('AR', 'Argentina'),
('BO', 'Bolivia'),
('BR', 'Brasil'),
('CL', 'Chile'),
('CO', 'Colombia'),
('CR', 'Costa Rica'),
('CU', 'Cuba'),
('EC', 'Ecuador'),
('SV', 'El Salvador'),
('GT', 'Guatemala'),
('HN', 'Honduras'),
('MX', 'México'),
('NI', 'Nicaragua'),
('PA', 'Panamá'),
('PY', 'Paraguay'),
('PE', 'Perú'),
('DO', 'República Dominicana'),
('UY', 'Uruguay'),
('VE', 'Venezuela');

INSERT INTO public.categorias_gastos (nombre) VALUES
('COMIDA'),
('TRANSPORTE'),
('VIAJES'),
('SALUD'),
('HOGAR'),
('MERCADO'),
('OCIO'),
('OTROS');

INSERT INTO public.categorias_ingresos (nombre) VALUES
('SALARIO'),
('FREELANCE'),
('NEGOCIO'),
('TRANSFERENCIAS'),
('INVERSIONES'),
('OTROS');

INSERT INTO public.fuentes_ingreso (nombre) VALUES
('EMPLEADO FORMAL (ASALARIADO)'),
('EMPLEADO INFORMAL'),
('INDEPENDIENTE / CUENTA PROPIA'),
('EMPLEADOR / EMPRESARIO'),
('PENSIONADO / JUBILADO'),
('RENTISTA DE CAPITAL'),
('TRABAJADOR FAMILIAR SIN REMUNERACIÓN'),
('BENEFICIARIO DE SUBSIDIOS / AYUDAS'),
('DESEMPLEADO CON INGRESOS OCASIONALES'),
('DESEMPLEADO TOTAL (SIN INGRESOS)');