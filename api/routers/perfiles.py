from api import database
from api.dependencies import get_current_user
from api.models.catalogo import PaisLatam
from api.models.perfil import PerfilUsuario
from api.models.usuario import Usuario
from api.schemas.perfil import PerfilUsuario as PerfilUsuarioSchema
from api.schemas.perfil import PerfilUsuarioCreate
from api.schemas.perfil import PerfilUsuarioUpdate
from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from fastapi import status
from sqlalchemy.orm import Session

router = APIRouter()


@router.post("/",
             response_model=PerfilUsuarioSchema,
             status_code=status.HTTP_201_CREATED)
def create_perfil(perfil_data: PerfilUsuarioCreate,
                  db: Session = Depends(database.get_db),
                  current_user: Usuario = Depends(get_current_user)):
  # Verificar si ya existe un perfil para este usuario
  existing_profile = db.query(PerfilUsuario).filter(
      PerfilUsuario.id_usuario == current_user.id_usuario).first()
  if existing_profile:
    raise HTTPException(
        status_code=400,
        detail=
        "El perfil para este usuario ya existe. Use PUT para actualizarlo.")

  # Verificar que el ID del usuario en el payload coincida con el del token
  if perfil_data.id_usuario != current_user.id_usuario:
    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="No autorizado para crear perfil para otro usuario.")

  # Opcional: Validar id_pais_residencia si se proporciona
  if perfil_data.id_pais_residencia:
    pais_existente = db.query(PaisLatam).filter(
        PaisLatam.id_pais == perfil_data.id_pais_residencia).first()
    if not pais_existente:
      raise HTTPException(
          status_code=400,
          detail=f"El país con id {perfil_data.id_pais_residencia} no existe.")

  # Crear nuevo perfil
  nuevo_perfil = PerfilUsuario(**perfil_data.model_dump())
  db.add(nuevo_perfil)
  db.commit()
  db.refresh(nuevo_perfil)

  # Opcional: Cargar la relación pais_residencia para devolverla en la respuesta
  # db.refresh(nuevo_perfil, attribute_names=['pais_residencia_obj'])
  # if nuevo_perfil.pais_residencia_obj:
  #     # Asignar el objeto país al esquema antes de devolverlo
  #     # Esto requiere manejo especial en Pydantic si se quiere incluir aquí
  #     # Una forma es usar `@property` en el modelo o manejarlo en el esquema de salida
  #     pass

  return nuevo_perfil


@router.get("/", response_model=PerfilUsuarioSchema)
def get_perfil(db: Session = Depends(database.get_db),
               current_user: Usuario = Depends(get_current_user)):
  perfil = db.query(PerfilUsuario).filter(
      PerfilUsuario.id_usuario == current_user.id_usuario).first()
  if not perfil:
    raise HTTPException(status_code=404, detail="Perfil no encontrado")
  # Opcional: Cargar la relación pais_residencia para devolverla en la respuesta
  # db.refresh(perfil, attribute_names=['pais_residencia_obj'])
  # if perfil.pais_residencia_obj:
  #     # Similar al create, manejar la inclusión del objeto país
  #     pass
  return perfil


@router.put("/", response_model=PerfilUsuarioSchema)
def update_perfil(perfil_data: PerfilUsuarioUpdate,
                  db: Session = Depends(database.get_db),
                  current_user: Usuario = Depends(get_current_user)):
  perfil = db.query(PerfilUsuario).filter(
      PerfilUsuario.id_usuario == current_user.id_usuario).first()
  if not perfil:
    raise HTTPException(status_code=404, detail="Perfil no encontrado")

  # Opcional: Validar id_pais_residencia si se proporciona en la actualización
  if perfil_data.id_pais_residencia:
    pais_existente = db.query(PaisLatam).filter(
        PaisLatam.id_pais == perfil_data.id_pais_residencia).first()
    if not pais_existente:
      raise HTTPException(
          status_code=400,
          detail=f"El país con id {perfil_data.id_pais_residencia} no existe.")

  # Actualizar solo los campos proporcionados
  for var, value in perfil_data.model_dump(exclude_unset=True).items():
    setattr(perfil, var, value)

  db.commit()
  db.refresh(perfil)
  # Opcional: Cargar la relación pais_residencia para devolverla en la respuesta
  # db.refresh(perfil, attribute_names=['pais_residencia_obj'])
  return perfil


# No se incluye DELETE para el perfil, ya que generalmente no se borra, solo se actualiza o se desactiva el usuario.
