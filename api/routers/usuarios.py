from api.auth.hashing import hash_password
from api.database import get_db
from api.models.usuario import Usuario
from api.schemas.usuario import UsuarioCreate
from api.schemas.usuario import UsuarioRead
from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from fastapi import status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

router = APIRouter(prefix="/register_usuario", tags=["Usuarios"])


@router.post("/",
             response_model=UsuarioRead,
             status_code=status.HTTP_201_CREATED)
def register_usuario(data: UsuarioCreate, db: Session = Depends(get_db)):
  hashed_pwd = hash_password(data.password)
  new_user = Usuario(email=data.email, password_hash=hashed_pwd)
  db.add(new_user)
  try:
    db.commit()
    db.refresh(new_user)
    return new_user
  except IntegrityError:
    db.rollback()
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                        detail="El correo ya está registrado.")
