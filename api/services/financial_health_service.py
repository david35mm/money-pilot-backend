from datetime import date
from datetime import timedelta
from typing import Any, Dict, List, Optional

from api.models.catalogo import CategoriaGasto
from api.models.catalogo import CategoriaIngreso
from api.models.evento import EventoFinanciero
from api.models.perfil import PerfilUsuario
from api.models.usuario import Usuario
from sqlalchemy.orm import Session


def ceil(x: float) -> int:
  """Función ceil simple si no se quiere importar math."""
  return int(-(-x // 1)) if x > 0 else int(x) - (x < int(x))


def calculate_financial_health_score(db: Session,
                                     user_id: int) -> Optional[dict]:
  """
    Calcula el Financial Health Score (0-100) y otros datos relevantes
    para un usuario específico, replicando la lógica del frontend.
    Devuelve un diccionario con el score y los detalles de cálculo.
    """
  perfil = db.query(PerfilUsuario).filter(
      PerfilUsuario.id_usuario == user_id).first()
  if not perfil:
    return None  # Usuario no tiene perfil

  # Extraer datos del perfil (equivalentes a userData.datos_financieros.perfil_financiero)
  ingreso_mensual_estimado = perfil.ingreso_mensual_estimado or 0
  gastos_fijos_mensuales = perfil.gastos_fijos_mensuales or 0
  gastos_variables_mensuales = perfil.gastos_variables_mensuales or 0
  ahorro_actual = perfil.ahorro_actual or 0
  deuda_total = perfil.deuda_total or 0
  monto_meta_ahorro = perfil.monto_meta_ahorro or 0
  plazo_meta_ahorro_meses = perfil.plazo_meta_ahorro_meses or 0  # Asumiendo que este campo existe
  ahorro_planificado_mensual = perfil.ahorro_planificado_mensual or 0

  # Cálculos de salud financiera (replicando el frontend)
  gastos_totales = gastos_fijos_mensuales + gastos_variables_mensuales
  disponible_mensual = ingreso_mensual_estimado - gastos_totales

  # Asegurarse de no dividir por cero
  porcentaje_ahorro = (ahorro_planificado_mensual / ingreso_mensual_estimado *
                       100) if ingreso_mensual_estimado > 0 else 0
  porcentaje_gastos = (gastos_totales / ingreso_mensual_estimado *
                       100) if ingreso_mensual_estimado > 0 else 0
  ratio_deuda = (
      deuda_total /
      ingreso_mensual_estimado) if ingreso_mensual_estimado > 0 else 0

  # Calcular meses para alcanzar la meta
  meses_para_meta = 0
  if ahorro_planificado_mensual > 0:
    diferencia_meta = max(0, monto_meta_ahorro - ahorro_actual)
    meses_para_meta = ceil(diferencia_meta / ahorro_planificado_mensual)
  else:
    meses_para_meta = float(
        'inf')  # o un valor que indique que no se puede alcanzar

  # Score de salud financiera (0-100) (replicando el frontend)
  score = 0.0

  # 30 puntos: Tasa de ahorro (ideal >20%)
  if porcentaje_ahorro >= 20:
    score += 30
  elif porcentaje_ahorro >= 15:
    score += 25
  elif porcentaje_ahorro >= 10:
    score += 20
  else:
    score += (porcentaje_ahorro / 10) * 20

  # 30 puntos: Gastos vs ingresos (ideal <70%)
  if porcentaje_gastos <= 70:
    score += 30
  elif porcentaje_gastos <= 80:
    score += 20
  elif porcentaje_gastos <= 90:
    score += 10
  else:
    score += 5

  # 20 puntos: Ratio de deuda (ideal <3 meses de ingreso)
  # (La lógica del frontend usa ratio_deuda = deuda_total / ingreso_mensual)
  # y compara contra 3, 6, 12. Esto parece estar midiendo deuda en términos de "meses de ingreso".
  # Asumiremos que la comparación es directa con el ratio calculado.
  if ratio_deuda <= 3:
    score += 20
  elif ratio_deuda <= 6:
    score += 15
  elif ratio_deuda <= 12:
    score += 10
  else:
    score += 5

  # 20 puntos: Fondo de emergencia (ideal 3-6 meses de gastos)
  meses_emergencia = (ahorro_actual /
                      gastos_totales) if gastos_totales > 0 else 0
  if meses_emergencia >= 6:
    score += 20
  elif meses_emergencia >= 3:
    score += 15
  elif meses_emergencia >= 1:
    score += 10
  else:
    score += (meses_emergencia * 10)

  # Asegurarse de que el score esté entre 0 y 100
  score = max(0, min(100, score))

  return {
      "financial_health_score": round(score),
      "details": {
          "gastos_totales": gastos_totales,
          "disponible_mensual": disponible_mensual,
          "porcentaje_ahorro": round(porcentaje_ahorro, 2),
          "porcentaje_gastos": round(porcentaje_gastos, 2),
          "ratio_deuda": round(ratio_deuda, 2),
          "meses_para_meta": meses_para_meta,
          "meses_fondo_emergencia": round(meses_emergencia, 2)
      }
  }


def get_dashboard_data(db: Session, user_id: int) -> Optional[Dict[str, Any]]:
  """
    Calcula todos los datos necesarios para pintar el dashboard financiero,
    replicando la lógica del frontend.
    """
  perfil = db.query(PerfilUsuario).filter(
      PerfilUsuario.id_usuario == user_id).first()
  if not perfil:
    return None  # Usuario no tiene perfil

  # Extraer datos del perfil
  ingreso_mensual_estimado = perfil.ingreso_mensual_estimado or 0
  gastos_fijos_mensuales = perfil.gastos_fijos_mensuales or 0
  gastos_variables_mensuales = perfil.gastos_variables_mensuales or 0
  ahorro_actual = perfil.ahorro_actual or 0
  deuda_total = perfil.deuda_total or 0
  monto_meta_ahorro = perfil.monto_meta_ahorro or 0
  plazo_meta_ahorro_meses = perfil.plazo_meta_ahorro_meses or 0
  ahorro_planificado_mensual = perfil.ahorro_planificado_mensual or 0

  # --- Cálculos ---
  gastos_totales = gastos_fijos_mensuales + gastos_variables_mensuales
  disponible_mensual = ingreso_mensual_estimado - gastos_totales
  porcentaje_ahorro = (ahorro_planificado_mensual / ingreso_mensual_estimado *
                       100) if ingreso_mensual_estimado > 0 else 0
  porcentaje_gastos = (gastos_totales / ingreso_mensual_estimado *
                       100) if ingreso_mensual_estimado > 0 else 0
  ratio_deuda = (
      deuda_total /
      ingreso_mensual_estimado) if ingreso_mensual_estimado > 0 else 0

  meses_para_meta = 0
  if ahorro_planificado_mensual > 0:
    diferencia_meta = max(0, monto_meta_ahorro - ahorro_actual)
    meses_para_meta = ceil(diferencia_meta / ahorro_planificado_mensual)
  else:
    meses_para_meta = float('inf')

  meses_emergencia = (ahorro_actual /
                      gastos_totales) if gastos_totales > 0 else 0

  # --- Métricas Clave ---
  key_metrics = {
      "ingreso_mensual": ingreso_mensual_estimado,
      "gastos_totales": gastos_totales,
      "porcentaje_gastos": round(porcentaje_gastos, 2),
      "ahorro_mensual": ahorro_planificado_mensual,
      "porcentaje_ahorro": round(porcentaje_ahorro, 2),
      "deuda_total": deuda_total,
      "ratio_deuda": round(ratio_deuda, 2),
      "disponible_mensual": disponible_mensual
  }

  # --- Datos para Gráficas ---
  # Distribución de Ingresos
  distribucion_ingresos = [
      {
          "name": "Gastos Fijos",
          "value": gastos_fijos_mensuales,
          "color": "#ef4444"
      },
      {
          "name": "Gastos Variables",
          "value": gastos_variables_mensuales,
          "color": "#f59e0b"
      },
      {
          "name": "Ahorro Planificado",
          "value": ahorro_planificado_mensual,
          "color": "#10b981"
      },
      {
          "name": "Disponible",
          "value": max(0, disponible_mensual - ahorro_planificado_mensual),
          "color": "#3b82f6"
      },
  ]

  # Comparación de Gastos
  comparacion_gastos = [
      {
          "categoria":
              "Gastos Fijos",
          "monto":
              gastos_fijos_mensuales,
          "porcentaje":
              round((gastos_fijos_mensuales / ingreso_mensual_estimado *
                     100) if ingreso_mensual_estimado > 0 else 0, 1)
      },
      {
          "categoria":
              "Gastos Variables",
          "monto":
              gastos_variables_mensuales,
          "porcentaje":
              round((gastos_variables_mensuales / ingreso_mensual_estimado *
                     100) if ingreso_mensual_estimado > 0 else 0, 1)
      },
  ]

  # Proyección de Ahorro (24 meses)
  proyeccion_ahorro: List[Dict[str, float]] = []
  for i in range(25):  # 0 a 24 meses
    ahorro_acumulado = ahorro_actual + (ahorro_planificado_mensual * i)
    proyeccion_ahorro.append({
        "mes": f"Mes {i}",
        "ahorro": ahorro_acumulado,
        "meta": monto_meta_ahorro
    })

  # --- Recomendaciones ---
  recomendaciones = []
  if porcentaje_ahorro < 20:
    recomendaciones.append({
        "type":
            "ahorro",
        "message":
            f"Aumenta tu tasa de ahorro: Actualmente ahorras el {porcentaje_ahorro:.1f}% de tus ingresos. Intenta llegar al 20% para mejorar tu salud financiera."
    })
  if ratio_deuda > 6:
    recomendaciones.append({
        "type":
            "deuda",
        "message":
            f"Reduce tu deuda: Tu deuda equivale a {ratio_deuda:.2f} meses de ingresos. Considera destinar más recursos a pagar deudas."
    })
  if meses_emergencia < 3:
    recomendaciones.append({
        "type":
            "fondo_emergencia",
        "message":
            f"Construye un fondo de emergencia: Tu ahorro actual cubre {meses_emergencia:.1f} meses de gastos. Lo ideal es tener entre 3-6 meses cubiertos."
    })
  if porcentaje_gastos > 80:
    recomendaciones.append({
        "type":
            "gastos",
        "message":
            f"Controla tus gastos: Estás gastando el {porcentaje_gastos:.1f}% de tus ingresos. Intenta reducir gastos variables para tener más margen financiero."
    })
  if round(
      calculate_financial_health_score(
          db, user_id)["financial_health_score"]) >= 80:
    recomendaciones.append({
        "type":
            "motivacional",
        "message":
            "¡Excelente trabajo! Tu salud financiera es muy buena. Mantén estos buenos hábitos y considera diversificar tus inversiones."
    })

  # --- Análisis de Proyección ---
  analysis_note = f"Con tu ahorro mensual de {ahorro_planificado_mensual:,.0f}, alcanzarás tu meta de {monto_meta_ahorro:,.0f} en aproximadamente {meses_para_meta} meses."
  if meses_para_meta > plazo_meta_ahorro_meses and plazo_meta_ahorro_meses > 0:
    analysis_note += f" ⚠️ Esto es {meses_para_meta - plazo_meta_ahorro_meses} meses más de lo planeado."
  elif meses_para_meta <= plazo_meta_ahorro_meses and plazo_meta_ahorro_meses > 0:
    analysis_note += " ✅ ¡Vas por buen camino para cumplir tu meta a tiempo!"

  # --- Score y Estado ---
  health_score = calculate_financial_health_score(db, user_id)
  if health_score:
    score_value = health_score["financial_health_score"]
    if score_value >= 80:
      health_status = {
          "text": "Excelente",
          "color": "text-green-600",
          "bg": "bg-green-100"
      }
    elif score_value >= 60:
      health_status = {
          "text": "Buena",
          "color": "text-blue-600",
          "bg": "bg-blue-100"
      }
    elif score_value >= 40:
      health_status = {
          "text": "Regular",
          "color": "text-yellow-600",
          "bg": "bg-yellow-100"
      }
    else:
      health_status = {
          "text": "Necesita Atención",
          "color": "text-red-600",
          "bg": "bg-red-100"
      }
  else:
    score_value = 0
    health_status = {
        "text": "No disponible",
        "color": "text-gray-600",
        "bg": "bg-gray-100"
    }

  return {
      "financial_health_score": score_value,
      "health_status": health_status,
      "key_metrics": key_metrics,
      "chart_data": {
          "distribution_income": distribucion_ingresos,
          "expense_comparison": comparacion_gastos,
          "savings_projection": proyeccion_ahorro
      },
      "recommendations": recomendaciones,
      "analysis_note": analysis_note
  }
