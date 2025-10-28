from datetime import datetime
from datetime import timedelta
from datetime import timezone
from typing import Optional

from api import config
from api.database import get_db
from api.models.usuario import Usuario
from fastapi import Depends
from fastapi import HTTPException
from fastapi import status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt
from jose import JWTError
from sqlalchemy.orm import Session

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
  """Crea un token JWT de acceso."""
  to_encode = data.copy()
  if expires_delta:
    expire = datetime.now(timezone.utc) + expires_delta
  else:
    expire = datetime.now(timezone.utc) + timedelta(
        minutes=config.settings.ACCESS_TOKEN_EXPIRE_MINUTES)
  to_encode.update({"exp": expire})
  encoded_jwt = jwt.encode(to_encode,
                           config.settings.SECRET_KEY,
                           algorithm=config.settings.ALGORITHM)
  return encoded_jwt


def verify_access_token(token: str):
  """Verifica un token JWT y devuelve el ID de usuario si es válido."""
  try:
    payload = jwt.decode(token,
                         config.settings.SECRET_KEY,
                         algorithms=[config.settings.ALGORITHM])
    user_id: int = payload.get("sub")
    if user_id is None:
      raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                          detail="Token inválido.")
    return user_id
  except JWTError:
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                        detail="Token inválido o expirado.")


def get_current_user(token: str = Depends(oauth2_scheme),
                     db: Session = Depends(get_db)) -> Usuario:
  """Obtiene el usuario actual a partir del token JWT."""
  user_id = verify_access_token(token)
  user = db.query(Usuario).filter(Usuario.id_usuario == user_id).first()
  if not user:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                        detail="Usuario no encontrado.")
  return user
