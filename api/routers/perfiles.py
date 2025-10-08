from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from fastapi import status
from sqlalchemy.orm import Session

from api import database
from api.dependencies import get_current_user  # Asumiendo que esta función devuelve el usuario autenticado
from api.models.perfil import PerfilUsuario
from api.models.usuario import Usuario
from api.schemas.perfil import PerfilUsuario as PerfilUsuarioSchema
from api.schemas.perfil import PerfilUsuarioCreate
from api.schemas.perfil import PerfilUsuarioUpdate

router = APIRouter()


# POST /perfiles - Crear perfil para el usuario actual (US1.2)
@router.post("/perfiles",
             response_model=PerfilUsuarioSchema,
             status_code=status.HTTP_201_CREATED)
def create_perfil(perfil_data: PerfilUsuarioCreate,
                  db: Session = Depends(database.get_db),
                  current_user: Usuario = Depends(get_current_user)):
  # Verificar si ya existe un perfil para este usuario
  existing_profile = db.query(PerfilUsuario).filter(
      PerfilUsuario.id_usuario == current_user.id_usuario).first()
  if existing_profile:
    raise HTTPException(
        status_code=400,
        detail=
        "El perfil para este usuario ya existe. Use PUT para actualizarlo.")

  # Verificar que el ID del usuario en el payload coincida con el del token
  if perfil_data.id_usuario != current_user.id_usuario:
    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="No autorizado para crear perfil para otro usuario.")

  # Crear nuevo perfil
  nuevo_perfil = PerfilUsuario(**perfil_data.model_dump())
  db.add(nuevo_perfil)
  db.commit()
  db.refresh(nuevo_perfil)

  return nuevo_perfil


# GET /perfiles - Obtener perfil del usuario actual
@router.get("/perfiles", response_model=PerfilUsuarioSchema)
def get_perfil(db: Session = Depends(database.get_db),
               current_user: Usuario = Depends(get_current_user)):
  perfil = db.query(PerfilUsuario).filter(
      PerfilUsuario.id_usuario == current_user.id_usuario).first()
  if not perfil:
    raise HTTPException(status_code=404, detail="Perfil no encontrado")
  return perfil


# PUT /perfiles - Actualizar perfil del usuario actual
@router.put("/perfiles", response_model=PerfilUsuarioSchema)
def update_perfil(perfil_data: PerfilUsuarioUpdate,
                  db: Session = Depends(database.get_db),
                  current_user: Usuario = Depends(get_current_user)):
  perfil = db.query(PerfilUsuario).filter(
      PerfilUsuario.id_usuario == current_user.id_usuario).first()
  if not perfil:
    raise HTTPException(status_code=404, detail="Perfil no encontrado")

  # Actualizar solo los campos proporcionados
  for var, value in perfil_data.model_dump(exclude_unset=True).items():
    setattr(perfil, var, value)

  db.commit()
  db.refresh(perfil)
  return perfil


# No se incluye DELETE para el perfil, ya que generalmente no se borra, solo se actualiza o se desactiva el usuario.
