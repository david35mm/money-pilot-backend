from sqlalchemy import Column
from sqlalchemy import Date
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import Numeric
from sqlalchemy import String
from sqlalchemy.orm import relationship

from .base import Base
from .usuario import Usuario


class Meta(Base):
  __tablename__ = 'metas'  # Asegura el nombre de la tabla

  id_meta = Column(Integer, primary_key=True, index=True)
  id_usuario = Column(Integer,
                      ForeignKey("usuarios.id_usuario"),
                      nullable=False)
  descripcion = Column(String(200), nullable=False)
  monto_objetivo = Column(Numeric(12, 2), nullable=False)
  fecha_objetivo = Column(Date, nullable=False)
  monto_actual = Column(Numeric(12, 2), default=0)
  estado = Column(String(20), default='en_progreso')  # CHECK se aplica en la DB

  # Relación
  usuario = relationship("Usuario", back_populates="metas")


# Añadir la relación inversa al modelo Usuario
Usuario.metas = relationship("Meta",
                             back_populates="usuario",
                             cascade="all, delete-orphan")
