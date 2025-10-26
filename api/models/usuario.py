from api.models.base import Base
from sqlalchemy import Column
from sqlalchemy import DateTime
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func


class Usuario(Base):
  __tablename__ = "usuarios"

  id_usuario = Column(Integer, primary_key=True, index=True)
  email = Column(String(100), unique=True, index=True, nullable=False)
  password_hash = Column(String(255), nullable=False)
  created_at = Column(DateTime, server_default=func.now())

  perfil = relationship("PerfilUsuario",
                        back_populates="usuario",
                        uselist=False)
