from api.auth.hashing import verify_password
from api.auth.token import create_access_token
from api.database import get_db
from api.models.usuario import Usuario
from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from fastapi import status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

router = APIRouter(prefix="/auth", tags=["Autenticación"])


@router.post("/login")
def login(request: OAuth2PasswordRequestForm = Depends(),
          db: Session = Depends(get_db)):
  user = db.query(Usuario).filter(Usuario.email == request.username).first()
  if not user:
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                        detail="Credenciales inválidas")

  if not verify_password(request.password, user.password_hash):
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                        detail="Credenciales inválidas")

  access_token = create_access_token(data={"sub": str(user.id_usuario)})

  return {"access_token": access_token, "token_type": "bearer"}
