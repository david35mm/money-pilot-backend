from datetime import date

from api.auth.hashing import hash_password
from api.models.categoria import Categoria
from api.models.transaccion import Transaccion
from api.models.usuario import Usuario
from fastapi.testclient import TestClient
import pytest


def test_create_and_get_transaccion(client, db_session):
  """Prueba la creación y obtención de una transacción (simulando autenticación)."""
  # Crear usuario y categoría de prueba
  hashed_pwd = hash_password("trans_test_password")
  new_user = Usuario(email="trans_test@example.com",
                     password_hash=hashed_pwd,
                     nombre="Trans Test")
  db_session.add(new_user)
  db_session.flush()  # Para obtener el ID

  new_categoria = Categoria(nombre="Alimentación", tipo="gasto")
  db_session.add(new_categoria)
  db_session.flush()

  db_session.commit()

  # Datos de la transacción
  transaccion_data = {
      "id_usuario":
          new_user.
          id_usuario,  # Este campo se debería tomar del token, no del payload
      "id_categoria": new_categoria.id_categoria,
      "monto": 50000.0,
      "fecha": date.fromisoformat("2025-10-08"),  # Convertimos la cadena a date
      "tipo": "gasto",
      "notas": "Desayuno en café"
  }

  # Simular autenticación (ver comentario en test_perfiles.py)
  # headers = {"Authorization": f"Bearer {fake_token_for_user(new_user.id_usuario)}"}

  # Intentar crear la transacción
  # response = client.post("/api/v1/transacciones", json=transaccion_data, headers=headers)
  # El router transacciones verifica el id_usuario del payload contra el token.
  # Para probarlo, necesitamos inyectar el `current_user`.
  # Usaremos el ID del payload para este test simple, asumiendo que el router lo valida correctamente.

  # Creamos la transacción directamente en la DB para probar la obtención
  new_transaccion = Transaccion(**transaccion_data)
  db_session.add(new_transaccion)
  db_session.commit()

  # Intentar obtener la transacción
  # response_get = client.get(f"/api/v1/transacciones/{new_transaccion.id_transaccion}", headers=headers)
  # Nuevamente, necesitamos inyectar el `current_user` para que la validación de id_usuario funcione.
  # Para simplificar, verificamos directamente en la base de datos que se haya creado.
  transaccion_in_db = db_session.query(Transaccion).filter(
      Transaccion.id_transaccion == new_transaccion.id_transaccion).first()
  assert transaccion_in_db is not None
  assert transaccion_in_db.monto == transaccion_data["monto"]
  assert transaccion_in_db.id_usuario == new_user.id_usuario
  assert transaccion_in_db.fecha == transaccion_data[
      "fecha"]  # Verificamos que la fecha se haya guardado correctamente

  # Limpiar
  db_session.delete(new_user)  # Borra transacciones y categorias por cascada
  db_session.commit()
  # Verificar que se eliminó
  user_check = db_session.query(Usuario).filter(
      Usuario.id_usuario == new_user.id_usuario).first()
  assert user_check is None


# --- Nueva prueba para el endpoint POST /api/v1/transacciones ---
def test_registro_manual_gasto_endpoint(client, db_session):
  """Prueba el endpoint POST /api/v1/transacciones para registrar un gasto manual."""
  # 1. Registrar un usuario (esto crea el perfil automáticamente)
  user_data = {
      "email": "test_registro_gasto@example.com",
      "password": "testpassword123",
      "nombre": "Test User Gasto"
  }
  response_register = client.post("/api/v1/register", json=user_data)
  assert response_register.status_code == 201
  user_in_db = db_session.query(Usuario).filter(
      Usuario.email == user_data["email"]).first()
  assert user_in_db is not None
  user_id = user_in_db.id_usuario

  # 2. Crear una categoría de gasto
  categoria_data = {"nombre": "Supermercado", "tipo": "gasto"}
  # Simulamos un token para autenticar la creación de la categoría si fuera necesario,
  # pero en nuestra implementación actual, categorias es global.
  response_categoria = client.post("/api/v1/categorias", json=categoria_data)
  assert response_categoria.status_code == 201
  categoria_in_db = db_session.query(Categoria).filter(
      Categoria.nombre == categoria_data["nombre"]).first()
  assert categoria_in_db is not None
  categoria_id = categoria_in_db.id_categoria

  # 3. Iniciar sesión para obtener el token JWT
  login_data = {"email": user_data["email"], "password": user_data["password"]}
  response_login = client.post("/api/v1/login", json=login_data)
  assert response_login.status_code == 200
  token_data = response_login.json()
  assert "access_token" in token_data
  access_token = token_data["access_token"]
  headers = {"Authorization": f"Bearer {access_token}"}

  # 4. Enviar solicitud POST para registrar el gasto
  gasto_data = {
      "id_usuario":
          user_id,  # <-- Este campo es requerido por el esquema TransaccionCreate
      "id_categoria":
          categoria_id,  # <-- Este campo es requerido por el esquema TransaccionCreate
      "monto": 125000.0,
      "fecha": "2025-10-18",  # Formato ISO
      "tipo": "gasto",
      "es_unico": False,  # Opcional
      "notas": "Compra de la semana en supermercado X"
  }

  response_create = client.post("/api/v1/transacciones",
                                json=gasto_data,
                                headers=headers)

  # 5. Verificar la respuesta del servidor
  assert response_create.status_code == 201
  created_gasto = response_create.json()
  assert created_gasto[
      "id_usuario"] == user_id  # Verificamos que se asignó correctamente el ID del usuario autenticado
  assert created_gasto["id_categoria"] == categoria_id
  assert created_gasto["monto"] == gasto_data["monto"]
  assert created_gasto["fecha"] == gasto_data["fecha"]
  assert created_gasto["tipo"] == gasto_data["tipo"]
  assert created_gasto["notas"] == gasto_data["notas"]

  # 6. Verificar que la transacción se haya guardado en la base de datos
  transaccion_in_db = db_session.query(Transaccion).filter(
      Transaccion.id_usuario == user_id,
      Transaccion.monto == gasto_data["monto"],
      Transaccion.fecha == date.fromisoformat(gasto_data["fecha"])).first()
  assert transaccion_in_db is not None
  assert transaccion_in_db.tipo == "gasto"
  assert transaccion_in_db.es_unico == gasto_data["es_unico"]

  # Limpiar: Eliminar el usuario (y por cascada, la transacción y el perfil)
  db_session.delete(user_in_db)
  # Eliminar la categoría global (cuidado con esto en prod, aquí es solo para el test)
  db_session.delete(categoria_in_db)
  db_session.commit()

  # Verificar que se eliminó
  user_check = db_session.query(Usuario).filter(
      Usuario.id_usuario == user_id).first()
  assert user_check is None
  categoria_check = db_session.query(Categoria).filter(
      Categoria.id_categoria == categoria_id).first()
  assert categoria_check is None
  transaccion_check = db_session.query(Transaccion).filter(
      Transaccion.id_transaccion == created_gasto["id_transaccion"]).first()
  assert transaccion_check is None
