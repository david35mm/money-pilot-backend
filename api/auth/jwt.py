from datetime import datetime
from datetime import timedelta
from datetime import timezone
from typing import Optional

from jose import jwt
from jose import JWTError

from api import config


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
  """Verifica un token JWT de acceso y devuelve el payload si es válido."""
  try:
    payload = jwt.decode(token,
                         config.settings.SECRET_KEY,
                         algorithms=[config.settings.ALGORITHM])
    user_id: int = payload.get("sub")
    if user_id is None:
      return None
    return payload
  except JWTError:
    return None
