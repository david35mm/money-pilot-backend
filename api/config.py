import os
from typing import List

from pydantic import Field
from pydantic_settings import BaseSettings
from pydantic_settings import SettingsConfigDict


class Settings(BaseSettings):
  # Environment (default = development)
  ENV: str = Field(default=os.getenv("ENV", "development"))

  # Database
  DATABASE_URL: str = os.getenv("DATABASE_URL",
                                "postgresql://user:password@localhost/dbname")

  # Auth
  SECRET_KEY: str = os.getenv(
      "SECRET_KEY", "your-default-secret-key-change-it-in-production")
  ALGORITHM: str = os.getenv("ALGORITHM", "HS256")
  ACCESS_TOKEN_EXPIRE_MINUTES: int = int(
      os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))

  # PostgreSQL
  POSTGRES_USER: str = os.getenv("POSTGRES_USER", "postgres")
  POSTGRES_PASSWORD: str = os.getenv("POSTGRES_PASSWORD", "postgres")
  POSTGRES_DB: str = os.getenv("POSTGRES_DB", "postgres")

  # CORS
  # Asegúrate de que ALLOWED_ORIGINS sea una variable de entorno con los orígenes separados por comas
  # Ejemplo: ALLOWED_ORIGINS=http://localhost:3000,https://myapp.com
  ALLOWED_ORIGINS: List[str] = Field(
      default_factory=lambda: os.getenv("ALLOWED_ORIGINS", "*").split(","))

  # Otros ajustes si es necesario
  DEBUG: bool = os.getenv("DEBUG", "False").lower() == "true"

  # Configuración de Pydantic V2
  model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")


settings = Settings()
