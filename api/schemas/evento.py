from datetime import date
from typing import Optional

from pydantic import BaseModel

from .base import BaseSchema


# --- Esquemas para Crear/Actualizar ---
class EventoFinancieroCreate(BaseModel):
  id_usuario: int
  tipo: str  # 'ingreso' o 'gasto'
  # Solo uno de estos dos debe estar presente según el tipo
  id_categoria_gasto: Optional[int] = None
  id_categoria_ingreso: Optional[int] = None
  id_fuente_ingreso: Optional[int] = None  # Solo para tipo 'ingreso'
  monto: float
  fecha: date
  descripcion: Optional[str] = None
  es_unico: Optional[bool] = False


class EventoFinancieroUpdate(BaseModel):
  # Similar a Create, pero opcional
  id_categoria_gasto: Optional[int] = None
  id_categoria_ingreso: Optional[int] = None
  id_fuente_ingreso: Optional[int] = None
  monto: Optional[float] = None
  fecha: Optional[date] = None
  descripcion: Optional[str] = None
  es_unico: Optional[bool] = None


# --- Esquema para Lectura (respuesta de la API) ---
class EventoFinanciero(BaseSchema):
  id_evento: int
  id_usuario: int
  tipo: str
  id_categoria_gasto: Optional[int] = None
  id_categoria_ingreso: Optional[int] = None
  id_fuente_ingreso: Optional[int] = None
  monto: float
  fecha: date
  descripcion: Optional[str] = None
  es_unico: bool
  semana_inicio: Optional[date] = None  # Fecha del lunes de la semana

  class Config:
    from_attributes = True
