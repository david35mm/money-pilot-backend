import os

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
  # Database
  DATABASE_URL: str = os.getenv("DATABASE_URL",
                                "postgresql://user:password@localhost/dbname")

  # Auth
  SECRET_KEY: str = os.getenv(
      "SECRET_KEY", "your-default-secret-key-change-it-in-production")
  ALGORITHM: str = os.getenv("ALGORITHM", "HS256")
  ACCESS_TOKEN_EXPIRE_MINUTES: int = int(
      os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))

  # CORS
  # Asegúrate de que ALLOWED_ORIGINS sea una variable de entorno con los orígenes separados por comas
  # Ejemplo: ALLOWED_ORIGINS=http://localhost:3000,https://myapp.com
  ALLOWED_ORIGINS: list[str] = os.getenv("ALLOWED_ORIGINS",
                                         "http://localhost:3000").split(",")

  # Otros ajustes si es necesario
  DEBUG: bool = os.getenv("DEBUG", "False").lower() == "true"

  class Config:
    env_file = ".env"  # Si usas un archivo .env


settings = Settings()
