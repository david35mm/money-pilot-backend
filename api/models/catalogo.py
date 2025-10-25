from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String

from .base import Base


class PaisLatam(Base):
  __tablename__ = 'paises_latam'
  id_pais = Column(Integer, primary_key=True, index=True)
  codigo = Column(String(2), nullable=False, unique=True)
  nombre = Column(String(50), nullable=False)


class CategoriaGasto(Base):
  __tablename__ = 'categorias_gastos'
  id_categoria_gasto = Column(Integer, primary_key=True, index=True)
  nombre = Column(String(50), nullable=False, unique=True)


class CategoriaIngreso(Base):
  __tablename__ = 'categorias_ingresos'
  id_categoria_ingreso = Column(Integer, primary_key=True, index=True)
  nombre = Column(String(50), nullable=False, unique=True)


class FuenteIngreso(Base):
  __tablename__ = 'fuentes_ingreso'
  id_fuente_ingreso = Column(Integer, primary_key=True, index=True)
  nombre = Column(String(100), nullable=False, unique=True)
