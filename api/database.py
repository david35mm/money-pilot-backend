from api import config
from sqlalchemy.ext.asyncio import async_sessionmaker
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine

engine = create_async_engine(
    config.settings.DATABASE_URL,
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
