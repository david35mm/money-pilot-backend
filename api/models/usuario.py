from datetime import datetime
from datetime import timezone

from api.models.base import Base
from sqlalchemy import DateTime
from sqlalchemy import String
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship


class Usuario(Base):
  __tablename__ = "usuarios"

  id_usuario: Mapped[int] = mapped_column(primary_key=True, index=True)
  email: Mapped[str] = mapped_column(String(100),
                                     unique=True,
                                     index=True,
                                     nullable=False)
  password_hash: Mapped[str] = mapped_column(String(255), nullable=False)
  created_at: Mapped[datetime] = mapped_column(
      DateTime, default=lambda: datetime.now(timezone.utc))

  perfil: Mapped["PerfilUsuario"] = relationship(back_populates="usuario",
                                                 uselist=False)
