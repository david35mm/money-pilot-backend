from datetime import date
from datetime import datetime
from datetime import timezone
from typing import Optional

from api.models.base import Base
from sqlalchemy import Boolean
from sqlalchemy import CheckConstraint
from sqlalchemy import Date
from sqlalchemy import DateTime
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import Numeric
from sqlalchemy import String
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column


class EventoFinanciero(Base):
  __tablename__ = "eventos_financieros"

  id_evento: Mapped[int] = mapped_column(primary_key=True, index=True)
  id_usuario: Mapped[int] = mapped_column(Integer,
                                          ForeignKey("usuarios.id_usuario",
                                                     ondelete="CASCADE"),
                                          nullable=False)
  tipo: Mapped[str] = mapped_column(String(10),
                                    nullable=False)  # 'INGRESO' o 'GASTO'

  id_categoria_gasto: Mapped[Optional[int]] = mapped_column(
      Integer,
      ForeignKey("categorias_gastos.id_categoria_gasto", ondelete="SET NULL"),
      nullable=True)
  id_categoria_ingreso: Mapped[Optional[int]] = mapped_column(
      Integer,
      ForeignKey("categorias_ingresos.id_categoria_ingreso",
                 ondelete="SET NULL"),
      nullable=True)

  monto: Mapped[float] = mapped_column(Numeric(12, 2), nullable=False)
  fecha: Mapped[date] = mapped_column(Date, nullable=False)
  descripcion: Mapped[Optional[str]] = mapped_column(String, nullable=True)
  es_unico: Mapped[bool] = mapped_column(Boolean, default=True)
  semana_inicio: Mapped[Optional[date]] = mapped_column(Date, nullable=True)
  fecha_creacion: Mapped[datetime] = mapped_column(
      DateTime, default=lambda: datetime.now(timezone.utc))

  __table_args__ = (CheckConstraint(
      "(tipo = 'gasto' AND id_categoria_gasto IS NOT NULL AND id_categoria_ingreso IS NULL) OR "
      "(tipo = 'ingreso' AND id_categoria_ingreso IS NOT NULL AND id_categoria_gasto IS NULL)",
      name="chk_categoria_tipo",
  ),)
