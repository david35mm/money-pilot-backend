from passlib.context import CryptContext

# Configura CryptContext para usar Argon2 como esquema por defecto
pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")


def hash_password(password: str) -> str:
  """Hashea una contraseña usando Argon2."""
  return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
  """Verifica si una contraseña coincide con su hash Argon2."""
  return pwd_context.verify(plain_password, hashed_password)
