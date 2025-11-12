from datetime import datetime
from datetime import timezone
from typing import List, Optional

from api.models.base import Base
from sqlalchemy import ARRAY
from sqlalchemy import Boolean
from sqlalchemy import Date
from sqlalchemy import DateTime
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import Numeric
from sqlalchemy import String
from sqlalchemy import Text
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship


class PerfilUsuario(Base):
  __tablename__ = "perfiles_usuario"

  id_perfil: Mapped[int] = mapped_column(primary_key=True, index=True)
  id_usuario: Mapped[int] = mapped_column(Integer,
                                          ForeignKey("usuarios.id_usuario"),
                                          unique=True,
                                          nullable=False)

  nombre: Mapped[Optional[str]] = mapped_column(String(100))
  apellido: Mapped[Optional[str]] = mapped_column(String(100))
  fecha_nacimiento: Mapped[Optional[Date]] = mapped_column(Date)
  # id_pais_residencia = mapped_column(Integer, ForeignKey("paises_latam.id_pais"))
  id_pais_residencia: Mapped[int] = mapped_column(Integer, nullable=False)
  acepta_terminos: Mapped[Optional[bool]] = mapped_column(Boolean,
                                                          default=False)

  ingreso_mensual_estimado: Mapped[Optional[float]] = mapped_column(
      Numeric(12, 2))
  gastos_fijos_mensuales: Mapped[Optional[float]] = mapped_column(Numeric(
      12, 2))
  gastos_variables_mensuales: Mapped[Optional[float]] = mapped_column(
      Numeric(12, 2))
  ahorro_actual: Mapped[Optional[float]] = mapped_column(Numeric(12, 2),
                                                         default=0)
  deuda_total: Mapped[Optional[float]] = mapped_column(Numeric(12, 2),
                                                       default=0)
  monto_meta_ahorro: Mapped[Optional[float]] = mapped_column(Numeric(12, 2))
  plazo_meta_ahorro_meses: Mapped[Optional[int]] = mapped_column(Integer)
  ahorro_planificado_mensual: Mapped[Optional[float]] = mapped_column(
      Numeric(12, 2))
  fuentes_ingreso: Mapped[Optional[List[str]]] = mapped_column(ARRAY(Text))

  fecha_creacion: Mapped[datetime] = mapped_column(
      DateTime, default=lambda: datetime.now(timezone.utc))
  ultima_actualizacion: Mapped[datetime] = mapped_column(
      DateTime,
      default=lambda: datetime.now(timezone.utc),
      onupdate=lambda: datetime.now(timezone.utc))

  usuario: Mapped["Usuario"] = relationship(back_populates="perfil")
  # pais = relationship("PaisLatam", lazy="joined")
