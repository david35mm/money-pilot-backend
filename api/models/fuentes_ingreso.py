from api.models.base import Base
from sqlalchemy import String
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column


class FuenteIngreso(Base):
  __tablename__ = "fuentes_ingreso"

  id_fuente_ingreso: Mapped[int] = mapped_column(primary_key=True, index=True)
  nombre: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
