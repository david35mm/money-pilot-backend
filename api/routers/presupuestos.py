from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from fastapi import status
from sqlalchemy.orm import Session

from api import database
from api.dependencies import get_current_user
from api.models.presupuesto import Presupuesto
from api.models.usuario import Usuario
from api.schemas.presupuesto import Presupuesto as PresupuestoSchema
from api.schemas.presupuesto import PresupuestoCreate
from api.schemas.presupuesto import PresupuestoUpdate

router = APIRouter()


@router.post("/",
             response_model=PresupuestoSchema,
             status_code=status.HTTP_201_CREATED)
def create_presupuesto(presupuesto_data: PresupuestoCreate,
                       db: Session = Depends(database.get_db),
                       current_user: Usuario = Depends(get_current_user)):
  # Verificar que el ID del usuario en el payload coincida con el del token
  if presupuesto_data.id_usuario != current_user.id_usuario:
    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="No autorizado para crear presupuesto para otro usuario.")

  nuevo_presupuesto = Presupuesto(**presupuesto_data.model_dump())
  db.add(nuevo_presupuesto)
  db.commit()
  db.refresh(nuevo_presupuesto)
  return nuevo_presupuesto


@router.get("/{presupuesto_id}", response_model=PresupuestoSchema)
def get_presupuesto(presupuesto_id: int,
                    db: Session = Depends(database.get_db),
                    current_user: Usuario = Depends(get_current_user)):
  presupuesto = db.query(Presupuesto).filter(
      Presupuesto.id_presupuesto == presupuesto_id,
      Presupuesto.id_usuario == current_user.id_usuario).first()
  if not presupuesto:
    raise HTTPException(status_code=404,
                        detail="Presupuesto no encontrado o no autorizado")
  return presupuesto


@router.get("/", response_model=list[PresupuestoSchema])
def get_presupuestos(skip: int = 0,
                     limit: int = 100,
                     db: Session = Depends(database.get_db),
                     current_user: Usuario = Depends(get_current_user)):
  presupuestos = db.query(Presupuesto).filter(
      Presupuesto.id_usuario == current_user.id_usuario).offset(skip).limit(
          limit).all()
  return presupuestos


@router.put("/{presupuesto_id}", response_model=PresupuestoSchema)
def update_presupuesto(presupuesto_id: int,
                       presupuesto_data: PresupuestoUpdate,
                       db: Session = Depends(database.get_db),
                       current_user: Usuario = Depends(get_current_user)):
  presupuesto = db.query(Presupuesto).filter(
      Presupuesto.id_presupuesto == presupuesto_id,
      Presupuesto.id_usuario == current_user.id_usuario).first()
  if not presupuesto:
    raise HTTPException(status_code=404,
                        detail="Presupuesto no encontrado o no autorizado")

  # Actualizar solo los campos proporcionados
  for var, value in presupuesto_data.model_dump(exclude_unset=True).items():
    setattr(presupuesto, var, value)

  db.commit()
  db.refresh(presupuesto)
  return presupuesto


@router.delete("/{presupuesto_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_presupuesto(presupuesto_id: int,
                       db: Session = Depends(database.get_db),
                       current_user: Usuario = Depends(get_current_user)):
  presupuesto = db.query(Presupuesto).filter(
      Presupuesto.id_presupuesto == presupuesto_id,
      Presupuesto.id_usuario == current_user.id_usuario).first()
  if not presupuesto:
    raise HTTPException(status_code=404,
                        detail="Presupuesto no encontrado o no autorizado")

  db.delete(presupuesto)
  db.commit()
  return  # 204 No Content
