from sqlalchemy import Boolean
from sqlalchemy import CheckConstraint
from sqlalchemy import Column
from sqlalchemy import Date
from sqlalchemy import DateTime
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import Numeric
from sqlalchemy import String
from sqlalchemy import Time
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from .base import Base
from .usuario import Usuario


class PerfilUsuario(Base):
  __tablename__ = 'perfiles_usuario'  # Asegura el nombre de la tabla

  id_perfil = Column(Integer, primary_key=True, index=True)
  id_usuario = Column(Integer,
                      ForeignKey("usuarios.id_usuario"),
                      unique=True,
                      nullable=False)
  # Relación con Usuario
  usuario = relationship("Usuario", back_populates="perfil")

  # Campos del perfil
  nombre_completo = Column(String(100), nullable=True)
  edad = Column(Integer,
                CheckConstraint('edad > 0 AND edad < 150', name='check_edad'),
                nullable=True)
  pais = Column(String(50), nullable=True)
  ciudad = Column(String(100), nullable=True)
  ingreso_mensual = Column(Numeric(12, 2), nullable=True)
  tipo_ingreso = Column(
      String(20),
      CheckConstraint("tipo_ingreso IN ('fijo', 'variable', 'mixto', 'otro')",
                      name='check_tipo_ingreso'),
      nullable=True)
  meta_principal = Column(String(100), nullable=True)
  plazo_meta = Column(String(20), nullable=True)
  monto_objetivo_meta = Column(Numeric(12, 2), nullable=True)
  nivel_conocimiento_financiero = Column(
      Integer,
      CheckConstraint(
          'nivel_conocimiento_financiero >= 1 AND nivel_conocimiento_financiero <= 5',
          name='check_nivel_conocimiento'),
      nullable=True)
  tolerancia_riesgo = Column(
      String(20),
      CheckConstraint("tolerancia_riesgo IN ('bajo', 'medio', 'alto')",
                      name='check_tolerancia_riesgo'),
      nullable=True)
  areas_interes = Column(
      String, nullable=True)  # Puede ser una cadena separada por comas
  tono_comunicacion = Column(
      String(20),
      CheckConstraint(
          "tono_comunicacion IN ('amigable', 'formal', 'informativo')",
          name='check_tono_comunicacion'),
      nullable=True)
  idioma = Column(String(5), nullable=True)
  notificaciones_diarias = Column(Boolean, nullable=True)
  horario_preferido_notif = Column(Time, nullable=True)
  canal_notif_preferido = Column(
      String(10),
      CheckConstraint("canal_notif_preferido IN ('push', 'email', 'sms')",
                      name='check_canal_notif'),
      nullable=True)
  fecha_creacion = Column(DateTime, server_default=func.now())
  ultima_actualizacion = Column(DateTime,
                                server_default=func.now(),
                                onupdate=func.now())


# Añadir la relación inversa al modelo Usuario
Usuario.perfil = relationship("PerfilUsuario",
                              back_populates="usuario",
                              uselist=False,
                              cascade="all, delete-orphan")
