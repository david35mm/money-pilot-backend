from datetime import date
from typing import Optional

from pydantic import BaseModel

from .base import BaseSchema


# --- Esquemas para Crear/Actualizar ---
class PresupuestoCreate(BaseModel):
  id_usuario: int
  id_categoria: int
  monto_maximo: float
  mes: date  # Fecha que representa el mes (ej. 2025-10-01)


class PresupuestoUpdate(BaseModel):
  id_categoria: Optional[int] = None
  monto_maximo: Optional[float] = None
  mes: Optional[date] = None


# --- Esquema para Lectura (respuesta de la API) ---
class Presupuesto(BaseSchema):
  id_presupuesto: int
  id_usuario: int
  id_categoria: int
  monto_maximo: float
  mes: date

  class Config:
    from_attributes = True
