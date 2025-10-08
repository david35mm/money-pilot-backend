from fastapi.testclient import TestClient
import pytest

from api.models.categoria import Categoria


def test_create_and_get_categoria(client, db_session):
  """Prueba la creación y obtención de una categoría."""
  categoria_data = {"nombre": "Transporte", "tipo": "gasto"}

  response = client.post("/api/v1/categorias", json=categoria_data)
  assert response.status_code == 201
  created_data = response.json()
  assert created_data["nombre"] == categoria_data["nombre"]
  assert created_data["tipo"] == categoria_data["tipo"]

  # Obtener la categoría creada
  categoria_id = created_data["id_categoria"]
  response_get = client.get(f"/api/v1/categorias/{categoria_id}")
  assert response_get.status_code == 200
  retrieved_data = response_get.json()
  assert retrieved_data["id_categoria"] == categoria_id
  assert retrieved_data["nombre"] == categoria_data["nombre"]

  # Limpiar: eliminar la categoría
  response_delete = client.delete(f"/api/v1/categorias/{categoria_id}")
  assert response_delete.status_code == 204
  # Verificar que se eliminó
  response_check = client.get(f"/api/v1/categorias/{categoria_id}")
  assert response_check.status_code == 404
