from api.models.base import Base
from sqlalchemy import Boolean
from sqlalchemy import CheckConstraint
from sqlalchemy import Column
from sqlalchemy import Date
from sqlalchemy import DateTime
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import Numeric
from sqlalchemy import String
from sqlalchemy import text
from sqlalchemy.sql import func


class EventoFinanciero(Base):
  __tablename__ = "eventos_financieros"

  id_evento = Column(Integer, primary_key=True, index=True)
  id_usuario = Column(Integer,
                      ForeignKey("usuarios.id_usuario", ondelete="CASCADE"),
                      nullable=False)
  tipo = Column(String(10), nullable=False)  # 'INGRESO' o 'GASTO'

  id_categoria_gasto = Column(Integer,
                              ForeignKey("categorias_gastos.id_categoria_gasto",
                                         ondelete="SET NULL"),
                              nullable=True)
  id_categoria_ingreso = Column(Integer,
                                ForeignKey(
                                    "categorias_ingresos.id_categoria_ingreso",
                                    ondelete="SET NULL"),
                                nullable=True)

  monto = Column(Numeric(12, 2), nullable=False)
  fecha = Column(Date, nullable=False)
  descripcion = Column(String, nullable=True)
  es_unico = Column(Boolean, server_default=text("TRUE"))
  semana_inicio = Column(Date, nullable=True)
  fecha_creacion = Column(DateTime, server_default=func.now())

  __table_args__ = (CheckConstraint(
      "(tipo = 'gasto' AND id_categoria_gasto IS NOT NULL AND id_categoria_ingreso IS NULL) OR "
      "(tipo = 'ingreso' AND id_categoria_ingreso IS NOT NULL AND id_categoria_gasto IS NULL)",
      name="chk_categoria_tipo",
  ),)
