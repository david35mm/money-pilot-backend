"""
Financial health schemas for MoneyPilot API.
All monetary values in COP (Colombian Peso), time periods in months/years.
"""
from datetime import datetime
from typing import List, Literal

from pydantic import BaseModel


class FinancialHealthScore(BaseModel):
  score: int
  status: str  # e.g. "Excelente", "Buena", etc.
  calculated_at: datetime

  model_config = {"from_attributes": True}


class FuenteIngreso(BaseModel):
  name: str
  amount: float


class FinancialHealthMetrics(BaseModel):
  ingreso_mensual: float
  gastos_fijos_mensuales: float
  gastos_variables_mensuales: float
  ahorro_actual: float
  ahorro_planificado_mensual: float
  deuda_total: float
  porcentaje_ahorro: float
  porcentaje_gastos: float
  ratio_deuda: float
  meses_emergencia: float
  fuentes_ingreso: List[FuenteIngreso]  # {"name": str, "amount": float}

  model_config = {"from_attributes": True}


class ProjectionItem(BaseModel):
  mes_index: int
  ahorro_acumulado: float
  meta: float

  model_config = {"from_attributes": True}


class FinancialHealthProjection(BaseModel):
  proyeccion: List[ProjectionItem]
  meses_para_meta: int

  model_config = {"from_attributes": True}


class RecommendationItem(BaseModel):
  category: str
  message: str
  priority: Literal["low", "medium", "high"]

  model_config = {"from_attributes": True}


class FinancialHealthRecommendations(BaseModel):
  recommendations: List[RecommendationItem]

  model_config = {"from_attributes": True}


class FinancialHealthSummary(BaseModel):
  score: FinancialHealthScore
  metrics: FinancialHealthMetrics
  projection: FinancialHealthProjection
  recommendations: FinancialHealthRecommendations

  model_config = {"from_attributes": True}
