from datetime import datetime
from typing import Optional

from pydantic import BaseModel

from .base import BaseSchema


# --- Esquemas para Crear/Actualizar ---
class AlertaCreate(BaseModel):
  id_usuario: int
  id_presupuesto: int
  umbral: Optional[float] = 0.8  # Valor por defecto del 80%


class AlertaUpdate(BaseModel):
  id_presupuesto: Optional[int] = None
  umbral: Optional[float] = None
  disparada: Optional[bool] = None


# --- Esquema para Lectura (respuesta de la API) ---
class Alerta(BaseSchema):
  id_alerta: int
  id_usuario: int
  id_presupuesto: int
  umbral: float
  disparada: bool
  fecha: datetime

  class Config:
    from_attributes = True
