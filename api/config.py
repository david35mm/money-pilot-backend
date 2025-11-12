import os
from typing import List, Optional

from pydantic import Field
from pydantic_settings import BaseSettings
from pydantic_settings import SettingsConfigDict


class Settings(BaseSettings):
  ENV: str = Field(default=os.getenv("ENV", "development"))
  DATABASE_URL: str = os.getenv("DATABASE_URL",
                                "postgresql://user:password@localhost/dbname")

  SECRET_KEY: str = os.getenv(
      "SECRET_KEY", "your-default-secret-key-change-it-in-production")
  ALGORITHM: str = os.getenv("ALGORITHM", "HS256")
  ACCESS_TOKEN_EXPIRE_MINUTES: int = int(
      os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))

  POSTGRES_USER: str = os.getenv("POSTGRES_USER", "postgres")
  POSTGRES_PASSWORD: str = os.getenv("POSTGRES_PASSWORD", "postgres")
  POSTGRES_DB: str = os.getenv("POSTGRES_DB", "postgres")

  ALLOWED_ORIGINS: Optional[str] = Field(
      default=os.getenv("ALLOWED_ORIGINS", "*"))

  DEBUG: bool = os.getenv("DEBUG", "False").lower() == "true"

  model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

  def allowed_origins_list(self) -> List[str]:
    """Safely return parsed origins as list."""
    if not self.ALLOWED_ORIGINS or self.ALLOWED_ORIGINS.strip() == "*":
      return ["*"]
    return [o.strip() for o in self.ALLOWED_ORIGINS.split(",") if o.strip()]


settings = Settings()
