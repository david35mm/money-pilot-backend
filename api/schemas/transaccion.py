from datetime import date
from typing import Optional

from pydantic import BaseModel

from .base import BaseSchema


# --- Esquemas para Crear/Actualizar ---
class TransaccionCreate(BaseModel):
  id_usuario: int
  id_categoria: Optional[int] = None  # Puede ser nulo si no se asigna categoría
  monto: float
  fecha: date
  tipo: str  # 'gasto' o 'ingreso'
  es_unico: Optional[bool] = False
  notas: Optional[str] = None


class TransaccionUpdate(BaseModel):
  id_categoria: Optional[int] = None
  monto: Optional[float] = None
  fecha: Optional[date] = None
  tipo: Optional[str] = None  # 'gasto' o 'ingreso'
  es_unico: Optional[bool] = None
  notas: Optional[str] = None


# --- Esquema para Lectura (respuesta de la API) ---
class Transaccion(BaseSchema):
  id_transaccion: int
  id_usuario: int
  id_categoria: Optional[int] = None
  monto: float
  fecha: date
  tipo: str
  es_unico: bool
  notas: Optional[str]

  class Config:
    from_attributes = True
