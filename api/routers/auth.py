from datetime import timedelta

from api import auth
from api import config
from api import database
from api.auth.hashing import hash_password
from api.auth.hashing import verify_password
from api.auth.jwt import create_access_token
from api.auth.verification import generate_verification_code
from api.auth.verification import send_verification_email
from api.dependencies import oauth2_scheme
from api.models.perfil import PerfilUsuario
# from api.schemas.perfil import PerfilUsuarioCreate # No es necesario importar el esquema completo
from api.models.usuario import Usuario
from api.schemas.usuario import Usuario as UsuarioSchema
from api.schemas.usuario import UsuarioCreate
from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from fastapi import status
from sqlalchemy.orm import Session

router = APIRouter()

# Simulación simple de almacenamiento temporal del código de verificación
# En producción, usar una base de datos o un sistema de cache (Redis) con TTL
verification_codes = {}


@router.post("/register",
             response_model=UsuarioSchema,
             status_code=status.HTTP_201_CREATED)
def register(usuario_data: UsuarioCreate,
             db: Session = Depends(database.get_db)):
  # Verificar si el email ya existe
  db_usuario = db.query(Usuario).filter(
      Usuario.email == usuario_data.email).first()
  if db_usuario:
    raise HTTPException(status_code=400, detail="El email ya está registrado")

  # Crear nuevo usuario
  hashed_pwd = hash_password(usuario_data.password)
  nuevo_usuario = Usuario(email=usuario_data.email,
                          password_hash=hashed_pwd,
                          nombre=usuario_data.nombre)
  db.add(nuevo_usuario)
  db.flush()  # flush() para obtener el ID sin commitear la transacción

  # Crear perfil vacío/por defecto para el nuevo usuario (US1.2, inicio)
  # Inicializamos solo los campos obligatorios o con valores por defecto
  # Los campos clave del nuevo perfil financiero se llenarán posteriormente
  perfil_inicial = PerfilUsuario(
      id_usuario=nuevo_usuario.id_usuario,
      # Campos de informacion_personal (inicialmente vacíos o nulos)
      nombre=None,  # Se puede dejar vacío o pedirlo en register si es necesario
      apellido=None,
      fecha_nacimiento=None,
      id_pais_residencia=None,  # FK a paises_latam, dejar nula por ahora
      acepta_terminos=usuario_data.acepta_terminos if hasattr(
          usuario_data, 'acepta_terminos') else
      False,  # Asumiendo que UsuarioCreate ahora tiene este campo o se pide después
      # Campos de datos_financieros.perfil_financiero (inicialmente vacíos o con valores por defecto)
      ingreso_mensual_estimado=0,
      gastos_fijos_mensuales=0,
      gastos_variables_mensuales=0,
      ahorro_actual=0,
      deuda_total=0,
      monto_meta_ahorro=0,
      plazo_meta_ahorro_meses=0,
      ahorro_planificado_mensual=0,
      fuentes_ingreso=[]  # Inicializar como lista vacía
      # Otros campos del perfil pueden inicializarse como nulos o con valores por defecto
  )
  db.add(perfil_inicial)

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
      minutes=config.settings.ACCESS_TOKEN_EXPIRE_MINUTES)
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
  if usuario_id in verification_codes:
    del verification_codes[usuario_id]

  return {"message": "Email verificado exitosamente"}
