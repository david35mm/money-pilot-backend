from api.models.base import Base
from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String


class CategoriaGasto(Base):
  __tablename__ = "categorias_gastos"

  id_categoria_gasto = Column(Integer, primary_key=True, index=True)
  nombre = Column(String(50), unique=True, nullable=False)


class CategoriaIngreso(Base):
  __tablename__ = "categorias_ingresos"

  id_categoria_ingreso = Column(Integer, primary_key=True, index=True)
  nombre = Column(String(50), unique=True, nullable=False)
