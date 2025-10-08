from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from fastapi import status
from sqlalchemy.orm import Session

from api import database
from api.dependencies import get_current_user
from api.models.transaccion import Transaccion
from api.models.usuario import Usuario
from api.schemas.transaccion import Transaccion as TransaccionSchema
from api.schemas.transaccion import TransaccionCreate
from api.schemas.transaccion import TransaccionUpdate

router = APIRouter()


@router.post("/",
             response_model=TransaccionSchema,
             status_code=status.HTTP_201_CREATED)
def create_transaccion(transaccion_data: TransaccionCreate,
                       db: Session = Depends(database.get_db),
                       current_user: Usuario = Depends(get_current_user)):
  # Verificar que el ID del usuario en el payload coincida con el del token
  if transaccion_data.id_usuario != current_user.id_usuario:
    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="No autorizado para crear transacción para otro usuario.")

  nueva_transaccion = Transaccion(**transaccion_data.model_dump())
  db.add(nueva_transaccion)
  db.commit()
  db.refresh(nueva_transaccion)
  return nueva_transaccion


@router.get("/{transaccion_id}", response_model=TransaccionSchema)
def get_transaccion(transaccion_id: int,
                    db: Session = Depends(database.get_db),
                    current_user: Usuario = Depends(get_current_user)):
  transaccion = db.query(Transaccion).filter(
      Transaccion.id_transaccion == transaccion_id,
      Transaccion.id_usuario == current_user.id_usuario).first()
  if not transaccion:
    raise HTTPException(status_code=404,
                        detail="Transacción no encontrada o no autorizada")
  return transaccion


@router.get("/", response_model=list[TransaccionSchema])
def get_transacciones(skip: int = 0,
                      limit: int = 100,
                      db: Session = Depends(database.get_db),
                      current_user: Usuario = Depends(get_current_user)):
  transacciones = db.query(Transaccion).filter(
      Transaccion.id_usuario == current_user.id_usuario).offset(skip).limit(
          limit).all()
  return transacciones


@router.put("/{transaccion_id}", response_model=TransaccionSchema)
def update_transaccion(transaccion_id: int,
                       transaccion_data: TransaccionUpdate,
                       db: Session = Depends(database.get_db),
                       current_user: Usuario = Depends(get_current_user)):
  transaccion = db.query(Transaccion).filter(
      Transaccion.id_transaccion == transaccion_id,
      Transaccion.id_usuario == current_user.id_usuario).first()
  if not transaccion:
    raise HTTPException(status_code=404,
                        detail="Transacción no encontrada o no autorizada")

  # Actualizar solo los campos proporcionados
  for var, value in transaccion_data.model_dump(exclude_unset=True).items():
    setattr(transaccion, var, value)

  db.commit()
  db.refresh(transaccion)
  return transaccion


@router.delete("/{transaccion_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_transaccion(transaccion_id: int,
                       db: Session = Depends(database.get_db),
                       current_user: Usuario = Depends(get_current_user)):
  transaccion = db.query(Transaccion).filter(
      Transaccion.id_transaccion == transaccion_id,
      Transaccion.id_usuario == current_user.id_usuario).first()
  if not transaccion:
    raise HTTPException(status_code=404,
                        detail="Transacción no encontrada o no autorizada")

  db.delete(transaccion)
  db.commit()
  return  # 204 No Content
