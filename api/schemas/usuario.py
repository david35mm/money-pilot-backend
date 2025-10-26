from datetime import datetime

from pydantic import EmailStr
from pydantic import Field

from .base import BaseSchema


class UsuarioCreate(BaseSchema):
  email: EmailStr = Field(..., max_length=100)
  password: str = Field(..., min_length=6, max_length=255)


class UsuarioRead(BaseSchema):
  id_usuario: int
  email: EmailStr
  created_at: datetime
