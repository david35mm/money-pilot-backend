from typing import List

from pydantic import BaseModel

from .base import BaseSchema


class PaisLatamBase(BaseModel):
  id: int
  codigo: str
  nombre: str

  class Config:
    from_attributes = True


class CategoriaGastoBase(BaseModel):
  id: int
  nombre: str

  class Config:
    from_attributes = True


class CategoriaIngresoBase(BaseModel):
  id: int
  nombre: str

  class Config:
    from_attributes = True


class FuenteIngresoBase(BaseModel):
  id: int
  nombre: str

  class Config:
    from_attributes = True


# Esquema para la respuesta del endpoint de catálogos (como lo espera el frontend)
class CatalogosResponseSchema(BaseModel):
  categoriasGastos: List[CategoriaGastoBase]
  categoriasIngresos: List[CategoriaIngresoBase]
  fuentesIngreso: List[FuenteIngresoBase]
  paisesLatam: List[PaisLatamBase]

  class Config:
    from_attributes = True
