from sqlalchemy import CheckConstraint
from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String

from .base import Base


class Categoria(Base):
  __tablename__ = 'categorias'  # Asegura el nombre de la tabla

  id_categoria = Column(Integer, primary_key=True, index=True)
  nombre = Column(String(50), nullable=False)
  tipo = Column(String(10),
                CheckConstraint("tipo IN ('gasto', 'ingreso')",
                                name='check_tipo_categoria'),
                nullable=False)  # 'gasto' o 'ingreso'
