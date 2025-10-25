from sqlalchemy import Column
from sqlalchemy import DateTime
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy.sql import func

from .base import Base


class Usuario(Base):
  __tablename__ = 'usuarios'  # Asegura el nombre de la tabla

  id_usuario = Column(Integer, primary_key=True, index=True)
  email = Column(String, unique=True, index=True, nullable=False)
  password_hash = Column(String, nullable=False)
  # nombre = Column(String, nullable=True) # Ya no se usa aquí, está en perfiles_usuario
  created_at = Column(DateTime, server_default=func.now())

  # Relaciones (ya definidas en los modelos relacionados)
  # perfil = relationship("PerfilUsuario", back_populates="usuario", uselist=False, cascade="all, delete-orphan") # Definida en PerfilUsuario
  # eventos = relationship("EventoFinanciero", back_populates="usuario", cascade="all, delete-orphan") # Definida en EventoFinanciero
