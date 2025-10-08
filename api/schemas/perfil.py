from datetime import datetime
from typing import Optional

from pydantic import BaseModel

from .base import BaseSchema


# --- Esquemas para Crear/Actualizar ---
class PerfilUsuarioCreate(BaseModel):
  id_usuario: int  # Se asocia el perfil con un usuario existente
  nombre_completo: Optional[str] = None
  edad: Optional[int] = None
  pais: Optional[str] = None
  ciudad: Optional[str] = None
  ingreso_mensual: Optional[float] = None
  tipo_ingreso: Optional[str] = None
  meta_principal: Optional[str] = None
  plazo_meta: Optional[str] = None
  monto_objetivo_meta: Optional[float] = None
  nivel_conocimiento_financiero: Optional[int] = None
  tolerancia_riesgo: Optional[str] = None
  areas_interes: Optional[str] = None  # Puede ser una cadena separada por comas
  tono_comunicacion: Optional[str] = None
  idioma: Optional[str] = None
  notificaciones_diarias: Optional[bool] = None
  horario_preferido_notif: Optional[str] = None  # Formato HH:MM:SS
  canal_notif_preferido: Optional[str] = None


class PerfilUsuarioUpdate(BaseModel):
  nombre_completo: Optional[str] = None
  edad: Optional[int] = None
  pais: Optional[str] = None
  ciudad: Optional[str] = None
  ingreso_mensual: Optional[float] = None
  tipo_ingreso: Optional[str] = None
  meta_principal: Optional[str] = None
  plazo_meta: Optional[str] = None
  monto_objetivo_meta: Optional[float] = None
  nivel_conocimiento_financiero: Optional[int] = None
  tolerancia_riesgo: Optional[str] = None
  areas_interes: Optional[str] = None
  tono_comunicacion: Optional[str] = None
  idioma: Optional[str] = None
  notificaciones_diarias: Optional[bool] = None
  horario_preferido_notif: Optional[str] = None
  canal_notif_preferido: Optional[str] = None


# --- Esquema para Lectura (respuesta de la API) ---
class PerfilUsuario(BaseSchema):
  id_perfil: int
  id_usuario: int
  nombre_completo: Optional[str] = None
  edad: Optional[int] = None
  pais: Optional[str] = None
  ciudad: Optional[str] = None
  ingreso_mensual: Optional[float] = None
  tipo_ingreso: Optional[str] = None
  meta_principal: Optional[str] = None
  plazo_meta: Optional[str] = None
  monto_objetivo_meta: Optional[float] = None
  nivel_conocimiento_financiero: Optional[int] = None
  tolerancia_riesgo: Optional[str] = None
  areas_interes: Optional[str] = None
  tono_comunicacion: Optional[str] = None
  idioma: Optional[str] = None
  notificaciones_diarias: Optional[bool] = None
  horario_preferido_notif: Optional[str] = None
  canal_notif_preferido: Optional[str] = None
  fecha_creacion: datetime
  ultima_actualizacion: datetime

  class Config:
    from_attributes = True
