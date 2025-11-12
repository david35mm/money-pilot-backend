from api.auth.token import verify_access_token
from api.database import get_db
from api.models.usuario import Usuario
from fastapi import Depends
from fastapi import HTTPException
from fastapi import status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/v1/auth/login")


async def get_current_user(db: AsyncSession = Depends(get_db),
                           token: str = Depends(oauth2_scheme)):
  """Dependencia que obtiene el usuario actual a partir del token JWT."""
  credentials_exception = HTTPException(
      status_code=status.HTTP_401_UNAUTHORIZED,
      detail="No se pudieron validar las credenciales",
      headers={"WWW-Authenticate": "Bearer"},
  )
  payload = verify_access_token(token)
  if payload is None:
    raise credentials_exception
  user_id: int = payload.get("sub")
  if user_id is None:
    raise credentials_exception

  result = await db.execute(
      select(Usuario).filter(Usuario.id_usuario == user_id))
  user = result.scalar_one_or_none()
  if user is None:
    raise credentials_exception
  return user
