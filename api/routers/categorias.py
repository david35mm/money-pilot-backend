from api.database import get_db
from api.models.categorias import CategoriaGasto
from api.models.categorias import CategoriaIngreso
from api.models.fuentes_ingreso import FuenteIngreso
from fastapi import APIRouter
from fastapi import Depends
from sqlalchemy.orm import Session

router = APIRouter(prefix="/categorias", tags=["Categorías"])


@router.get("/gastos")
def obtener_categorias_gastos(db: Session = Depends(get_db)):
  """Obtiene todas las categorías de gastos disponibles."""
  categorias = db.query(CategoriaGasto.nombre).all()
  return [categoria[0] for categoria in categorias]


@router.get("/ingresos")
def obtener_categorias_ingresos(db: Session = Depends(get_db)):
  """Obtiene todas las categorías de ingresos disponibles."""
  categorias = db.query(CategoriaIngreso.nombre).all()
  return [categoria[0] for categoria in categorias]


@router.get("/fuentes")
def obtener_fuentes_ingreso(db: Session = Depends(get_db)):
  """Obtiene todas las fuentes de ingreso disponibles."""
  fuentes = db.query(FuenteIngreso.nombre).all()
  return [fuente[0] for fuente in fuentes]
