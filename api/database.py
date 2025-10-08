from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker

from api import config

# Crear el engine de SQLAlchemy
engine = create_engine(
    config.settings.DATABASE_URL,
    # echo=True # Descomentar para ver queries SQL en consola (útil para debugging)
)

# Crear una clase de sesión local
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Instancia base para crear modelos
Base = declarative_base()


# Dependencia FastAPI para obtener la sesión de DB
def get_db():
  db = SessionLocal()
  try:
    yield db
  finally:
    db.close()
