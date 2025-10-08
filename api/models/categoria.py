from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String

from .base import Base


class Categoria(Base):
  __tablename__ = 'categorias'  # Asegura el nombre de la tabla

  id_categoria = Column(Integer, primary_key=True, index=True)
  nombre = Column(String(50), nullable=False)
  tipo = Column(String(10),
                nullable=False)  # 'gasto' o 'ingreso'. CHECK se aplica en la DB
