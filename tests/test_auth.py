from fastapi.testclient import TestClient
import pytest

from api.models.perfil import PerfilUsuario
from api.models.usuario import Usuario


def test_register_and_create_profile(client, db_session):
  """Prueba el registro de un usuario y la creación automática de su perfil."""
  # Datos de registro
  user_data = {
      "email": "test_user@example.com",
      "password": "securepassword123",
      "nombre": "Test User"
  }

  response = client.post("/api/v1/register", json=user_data)
  assert response.status_code == 201

  # Verificar que el usuario se haya creado en la DB
  user_in_db = db_session.query(Usuario).filter(
      Usuario.email == user_data["email"]).first()
  assert user_in_db is not None
  assert user_in_db.nombre == user_data["nombre"]

  # Verificar que el perfil se haya creado automáticamente
  profile_in_db = db_session.query(PerfilUsuario).filter(
      PerfilUsuario.id_usuario == user_in_db.id_usuario).first()
  assert profile_in_db is not None
  assert profile_in_db.nombre_completo == user_data[
      "nombre"]  # Se copia el nombre en register


def test_login_success(client, db_session):
  """Prueba el inicio de sesión exitoso."""
  # Asumiendo que el usuario ya está registrado y verificado (perfil opcional)
  # Primero, registramos un usuario para tener datos
  user_data = {
      "email": "login_test@example.com",
      "password": "anotherpassword123",
      "nombre": "Login Test"
  }
  client.post("/api/v1/register", json=user_data)

  login_data = {
      "email": "login_test@example.com",
      "password": "anotherpassword123"
  }
  response = client.post("/api/v1/login", json=login_data)
  assert response.status_code == 200
  data = response.json()
  assert "access_token" in data
  assert data["token_type"] == "bearer"


def test_login_invalid_credentials(client, db_session):
  """Prueba el inicio de sesión con credenciales incorrectas."""
  login_data = {"email": "nonexistent@example.com", "password": "wrongpassword"}
  response = client.post("/api/v1/login", json=login_data)
  assert response.status_code == 401
