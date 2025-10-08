from sqlalchemy import Boolean
from sqlalchemy import Column
from sqlalchemy import DateTime
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import Numeric
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from .base import Base
from .presupuesto import Presupuesto
from .usuario import Usuario


class Alerta(Base):
  __tablename__ = 'alertas'  # Asegura el nombre de la tabla

  id_alerta = Column(Integer, primary_key=True, index=True)
  id_usuario = Column(Integer,
                      ForeignKey("usuarios.id_usuario"),
                      nullable=False)
  id_presupuesto = Column(Integer,
                          ForeignKey("presupuestos.id_presupuesto"),
                          nullable=False)
  umbral = Column(Numeric(3, 2), default=0.8)  # Valor por defecto del 80%
  disparada = Column(Boolean, default=False)
  fecha = Column(DateTime, server_default=func.now())

  # Relaciones
  usuario = relationship("Usuario", back_populates="alertas")
  presupuesto = relationship("Presupuesto", back_populates="alertas")


# Añadir la relación inversa al modelo Usuario
Usuario.alertas = relationship("Alerta",
                               back_populates="usuario",
                               cascade="all, delete-orphan")
# Añadir la relación inversa al modelo Presupuesto
Presupuesto.alertas = relationship("Alerta", back_populates="presupuesto")
