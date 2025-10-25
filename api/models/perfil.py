from sqlalchemy import ARRAY
from sqlalchemy import Boolean
from sqlalchemy import Column
from sqlalchemy import Date
from sqlalchemy import DateTime
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import Numeric
from sqlalchemy import String
from sqlalchemy import Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from .base import Base
from .catalogo import PaisLatam
from .usuario import Usuario


class PerfilUsuario(Base):
  __tablename__ = 'perfiles_usuario'

  id_perfil = Column(Integer, primary_key=True, index=True)
  id_usuario = Column(Integer,
                      ForeignKey("usuarios.id_usuario"),
                      unique=True,
                      nullable=False)
  # Relación con Usuario
  usuario = relationship("Usuario", back_populates="perfil")

  nombre = Column(String(100), nullable=True)
  apellido = Column(String(100), nullable=True)
  fecha_nacimiento = Column(Date, nullable=True)
  id_pais_residencia = Column(Integer,
                              ForeignKey("paises_latam.id_pais"),
                              nullable=True)
  acepta_terminos = Column(Boolean, default=False)

  ingreso_mensual_estimado = Column(Numeric(12, 2), nullable=True)
  gastos_fijos_mensuales = Column(Numeric(12, 2), nullable=True)
  gastos_variables_mensuales = Column(Numeric(12, 2), nullable=True)
  ahorro_actual = Column(Numeric(12, 2), default=0)
  deuda_total = Column(Numeric(12, 2), default=0)
  monto_meta_ahorro = Column(Numeric(12, 2), nullable=True)
  plazo_meta_ahorro_meses = Column(Integer, nullable=True)
  ahorro_planificado_mensual = Column(Numeric(12, 2), nullable=True)
  # Opción 1: Almacenar fuentes_ingreso como array de texto
  fuentes_ingreso = Column(
      ARRAY(String),
      nullable=True)  # Almacena IDs o nombres como array de texto

  fecha_creacion = Column(DateTime, server_default=func.now())
  ultima_actualizacion = Column(DateTime,
                                server_default=func.now(),
                                onupdate=func.now())

  pais_residencia_obj = relationship(
      "PaisLatam", back_populates="perfiles_usuario_asociados")


PaisLatam.perfiles_usuario_asociados = relationship(
    "PerfilUsuario", back_populates="pais_residencia_obj", uselist=True)

Usuario.perfil = relationship("PerfilUsuario",
                              back_populates="usuario",
                              uselist=False,
                              cascade="all, delete-orphan")
