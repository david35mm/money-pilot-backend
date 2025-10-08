from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from fastapi import status
from sqlalchemy.orm import Session

from api import database
from api.dependencies import get_current_user
from api.models.alerta import Alerta
from api.models.usuario import Usuario
from api.schemas.alerta import Alerta as AlertaSchema
from api.schemas.alerta import AlertaCreate
from api.schemas.alerta import AlertaUpdate

router = APIRouter()


@router.post("/alertas",
             response_model=AlertaSchema,
             status_code=status.HTTP_201_CREATED)
def create_alerta(alerta_data: AlertaCreate,
                  db: Session = Depends(database.get_db),
                  current_user: Usuario = Depends(get_current_user)):
  # Verificar que el ID del usuario en el payload coincida con el del token
  # Y que el presupuesto pertenezca al usuario
  presupuesto_usuario = db.query(Alerta.id_presupuesto).filter(
      Alerta.id_presupuesto == alerta_data.id_presupuesto,
      Alerta.id_usuario == current_user.id_usuario).first()
  if not presupuesto_usuario:
    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="No autorizado para crear alerta para este presupuesto.")

  # Asegurarse que el id_usuario de la alerta sea el del usuario actual
  alerta_data.id_usuario = current_user.id_usuario
  nueva_alerta = Alerta(**alerta_data.model_dump())
  db.add(nueva_alerta)
  db.commit()
  db.refresh(nueva_alerta)
  return nueva_alerta


@router.get("/alertas/{alerta_id}", response_model=AlertaSchema)
def get_alerta(alerta_id: int,
               db: Session = Depends(database.get_db),
               current_user: Usuario = Depends(get_current_user)):
  alerta = db.query(Alerta).filter(
      Alerta.id_alerta == alerta_id,
      Alerta.id_usuario == current_user.id_usuario).first()
  if not alerta:
    raise HTTPException(status_code=404,
                        detail="Alerta no encontrada o no autorizada")
  return alerta


@router.get("/alertas", response_model=list[AlertaSchema])
def get_alertas(skip: int = 0,
                limit: int = 100,
                db: Session = Depends(database.get_db),
                current_user: Usuario = Depends(get_current_user)):
  alertas = db.query(Alerta).filter(Alerta.id_usuario == current_user.id_usuario
                                   ).offset(skip).limit(limit).all()
  return alertas


@router.put("/alertas/{alerta_id}", response_model=AlertaSchema)
def update_alerta(alerta_id: int,
                  alerta_data: AlertaUpdate,
                  db: Session = Depends(database.get_db),
                  current_user: Usuario = Depends(get_current_user)):
  alerta = db.query(Alerta).filter(
      Alerta.id_alerta == alerta_id,
      Alerta.id_usuario == current_user.id_usuario).first()
  if not alerta:
    raise HTTPException(status_code=404,
                        detail="Alerta no encontrada o no autorizada")

  # Actualizar solo los campos proporcionados
  for var, value in alerta_data.model_dump(exclude_unset=True).items():
    setattr(alerta, var, value)

  db.commit()
  db.refresh(alerta)
  return alerta


@router.delete("/alertas/{alerta_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_alerta(alerta_id: int,
                  db: Session = Depends(database.get_db),
                  current_user: Usuario = Depends(get_current_user)):
  alerta = db.query(Alerta).filter(
      Alerta.id_alerta == alerta_id,
      Alerta.id_usuario == current_user.id_usuario).first()
  if not alerta:
    raise HTTPException(status_code=404,
                        detail="Alerta no encontrada o no autorizada")

  db.delete(alerta)
  db.commit()
  return  # 204 No Content
