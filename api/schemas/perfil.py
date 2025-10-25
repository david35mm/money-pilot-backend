from datetime import date
from typing import List, Optional

from pydantic import BaseModel
from pydantic import EmailStr

from .base import BaseSchema
from .catalogo import PaisLatamBase


# --- Esquemas para Crear/Actualizar ---
class PerfilUsuarioCreate(BaseModel):
  id_usuario: int
  nombre: Optional[str] = None
  apellido: Optional[str] = None
  fecha_nacimiento: Optional[date] = None
  id_pais_residencia: Optional[int] = None
  acepta_terminos: Optional[bool] = False

  ingreso_mensual_estimado: Optional[float] = None
  gastos_fijos_mensuales: Optional[float] = None
  gastos_variables_mensuales: Optional[float] = None
  ahorro_actual: Optional[float] = 0
  deuda_total: Optional[float] = 0
  monto_meta_ahorro: Optional[float] = None
  plazo_meta_ahorro_meses: Optional[int] = None
  ahorro_planificado_mensual: Optional[float] = None
  # Opción 1: fuentes_ingreso como lista de strings (IDs o nombres)
  fuentes_ingreso: Optional[
      List[str]] = None  # Lista de IDs o nombres de fuentes_ingreso


class PerfilUsuarioUpdate(BaseModel):
  nombre: Optional[str] = None
  apellido: Optional[str] = None
  fecha_nacimiento: Optional[date] = None
  id_pais_residencia: Optional[int] = None
  acepta_terminos: Optional[bool] = None

  ingreso_mensual_estimado: Optional[float] = None
  gastos_fijos_mensuales: Optional[float] = None
  gastos_variables_mensuales: Optional[float] = None
  ahorro_actual: Optional[float] = None
  deuda_total: Optional[float] = None
  monto_meta_ahorro: Optional[float] = None
  plazo_meta_ahorro_meses: Optional[int] = None
  ahorro_planificado_mensual: Optional[float] = None
  fuentes_ingreso: Optional[List[str]] = None


# --- Esquema para Lectura (respuesta de la API) ---
class PerfilUsuario(BaseSchema):
  id_perfil: int
  id_usuario: int
  nombre: Optional[str] = None
  apellido: Optional[str] = None
  fecha_nacimiento: Optional[date] = None
  id_pais_residencia: Optional[int] = None
  pais_residencia: Optional[PaisLatamBase] = None
  acepta_terminos: bool
  ingreso_mensual_estimado: Optional[float] = None
  gastos_fijos_mensuales: Optional[float] = None
  gastos_variables_mensuales: Optional[float] = None
  ahorro_actual: Optional[float] = 0
  deuda_total: Optional[float] = 0
  monto_meta_ahorro: Optional[float] = None
  plazo_meta_ahorro_meses: Optional[int] = None
  ahorro_planificado_mensual: Optional[float] = None
  # Opción 1: fuentes_ingreso como lista de strings
  fuentes_ingreso: Optional[List[str]] = None
  fecha_creacion: date
  ultima_actualizacion: date

  class Config:
    from_attributes = True
