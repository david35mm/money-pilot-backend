from datetime import date
from typing import Optional

from pydantic import BaseModel

from .base import BaseSchema


# --- Esquemas para Crear/Actualizar ---
class MetaCreate(BaseModel):
  id_usuario: int
  descripcion: str
  monto_objetivo: float
  fecha_objetivo: date
  # monto_actual se inicializa en 0, no se envía en la creación
  # estado se inicializa en 'en_progreso', no se envía en la creación


class MetaUpdate(BaseModel):
  descripcion: Optional[str] = None
  monto_objetivo: Optional[float] = None
  fecha_objetivo: Optional[date] = None
  monto_actual: Optional[float] = None
  estado: Optional[str] = None  # 'en_progreso', 'cumplida', 'cancelada'


# --- Esquema para Lectura (respuesta de la API) ---
class Meta(BaseSchema):
  id_meta: int
  id_usuario: int
  descripcion: str
  monto_objetivo: float
  fecha_objetivo: date
  monto_actual: float
  estado: str

  class Config:
    from_attributes = True
