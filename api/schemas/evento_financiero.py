from datetime import date
from typing import List, Optional

from pydantic import BaseModel


class EventoFinancieroCreate(BaseModel):
  tipo: str
  id_categoria_gasto: Optional[int] = None
  id_categoria_ingreso: Optional[int] = None
  monto: float
  fecha: date
  descripcion: Optional[str] = None
  es_unico: Optional[bool] = True
  semana_inicio: Optional[date] = None


class EventoFinancieroUpdate(BaseModel):
  tipo: Optional[str] = None
  id_categoria_gasto: Optional[int] = None
  id_categoria_ingreso: Optional[int] = None
  monto: Optional[float] = None
  fecha: Optional[date] = None
  descripcion: Optional[str] = None
  es_unico: Optional[bool] = None
  semana_inicio: Optional[date] = None


class EventoFinancieroDBRead(BaseModel):
  id_evento: int
  id_usuario: int
  tipo: str
  id_categoria_gasto: Optional[int]
  id_categoria_ingreso: Optional[int]
  monto: float
  fecha: date
  descripcion: Optional[str]
  es_unico: bool
  semana_inicio: Optional[date]

  class Config:
    from_attributes = True


class EventoFinancieroListRead(BaseModel):
  id_evento: int
  tipo: str
  monto: float
  fecha: date
  descripcion: Optional[str]
  es_unico: Optional[bool]
  semana_inicio: Optional[date]
  categoria: Optional[str]

  class Config:
    orm_mode = True


class EventosFinancierosResponse(BaseModel):
  eventos: List[EventoFinancieroListRead]
  total_eventos: int
  total_gastos: float
  total_ingresos: float
