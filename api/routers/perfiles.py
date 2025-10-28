from api.config import settings
from api.database import get_db
from api.models.perfil import PerfilUsuario
from api.models.usuario import Usuario
from api.schemas.perfil import PerfilPersonalCreate
from api.schemas.perfil import PerfilUsuarioRead
from fastapi import APIRouter
from fastapi import Depends
from fastapi import Header
from fastapi import HTTPException
from fastapi import status
from jose import jwt
from jose import JWTError
from sqlalchemy import text
from sqlalchemy.orm import Session

router = APIRouter(prefix="/perfil_personal", tags=["Perfiles"])


def get_user_id_from_token(authorization: str = Header(None)) -> int | None:
  """Extrae el id_usuario del token JWT si está presente en el header Authorization."""
  if not authorization or not authorization.startswith("Bearer "):
    return None
  token = authorization.split(" ")[1]
  try:
    payload = jwt.decode(token,
                         settings.SECRET_KEY,
                         algorithms=[settings.ALGORITHM])
    return payload.get("sub")
  except JWTError:
    return None


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


@router.get("/", response_model=dict, status_code=status.HTTP_200_OK)
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

  return {
      "nombre": perfil.nombre,
      "apellido": perfil.apellido,
      "fecha_nacimiento": perfil.fecha_nacimiento,
      "pais_residencia": pais[0] if pais else None
  }