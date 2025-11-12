from api.auth.token import get_user_id_from_token
from api.database import get_db
from api.models.perfil import PerfilUsuario
from api.models.usuario import Usuario
from api.schemas.perfil import PerfilFinancieroCreate
from api.schemas.perfil import PerfilFinancieroRead
from api.schemas.perfil import PerfilPersonalCreate
from api.schemas.perfil import PerfilPersonalRead
from api.schemas.perfil import PerfilUsuarioRead
from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from fastapi import status
from sqlalchemy import text
from sqlalchemy.orm import Session

router = APIRouter(prefix="/perfil_personal", tags=["Perfiles"])


@router.post("/",
             response_model=PerfilUsuarioRead,
             status_code=status.HTTP_201_CREATED)
def crear_perfil_personal(data: PerfilPersonalCreate,
                          db: Session = Depends(get_db),
                          token_user_id: int |
                          None = Depends(get_user_id_from_token),
                          id_usuario: int | None = None):
  """Crea o actualiza la información personal básica del usuario.
    Si no se proporciona id_usuario, se toma del token JWT.
    """

  user_id = id_usuario or token_user_id
  if not user_id:
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                        detail="No autorizado o token inválido.")

  user = db.query(Usuario).filter(Usuario.id_usuario == user_id).first()
  if not user:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                        detail="Usuario no encontrado.")

  perfil = db.query(PerfilUsuario).filter(
      PerfilUsuario.id_usuario == user_id).first()

  pais = db.execute(
      text("SELECT id_pais FROM paises_latam WHERE codigo = :codigo"), {
          "codigo": data.codigo_pais
      }).fetchone()
  id_pais = pais[0] if pais else None

  if perfil:
    perfil.nombre = data.nombre
    perfil.apellido = data.apellido
    perfil.fecha_nacimiento = data.fecha_nacimiento
    perfil.id_pais_residencia = id_pais
    perfil.acepta_terminos = data.acepta_terminos
  else:
    perfil = PerfilUsuario(id_usuario=user_id,
                           nombre=data.nombre,
                           apellido=data.apellido,
                           fecha_nacimiento=data.fecha_nacimiento,
                           id_pais_residencia=id_pais,
                           acepta_terminos=data.acepta_terminos)
    db.add(perfil)

  db.commit()
  db.refresh(perfil)
  return perfil


@router.get("/",
            response_model=PerfilPersonalRead,
            status_code=status.HTTP_200_OK)
def obtener_perfil_personal(
    db: Session = Depends(get_db),
    token_user_id: int | None = Depends(get_user_id_from_token),
    id_usuario: int | None = None):
  """Obtiene la información personal de un usuario (sin acepta_terminos).
    Si no se proporciona id_usuario, se toma del token JWT.
    """

  user_id = id_usuario or token_user_id
  if not user_id:
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                        detail="No autorizado o token inválido.")

  user = db.query(Usuario).filter(Usuario.id_usuario == user_id).first()
  if not user:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                        detail="Usuario no encontrado.")

  perfil = db.query(PerfilUsuario).filter(
      PerfilUsuario.id_usuario == user.id_usuario).first()
  if not perfil:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                        detail="Perfil no encontrado.")

  pais = db.execute(
      text("SELECT nombre FROM paises_latam WHERE id_pais = :id_pais"), {
          "id_pais": perfil.id_pais_residencia
      }).fetchone()

  return PerfilPersonalRead(nombre=perfil.nombre,
                            apellido=perfil.apellido,
                            fecha_nacimiento=perfil.fecha_nacimiento,
                            pais_residencia=pais[0] if pais else None)


@router.post("/financiero",
             response_model=PerfilUsuarioRead,
             status_code=status.HTTP_201_CREATED)
def crear_o_actualizar_perfil_financiero(data: PerfilFinancieroCreate,
                                         db: Session = Depends(get_db),
                                         token_user_id: int |
                                         None = Depends(get_user_id_from_token),
                                         id_usuario: int | None = None):
  """Crea o actualiza la información financiera del usuario."""

  user_id = id_usuario or token_user_id
  if not user_id:
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                        detail="No autorizado o token inválido.")

  user = db.query(Usuario).filter(Usuario.id_usuario == user_id).first()
  if not user:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                        detail="Usuario no encontrado.")

  perfil = db.query(PerfilUsuario).filter(
      PerfilUsuario.id_usuario == user_id).first()

  if not perfil:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                        detail="Debe crear primero el perfil personal.")

  perfil.ingreso_mensual_estimado = data.ingreso_mensual_estimado
  perfil.fuentes_ingreso = data.fuentes_ingreso
  perfil.gastos_fijos_mensuales = data.gastos_fijos_mensuales
  perfil.gastos_variables_mensuales = data.gastos_variables_mensuales
  perfil.ahorro_actual = data.ahorro_actual
  perfil.deuda_total = data.deuda_total
  perfil.monto_meta_ahorro = data.meta_ahorro.monto
  perfil.plazo_meta_ahorro_meses = data.meta_ahorro.plazo_meses
  perfil.ahorro_planificado_mensual = data.ahorro_planificado_mensual

  db.commit()
  db.refresh(perfil)
  return perfil


@router.get("/financiero",
            response_model=PerfilFinancieroRead,
            status_code=status.HTTP_200_OK)
def obtener_perfil_financiero(
    db: Session = Depends(get_db),
    token_user_id: int | None = Depends(get_user_id_from_token),
    id_usuario: int | None = None):
  """Obtiene la información financiera del usuario."""

  user_id = id_usuario or token_user_id
  if not user_id:
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                        detail="No autorizado o token inválido.")

  user = db.query(Usuario).filter(Usuario.id_usuario == user_id).first()
  if not user:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                        detail="Usuario no encontrado.")

  perfil = db.query(PerfilUsuario).filter(
      PerfilUsuario.id_usuario == user_id).first()
  if not perfil:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                        detail="Perfil financiero no encontrado.")

  return PerfilFinancieroRead(
      ingreso_mensual_estimado=perfil.ingreso_mensual_estimado,
      fuentes_ingreso=perfil.fuentes_ingreso,
      gastos_fijos_mensuales=perfil.gastos_fijos_mensuales,
      gastos_variables_mensuales=perfil.gastos_variables_mensuales,
      ahorro_actual=perfil.ahorro_actual,
      deuda_total=perfil.deuda_total,
      monto_meta_ahorro=perfil.monto_meta_ahorro,
      plazo_meta_ahorro_meses=perfil.plazo_meta_ahorro_meses,
      ahorro_planificado_mensual=perfil.ahorro_planificado_mensual,
  )
