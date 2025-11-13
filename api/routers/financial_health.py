"""
Financial Health Routers for MoneyPilot API.
Provides modular GET endpoints for financial health features.
"""
from datetime import datetime
from datetime import timezone
from typing import Optional

from api.auth.token import get_user_id_from_token
from api.database import get_db
from api.models.evento_financiero import EventoFinanciero
from api.models.perfil import PerfilUsuario
from api.schemas.financial_health import FinancialHealthMetrics
from api.schemas.financial_health import FinancialHealthProjection
from api.schemas.financial_health import FinancialHealthRecommendations
from api.schemas.financial_health import FinancialHealthScore
from api.schemas.financial_health import FinancialHealthSummary
from api.schemas.financial_health import RecommendationItem
from api.services.financial_health_service import analyze_financial_metrics
from api.services.financial_health_service import build_summary
from api.services.financial_health_service import calculate_health_score
from api.services.financial_health_service import generate_recommendations
from api.services.financial_health_service import project_savings
from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from fastapi import Query
from fastapi import status
from sqlalchemy.orm import Session

router = APIRouter(prefix="/financial_health", tags=["Financial Health"])


@router.get("/score",
            response_model=FinancialHealthScore,
            status_code=status.HTTP_200_OK)
def obtener_score(db: Session = Depends(get_db),
                  token_user_id: int | None = Depends(get_user_id_from_token),
                  id_usuario: int | None = None):
  """Devuelve el puntaje y estado de salud financiera del usuario."""
  user_id = id_usuario or token_user_id
  if not user_id:
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                        detail="No autorizado o token inválido.")

  profile = db.query(PerfilUsuario).filter(
      PerfilUsuario.id_usuario == user_id).first()
  if not profile:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                        detail="Perfil no encontrado.")

  transactions = db.query(EventoFinanciero).filter(
      EventoFinanciero.id_usuario == user_id).all()
  metrics = analyze_financial_metrics(profile, transactions)
  score = calculate_health_score(metrics)

  return FinancialHealthScore(
      score=score,
      status=("Excelente" if score >= 80 else "Buena" if score >= 60 else
              "Regular" if score >= 40 else "Necesita Atención"),
      calculated_at=datetime.now(timezone.utc))


@router.get("/metrics",
            response_model=FinancialHealthMetrics,
            status_code=status.HTTP_200_OK)
def obtener_metrics(db: Session = Depends(get_db),
                    token_user_id: int | None = Depends(get_user_id_from_token),
                    id_usuario: int | None = None):
  """Devuelve las métricas básicas de salud financiera del usuario."""
  user_id = id_usuario or token_user_id
  if not user_id:
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                        detail="No autorizado o token inválido.")

  profile = db.query(PerfilUsuario).filter(
      PerfilUsuario.id_usuario == user_id).first()
  if not profile:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                        detail="Perfil no encontrado.")

  transactions = db.query(EventoFinanciero).filter(
      EventoFinanciero.id_usuario == user_id).all()
  metrics = analyze_financial_metrics(profile, transactions)

  return FinancialHealthMetrics(**metrics)


@router.get("/projection",
            response_model=FinancialHealthProjection,
            status_code=status.HTTP_200_OK)
def obtener_projection(
    db: Session = Depends(get_db),
    token_user_id: int | None = Depends(get_user_id_from_token),
    id_usuario: int | None = None):
  """Devuelve la proyección de ahorros del usuario a 24 meses."""
  user_id = id_usuario or token_user_id
  if not user_id:
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                        detail="No autorizado o token inválido.")

  profile = db.query(PerfilUsuario).filter(
      PerfilUsuario.id_usuario == user_id).first()
  if not profile:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                        detail="Perfil no encontrado.")

  projection_data = project_savings(profile)

  return FinancialHealthProjection(**projection_data)


@router.get("/recommendations",
            response_model=FinancialHealthRecommendations,
            status_code=status.HTTP_200_OK)
def obtener_recommendations(
    db: Session = Depends(get_db),
    token_user_id: int | None = Depends(get_user_id_from_token),
    id_usuario: int | None = None):
  """Devuelve recomendaciones personalizadas de salud financiera."""
  user_id = id_usuario or token_user_id
  if not user_id:
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                        detail="No autorizado o token inválido.")

  profile = db.query(PerfilUsuario).filter(
      PerfilUsuario.id_usuario == user_id).first()
  if not profile:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                        detail="Perfil no encontrado.")

  transactions = db.query(EventoFinanciero).filter(
      EventoFinanciero.id_usuario == user_id).all()
  metrics = analyze_financial_metrics(profile, transactions)
  recommendations = generate_recommendations(metrics)
  recommendation_items = [RecommendationItem(**rec) for rec in recommendations]

  return FinancialHealthRecommendations(recommendations=recommendation_items)


@router.get("/summary",
            response_model=FinancialHealthSummary,
            status_code=status.HTTP_200_OK)
def obtener_summary(db: Session = Depends(get_db),
                    token_user_id: int | None = Depends(get_user_id_from_token),
                    id_usuario: int | None = None):
  """Devuelve el resumen completo de salud financiera del usuario."""
  user_id = id_usuario or token_user_id
  if not user_id:
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                        detail="No autorizado o token inválido.")

  profile = db.query(PerfilUsuario).filter(
      PerfilUsuario.id_usuario == user_id).first()
  if not profile:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                        detail="Perfil no encontrado.")

  transactions = db.query(EventoFinanciero).filter(
      EventoFinanciero.id_usuario == user_id).all()
  summary_data = build_summary(profile, transactions)

  # Convert recommendation dictionaries to RecommendationItem objects
  recommendation_items = [
      RecommendationItem(**rec)
      for rec in summary_data["recommendations"]["recommendations"]
  ]

  return FinancialHealthSummary(
      score=FinancialHealthScore(
          score=summary_data["score"]["score"],
          status=summary_data["score"]["status"],
          calculated_at=summary_data["score"]["calculated_at"]),
      metrics=FinancialHealthMetrics(**summary_data["metrics"]),
      projection=FinancialHealthProjection(**summary_data["projection"]),
      recommendations=FinancialHealthRecommendations(
          recommendations=recommendation_items))
