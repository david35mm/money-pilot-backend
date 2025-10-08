from datetime import timedelta

from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from fastapi import status
from sqlalchemy.orm import Session

from api import auth
from api import database
from api.auth.hashing import hash_password
from api.auth.hashing import verify_password
from api.auth.jwt import create_access_token
from api.auth.verification import generate_verification_code
from api.auth.verification import send_verification_email
from api.dependencies import oauth2_scheme  # Importamos oauth2_scheme
from api.models.usuario import Usuario
from api.schemas.usuario import Usuario as UsuarioSchema
from api.schemas.usuario import UsuarioCreate

router = APIRouter()

# Simulación simple de almacenamiento temporal del código de verificación
# En producción, usar una base de datos o un sistema de cache (Redis) con TTL
verification_codes = {}


@router.post("/register",
             response_model=UsuarioSchema,
             status_code=status.HTTP_201_CREATED)
def register(usuario: UsuarioCreate, db: Session = Depends(database.get_db)):
  # Verificar si el email ya existe
  db_usuario = db.query(Usuario).filter(Usuario.email == usuario.email).first()
  if db_usuario:
    raise HTTPException(status_code=400, detail="El email ya está registrado")

  # Crear nuevo usuario
  hashed_pwd = hash_password(usuario.password)
  nuevo_usuario = Usuario(email=usuario.email,
                          password_hash=hashed_pwd,
                          nombre=usuario.nombre)
  db.add(nuevo_usuario)
  db.commit()
  db.refresh(nuevo_usuario)

  # Generar y enviar código de verificación (simulado)
  code = generate_verification_code()
  verification_codes[nuevo_usuario.id_usuario] = code  # Almacenar temporalmente
  send_verification_email(nuevo_usuario.email, code)

  return nuevo_usuario


@router.post("/login")
def login(usuario_data: dict, db: Session = Depends(database.get_db)):
  # Buscar usuario por email
  usuario = db.query(Usuario).filter(
      Usuario.email == usuario_data.get("email")).first()
  if not usuario or not verify_password(usuario_data.get("password"),
                                        usuario.password_hash):
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                        detail="Credenciales incorrectas")

  # Crear token de acceso
  access_token_expires = timedelta(
      minutes=auth.config.settings.ACCESS_TOKEN_EXPIRE_MINUTES)
  access_token = create_access_token(data={"sub": str(usuario.id_usuario)},
                                     expires_delta=access_token_expires)

  return {"access_token": access_token, "token_type": "bearer"}


@router.post("/verify-email")
def verify_email(usuario_id: int, code: str):
  stored_code = verification_codes.get(usuario_id)
  if not stored_code or stored_code != code:
    raise HTTPException(status_code=400,
                        detail="Código de verificación inválido o expirado")

  # Si el código es correcto, se puede marcar al usuario como verificado en la base de datos
  # (Asumiendo que tienes un campo 'email_verified' en tu modelo Usuario)
  # db.query(Usuario).filter(Usuario.id_usuario == usuario_id).update({"email_verified": True})
  # db.commit()

  # Limpiar el código después de verificarlo
  del verification_codes[usuario_id]

  return {"message": "Email verificado exitosamente"}
