from fastapi.testclient import TestClient
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from api.database import get_db
from api.main import app
from api.models.base import Base  # Asegúrate de importar Base desde el archivo correcto

# Usar SQLite en memoria con StaticPool para pruebas
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False
                 },  # Necesario para SQLite en memoria
    poolclass=StaticPool,  # Crucial para pruebas con SQLite en memoria
    echo=False  # Cambia a True si quieres ver las queries SQL
)
TestingSessionLocal = sessionmaker(autocommit=False,
                                   autoflush=False,
                                   bind=engine)

# Creamos las tablas en el engine (antes de cualquier test)
Base.metadata.create_all(bind=engine)


@pytest.fixture(
    scope="function"
)  # Cambiamos el scope a function para que coincida con db_session
def db_session():
  """Crea una nueva sesión de base de datos para cada función de prueba."""
  connection = engine.connect()
  transaction = connection.begin()
  session = TestingSessionLocal(bind=connection)
  # Creamos las tablas *dentro* de la transacción de la sesión de prueba
  Base.metadata.create_all(bind=connection)
  yield session
  session.close()
  transaction.rollback()
  connection.close()


@pytest.fixture(
    scope="function"
)  # Cambiamos el scope a function para que coincida con db_session
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
