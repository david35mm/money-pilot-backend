from fastapi.testclient import TestClient
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from api.database import get_db
from api.main import app
from api.models.base import Base

# Usar SQLite en memoria para pruebas
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(SQLALCHEMY_DATABASE_URL,
                       connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False,
                                   autoflush=False,
                                   bind=engine)

# Crear las tablas en la base de datos de prueba
Base.metadata.create_all(bind=engine)


@pytest.fixture(scope="module")
def db_session():
  """Crea una nueva sesión de base de datos para cada módulo de pruebas."""
  connection = engine.connect()
  transaction = connection.begin()
  session = TestingSessionLocal(bind=connection)
  yield session
  session.close()
  transaction.rollback()
  connection.close()


@pytest.fixture(scope="module")
def client(db_session):
  """Crea un cliente de prueba FastAPI inyectando la sesión de DB de prueba."""

  def override_get_db():
    try:
      yield db_session
    finally:
      pass  # La sesión se cierra en el fixture db_session

  app.dependency_overrides[get_db] = override_get_db
  with TestClient(app) as c:
    yield c
  # Limpiar la sobreescritura de la dependencia
  app.dependency_overrides.clear()
