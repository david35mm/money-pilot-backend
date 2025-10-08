from typing import Optional

from pydantic import BaseModel

from .base import BaseSchema


# --- Esquemas para Crear/Actualizar ---
class CategoriaCreate(BaseModel):
  nombre: str
  tipo: str  # 'gasto' o 'ingreso'


class CategoriaUpdate(BaseModel):
  nombre: Optional[str] = None
  tipo: Optional[str] = None  # 'gasto' o 'ingreso'


# --- Esquema para Lectura (respuesta de la API) ---
class Categoria(BaseSchema):
  id_categoria: int
  nombre: str
  tipo: str

  class Config:
    from_attributes = True
