import re

from api import config
from sqlalchemy.ext.asyncio import async_sessionmaker
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine


def ensure_async_driver(db_url: str) -> str:
  """
    Ensures the database URL uses the asyncpg driver for async operations
    while keeping the original clean URL format in environment variables.
    """
  if db_url.startswith("postgresql://"):
    # Replace with postgresql+asyncpg:// for async operations
    return db_url.replace("postgresql://", "postgresql+asyncpg://", 1)
  return db_url


engine = create_async_engine(
    ensure_async_driver(config.settings.DATABASE_URL),
    # echo=True # Descomentar para ver queries SQL en consola (útil para debugging)
)

AsyncSessionLocal = async_sessionmaker(engine,
                                       class_=AsyncSession,
                                       expire_on_commit=False)


async def get_db():
  async with AsyncSessionLocal() as session:
    try:
      yield session
    finally:
      await session.close()
