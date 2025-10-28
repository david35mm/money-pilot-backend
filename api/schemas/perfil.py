from datetime import date
from datetime import datetime
from typing import List, Optional

from api.schemas.base import BaseSchema
from pydantic import BaseModel
from pydantic import Field


class PerfilPersonalCreate(BaseModel):
  nombre: str
  apellido: str
  fecha_nacimiento: date
  codigo_pais: str
  acepta_terminos: bool


class InformacionPersonal(BaseSchema):
  nombre: str = Field(..., max_length=100)
  apellido: str = Field(..., max_length=100)
  fecha_nacimiento: date
  pais_residencia: str = Field(..., max_length=50)
  codigo_pais: str = Field(..., min_length=2, max_length=2)
  acepta_terminos: bool


class MetaAhorro(BaseSchema):
  monto: float
  plazo_meses: int


class PerfilFinanciero(BaseSchema):
  ingreso_mensual_estimado: float
  fuentes_ingreso: List[str]
  gastos_fijos_mensuales: float
  gastos_variables_mensuales: float
  ahorro_actual: float
  deuda_total: float
  meta_ahorro: MetaAhorro
  ahorro_planificado_mensual: float


class DatosFinancieros(BaseSchema):
  perfil_financiero: PerfilFinanciero


class PerfilCompletoCreate(BaseSchema):
  informacion_personal: InformacionPersonal
  datos_financieros: DatosFinancieros


class PerfilUsuarioRead(BaseSchema):
  id_perfil: int
  id_usuario: int
  nombre: Optional[str]
  apellido: Optional[str]
  fecha_nacimiento: Optional[date]
  id_pais_residencia: Optional[int]
  acepta_terminos: Optional[bool]
  ingreso_mensual_estimado: Optional[float]
  gastos_fijos_mensuales: Optional[float]
  gastos_variables_mensuales: Optional[float]
  ahorro_actual: Optional[float]
  deuda_total: Optional[float]
  monto_meta_ahorro: Optional[float]
  plazo_meta_ahorro_meses: Optional[int]
  ahorro_planificado_mensual: Optional[float]
  fuentes_ingreso: Optional[List[str]]
  fecha_creacion: datetime
  ultima_actualizacion: datetime
