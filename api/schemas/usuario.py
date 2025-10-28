from datetime import datetime

from api.schemas.base import BaseSchema
from pydantic import EmailStr
from pydantic import Field


class UsuarioCreate(BaseSchema):
  email: EmailStr = Field(..., max_length=100)
  password: str = Field(..., min_length=6, max_length=255)


class UsuarioRead(BaseSchema):
  id_usuario: int
  email: EmailStr
  created_at: datetime
