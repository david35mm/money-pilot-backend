from api import database
from api.dependencies import get_current_user
from api.models.usuario import Usuario
from api.services.financial_health_service import calculate_financial_health_score
from api.services.financial_health_service import get_dashboard_data
from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from fastapi import status
from sqlalchemy.orm import Session

router = APIRouter()


@router.get("/score", response_model=dict)
# Devuelve un dict con score y detalles
def get_financial_health_score_endpoint(
    db: Session = Depends(database.get_db),
    current_user: Usuario = Depends(get_current_user)):
  """Calcula y devuelve el Financial Health Score del usuario actual y detalles del cálculo."""
  result = calculate_financial_health_score(db, current_user.id_usuario)
  if result is None:
    raise HTTPException(
        status_code=404,
        detail="Perfil de usuario no encontrado para calcular el score.")

  return result  # Devuelve el diccionario completo desde el servicio


@router.get("/dashboard-data", response_model=dict)
# Devuelve un dict con todos los datos del dashboard
def get_dashboard_data_endpoint(
    db: Session = Depends(database.get_db),
    current_user: Usuario = Depends(get_current_user)):
  """Calcula y devuelve todos los datos necesarios para pintar el dashboard financiero."""
  data = get_dashboard_data(db, current_user.id_usuario)
  if data is None:
    raise HTTPException(
        status_code=404,
        detail=
        "Perfil de usuario no encontrado para calcular los datos del dashboard."
    )

  return data  # Devuelve el diccionario completo desde el servicio
