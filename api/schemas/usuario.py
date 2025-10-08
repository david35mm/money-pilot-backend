from datetime import datetime

from pydantic import BaseModel
from pydantic import EmailStr

from .base import BaseSchema


# --- Esquemas para Crear/Actualizar ---
class UsuarioCreate(BaseModel):
  email: EmailStr
  password: str
  nombre: str


class UsuarioUpdate(BaseModel):
  nombre: str | None = None


# --- Esquema para Lectura (respuesta de la API) ---
class Usuario(BaseSchema):
  id_usuario: int
  email: EmailStr
  nombre: str
  created_at: datetime

  class Config:
    from_attributes = True
