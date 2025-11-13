"""
Financial Health Service for MoneyPilot API.
Contains pure functions for calculating financial health metrics, scores, projections, and recommendations.
"""
from datetime import datetime
from datetime import timezone
from typing import List

from api.models.evento_financiero import EventoFinanciero
from api.models.perfil import PerfilUsuario


def analyze_financial_metrics(profile: PerfilUsuario,
                              transactions: List[EventoFinanciero]) -> dict:
  """
    Computes base financial metrics derived from the user's profile.
    """
  ingresos = profile.ingreso_mensual_estimado or 0
  gastos_fijos = profile.gastos_fijos_mensuales or 0
  gastos_variables = profile.gastos_variables_mensuales or 0
  ahorro_planificado = profile.ahorro_planificado_mensual or 0
  ahorro_actual = profile.ahorro_actual or 0
  deuda_total = profile.deuda_total or 0
  gastos_totales = gastos_fijos + gastos_variables
  disponible_mensual = ingresos - gastos_totales

  porcentaje_ahorro = (ahorro_planificado /
                       ingresos) * 100 if ingresos > 0 else 0
  porcentaje_gastos = (gastos_totales / ingresos) * 100 if ingresos > 0 else 0
  ratio_deuda = (deuda_total / ingresos) if ingresos > 0 else 0
  meses_emergencia = (ahorro_actual /
                      gastos_totales) if gastos_totales > 0 else 0

  raw_fuentes = getattr(profile, "fuentes_ingreso", [])

  fuentes_ingreso = []
  if isinstance(raw_fuentes, list):
    for item in raw_fuentes:
      if isinstance(item, dict):
        fuentes_ingreso.append(item)
      elif isinstance(item, str):
        fuentes_ingreso.append({"name": item, "amount": 0.0})

  # Validate and coerce amounts to numeric values
  for item in fuentes_ingreso:
    if "amount" in item:
      amount = item["amount"]
      if not isinstance(amount, (int, float)) or isinstance(amount, bool):
        item["amount"] = 0.0
      elif str(amount) in [
          "nan", "inf", "-inf"
      ] or (isinstance(amount, float) and
            (amount != amount or abs(amount) == float('inf'))):
        item["amount"] = 0.0
    else:
      item["amount"] = 0.0

  return {
      "ingreso_mensual": ingresos,
      "gastos_fijos_mensuales": gastos_fijos,
      "gastos_variables_mensuales": gastos_variables,
      "ahorro_actual": ahorro_actual,
      "ahorro_planificado_mensual": ahorro_planificado,
      "deuda_total": deuda_total,
      "porcentaje_ahorro": porcentaje_ahorro,
      "porcentaje_gastos": porcentaje_gastos,
      "ratio_deuda": ratio_deuda,
      "meses_emergencia": meses_emergencia,
      "disponible_mensual": disponible_mensual,
      "fuentes_ingreso": fuentes_ingreso,
  }


def calculate_health_score(metrics: dict) -> int:
  """
    Calculates the financial health score (0–100).
    """
  score = 0

  # Savings rate (30 pts)
  if metrics["porcentaje_ahorro"] >= 20:
    score += 30
  elif metrics["porcentaje_ahorro"] >= 15:
    score += 25
  elif metrics["porcentaje_ahorro"] >= 10:
    score += 20
  else:
    score += (metrics["porcentaje_ahorro"] / 10) * 20

  # Expense ratio (30 pts)
  if metrics["porcentaje_gastos"] <= 70:
    score += 30
  elif metrics["porcentaje_gastos"] <= 80:
    score += 20
  elif metrics["porcentaje_gastos"] <= 90:
    score += 10
  else:
    score += 5

  # Debt ratio (20 pts)
  if metrics["ratio_deuda"] <= 3:
    score += 20
  elif metrics["ratio_deuda"] <= 6:
    score += 15
  elif metrics["ratio_deuda"] <= 12:
    score += 10
  else:
    score += 5

  # Emergency fund (20 pts)
  meses = metrics["meses_emergencia"]
  if meses >= 6:
    score += 20
  elif meses >= 3:
    score += 15
  elif meses >= 1:
    score += 10
  else:
    score += meses * 10

  return round(score)


def project_savings(profile: PerfilUsuario) -> dict:
  """
    Returns a 24-month projection of savings progress toward the goal.
    """
  proyeccion = []
  for i in range(25):  # months 0–24
    ahorro_acumulado = (profile.ahorro_actual or 0) + (
        (profile.ahorro_planificado_mensual or 0) * i)
    proyeccion.append({
        "mes_index": i,
        "ahorro_acumulado": ahorro_acumulado,
        "meta": profile.monto_meta_ahorro or 0,
    })

  restante = (profile.monto_meta_ahorro or 0) - (profile.ahorro_actual or 0)
  meses_para_meta = int(
      restante / profile.ahorro_planificado_mensual
  ) if profile.ahorro_planificado_mensual and profile.ahorro_planificado_mensual > 0 else None

  return {"proyeccion": proyeccion, "meses_para_meta": meses_para_meta}


def generate_recommendations(metrics: dict) -> list[dict]:
  """
    Generates textual financial recommendations based on threshold conditions.
    """
  recs = []
  if metrics["porcentaje_ahorro"] < 20:
    recs.append({
        "category":
            "ahorro",
        "message":
            f"Aumenta tu tasa de ahorro ({metrics['porcentaje_ahorro']:.1f}%). Intenta llegar al 20%.",
        "priority":
            "medium"
    })
  if metrics["ratio_deuda"] > 6:
    recs.append({
        "category":
            "deuda",
        "message":
            f"Tu deuda equivale a {metrics['ratio_deuda']:.1f} meses de ingreso. Considera reducirla.",
        "priority":
            "high"
    })
  if metrics["meses_emergencia"] < 3:
    recs.append({
        "category":
            "emergencia",
        "message":
            f"Tu fondo de emergencia cubre {metrics['meses_emergencia']:.1f} meses. Ideal: 3–6.",
        "priority":
            "medium"
    })
  if metrics["porcentaje_gastos"] > 80:
    recs.append({
        "category":
            "gastos",
        "message":
            f"Estás gastando el {metrics['porcentaje_gastos']:.1f}% de tus ingresos. Reduce gastos variables.",
        "priority":
            "high"
    })
  if not recs:
    recs.append({
        "category":
            "general",
        "message":
            "Excelente equilibrio financiero. Mantén tus hábitos y evalúa diversificar tus inversiones.",
        "priority":
            "low"
    })

  # Sort recommendations by priority: high, medium, low
  priority_order = {"high": 0, "medium": 1, "low": 2}
  recs.sort(key=lambda x: priority_order[x["priority"]])

  return recs


def build_summary(profile: PerfilUsuario,
                  transactions: List[EventoFinanciero]) -> dict:
  """
    Orchestrates all previous functions and builds a dict shaped like FinancialHealthSummary.
    """
  metrics = analyze_financial_metrics(profile, transactions)
  score = calculate_health_score(metrics)
  projection = project_savings(profile)
  recommendations = generate_recommendations(metrics)

  return {
      "score": {
          "score": score,
          "status": ("Excelente" if score >= 80 else "Buena" if score >= 60 else
                     "Regular" if score >= 40 else "Necesita Atención"),
          "calculated_at": datetime.now(timezone.utc)
      },
      "metrics": metrics,
      "projection": projection,
      "recommendations": {
          "recommendations": recommendations
      }
  }
