from api.models.base import Base
from sqlalchemy import String
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column


class CategoriaGasto(Base):
  __tablename__ = "categorias_gastos"

  id_categoria_gasto: Mapped[int] = mapped_column(primary_key=True, index=True)
  nombre: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)


class CategoriaIngreso(Base):
  __tablename__ = "categorias_ingresos"

  id_categoria_ingreso: Mapped[int] = mapped_column(primary_key=True,
                                                    index=True)
  nombre: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
