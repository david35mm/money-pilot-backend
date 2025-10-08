from sqlalchemy import Boolean
from sqlalchemy import Column
from sqlalchemy import Date
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import Numeric
from sqlalchemy import String
from sqlalchemy import Text
from sqlalchemy.orm import relationship

from .base import Base
from .categoria import Categoria
from .usuario import Usuario


class Transaccion(Base):
  __tablename__ = 'transacciones'  # Asegura el nombre de la tabla

  id_transaccion = Column(Integer, primary_key=True, index=True)
  id_usuario = Column(Integer,
                      ForeignKey("usuarios.id_usuario"),
                      nullable=False)
  id_categoria = Column(Integer,
                        ForeignKey("categorias.id_categoria"),
                        nullable=True)
  monto = Column(Numeric(12, 2), nullable=False)
  fecha = Column(Date, nullable=False)
  tipo = Column(String(10),
                nullable=False)  # 'gasto' o 'ingreso'. CHECK se aplica en la DB
  es_unico = Column(Boolean, default=False)
  notas = Column(Text, nullable=True)

  # Relaciones
  usuario = relationship("Usuario", back_populates="transacciones")
  categoria = relationship("Categoria", back_populates="transacciones")


# Añadir la relación inversa al modelo Usuario
Usuario.transacciones = relationship("Transaccion",
                                     back_populates="usuario",
                                     cascade="all, delete-orphan")
# Añadir la relación inversa al modelo Categoria
Categoria.transacciones = relationship("Transaccion",
                                       back_populates="categoria")
