from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from fastapi import status
from sqlalchemy.orm import Session

from api import database
from api.dependencies import get_current_user
from api.models.usuario import Usuario
from api.schemas.usuario import Usuario as UsuarioSchema
from api.schemas.usuario import UsuarioUpdate

router = APIRouter()


# GET /usuarios/me - Obtener información del usuario actual
@router.get("/usuarios/me", response_model=UsuarioSchema)
def get_current_user_profile(current_user: Usuario = Depends(get_current_user)):
  return current_user


# PUT /usuarios/me - Actualizar información del usuario actual
@router.put("/usuarios/me", response_model=UsuarioSchema)
def update_current_user_profile(
    usuario_data: UsuarioUpdate,
    db: Session = Depends(database.get_db),
    current_user: Usuario = Depends(get_current_user)):
  # Actualizar solo los campos proporcionados
  for var, value in usuario_data.model_dump(exclude_unset=True).items():
    setattr(current_user, var, value)

  db.commit()
  db.refresh(current_user)
  return current_user


# DELETE /usuarios/me - (Opcional y delicado) Eliminar la cuenta del usuario actual
# No se implementa aquí por razones de seguridad y complejidad (cascadas, etc.).
# Se podría marcar como inactivo o usar un endpoint separado con confirmación.
