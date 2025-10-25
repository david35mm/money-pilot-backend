import calendar
from datetime import date

from sqlalchemy import Boolean
from sqlalchemy import CheckConstraint
from sqlalchemy import Column
from sqlalchemy import Date
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import Numeric
from sqlalchemy import String
from sqlalchemy import Text
from sqlalchemy.orm import relationship

from .base import Base
from .catalogo import CategoriaGasto
from .catalogo import CategoriaIngreso
from .catalogo import FuenteIngreso
from .usuario import Usuario


def get_start_of_week(input_date: date):
  """Calcula la fecha del lunes de la semana a la que pertenece input_date."""
  # weekday(): 0 es lunes, 6 es domingo
  days_since_monday = input_date.weekday()
  start_of_week = input_date - timedelta(days=days_since_monday)
  return start_of_week


class EventoFinanciero(Base):
  __tablename__ = 'eventos_financieros'

  id_evento = Column(Integer, primary_key=True, index=True)
  id_usuario = Column(Integer,
                      ForeignKey("usuarios.id_usuario"),
                      nullable=False)
  tipo = Column(String(10), nullable=False)  # 'ingreso' o 'gasto'
  # FK condicional: una transacción es de gasto O de ingreso
  id_categoria_gasto = Column(
      Integer,
      ForeignKey("categorias_gastos.id_categoria_gasto"),
      nullable=True)
  id_categoria_ingreso = Column(
      Integer,
      ForeignKey("categorias_ingresos.id_categoria_ingreso"),
      nullable=True)
  id_fuente_ingreso = Column(Integer,
                             ForeignKey("fuentes_ingreso.id_fuente_ingreso"),
                             nullable=True)  # Solo para ingresos
  monto = Column(Numeric(12, 2), nullable=False)
  fecha = Column(Date, nullable=False)
  descripcion = Column(Text, nullable=True)
  es_unico = Column(Boolean, default=False)  # Para US1.3
  # Campo para agrupar eventos por semana
  semana_inicio = Column(Date, nullable=True)  # Fecha del lunes de la semana

  # Relaciones
  usuario = relationship("Usuario", back_populates="eventos")
  categoria_gasto = relationship("CategoriaGasto")
  categoria_ingreso = relationship("CategoriaIngreso")
  fuente_ingreso = relationship("FuenteIngreso")

  # Restricción CHECK para asegurar que solo una categoría esté presente según el tipo
  __table_args__ = (CheckConstraint(
      "(tipo = 'gasto' AND id_categoria_gasto IS NOT NULL AND id_categoria_ingreso IS NULL) OR "
      "(tipo = 'ingreso' AND id_categoria_ingreso IS NOT NULL AND id_categoria_gasto IS NULL)",
      name="chk_categoria_tipo"),)

  def __init__(self, **kwargs):
    """Sobrescribe __init__ para calcular semana_inicio al insertar."""
    super().__init__(**kwargs)
    if self.fecha:
      self.semana_inicio = get_start_of_week(self.fecha)


# Añadir la relación inversa al modelo Usuario
Usuario.eventos = relationship("EventoFinanciero",
                               back_populates="usuario",
                               cascade="all, delete-orphan")
