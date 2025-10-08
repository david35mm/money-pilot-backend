from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from fastapi import status
from sqlalchemy.orm import Session

from api import database
from api.models.categoria import Categoria
from api.schemas.categoria import Categoria as CategoriaSchema
from api.schemas.categoria import CategoriaCreate
from api.schemas.categoria import CategoriaUpdate

router = APIRouter()


@router.post("/categorias",
             response_model=CategoriaSchema,
             status_code=status.HTTP_201_CREATED)
def create_categoria(categoria_data: CategoriaCreate,
                     db: Session = Depends(database.get_db)):
  nueva_categoria = Categoria(nombre=categoria_data.nombre,
                              tipo=categoria_data.tipo)
  db.add(nueva_categoria)
  db.commit()
  db.refresh(nueva_categoria)
  return nueva_categoria


@router.get("/categorias/{categoria_id}", response_model=CategoriaSchema)
def get_categoria(categoria_id: int, db: Session = Depends(database.get_db)):
  categoria = db.query(Categoria).filter(
      Categoria.id_categoria == categoria_id).first()
  if not categoria:
    raise HTTPException(status_code=404, detail="Categoría no encontrada")
  return categoria


@router.get("/categorias", response_model=list[CategoriaSchema])
def get_categorias(skip: int = 0,
                   limit: int = 100,
                   db: Session = Depends(database.get_db)):
  categorias = db.query(Categoria).offset(skip).limit(limit).all()
  return categorias


@router.put("/categorias/{categoria_id}", response_model=CategoriaSchema)
def update_categoria(categoria_id: int,
                     categoria_data: CategoriaUpdate,
                     db: Session = Depends(database.get_db)):
  categoria = db.query(Categoria).filter(
      Categoria.id_categoria == categoria_id).first()
  if not categoria:
    raise HTTPException(status_code=404, detail="Categoría no encontrada")

  for var, value in categoria_data.model_dump(exclude_unset=True).items():
    setattr(categoria, var, value)

  db.commit()
  db.refresh(categoria)
  return categoria


@router.delete("/categorias/{categoria_id}",
               status_code=status.HTTP_204_NO_CONTENT)
def delete_categoria(categoria_id: int, db: Session = Depends(database.get_db)):
  categoria = db.query(Categoria).filter(
      Categoria.id_categoria == categoria_id).first()
  if not categoria:
    raise HTTPException(status_code=404, detail="Categoría no encontrada")

  db.delete(categoria)
  db.commit()
  return  # 204 No Content
