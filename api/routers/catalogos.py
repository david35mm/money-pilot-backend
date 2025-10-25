from api import database
from api.models.catalogo import CategoriaGasto
from api.models.catalogo import CategoriaIngreso
from api.models.catalogo import FuenteIngreso
from api.models.catalogo import PaisLatam
from api.schemas.catalogo import CatalogosResponseSchema
from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from fastapi import status
from sqlalchemy.orm import Session

# from api.dependencies import get_current_user # Opcional: si se requiere autenticación

router = APIRouter()


@router.get("/catalogos", response_model=CatalogosResponseSchema)
def get_catalogos(db: Session = Depends(
    database.get_db)):  # , current_user: Usuario = Depends(get_current_user)):
  """Obtiene los catálogos de datos para el frontend."""
  # Obtener las categorías de gastos
  categorias_gastos = db.query(CategoriaGasto).order_by(
      CategoriaGasto.id_categoria_gasto).all()
  # Obtener las categorías de ingresos
  categorias_ingresos = db.query(CategoriaIngreso).order_by(
      CategoriaIngreso.id_categoria_ingreso).all()
  # Obtener las fuentes de ingreso
  fuentes_ingreso = db.query(FuenteIngreso).order_by(
      FuenteIngreso.id_fuente_ingreso).all()
  # Obtener los países de Latinoamérica
  paises_latam = db.query(PaisLatam).order_by(PaisLatam.id_pais).all()

  # Devolver la respuesta en el formato esperado por el frontend
  return {
      "categoriasGastos": categorias_gastos,
      "categoriasIngresos": categorias_ingresos,
      "fuentesIngreso": fuentes_ingreso,
      "paisesLatam": paises_latam
  }
