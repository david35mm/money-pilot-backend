from sqlalchemy import Column
from sqlalchemy import Date
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import Numeric
from sqlalchemy.orm import relationship

from .base import Base
from .categoria import Categoria
from .usuario import Usuario


class Presupuesto(Base):
  __tablename__ = 'presupuestos'  # Asegura el nombre de la tabla

  id_presupuesto = Column(Integer, primary_key=True, index=True)
  id_usuario = Column(Integer,
                      ForeignKey("usuarios.id_usuario"),
                      nullable=False)
  id_categoria = Column(Integer,
                        ForeignKey("categorias.id_categoria"),
                        nullable=False)
  monto_maximo = Column(Numeric(12, 2), nullable=False)
  mes = Column(Date, nullable=False)  # Fecha que representa el mes

  # Relaciones
  usuario = relationship("Usuario", back_populates="presupuestos")
  categoria = relationship("Categoria", back_populates="presupuestos")


# Añadir la relación inversa al modelo Usuario
Usuario.presupuestos = relationship("Presupuesto",
                                    back_populates="usuario",
                                    cascade="all, delete-orphan")
# Añadir la relación inversa al modelo Categoria
Categoria.presupuestos = relationship("Presupuesto", back_populates="categoria")
