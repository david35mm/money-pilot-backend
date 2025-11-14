from datetime import date
from datetime import timedelta
from typing import Optional

from api.auth.token import get_user_id_from_token
from api.database import get_db
from api.models.categorias import CategoriaGasto
from api.models.categorias import CategoriaIngreso
from api.models.evento_financiero import EventoFinanciero
from api.models.usuario import Usuario
from api.schemas.evento_financiero import EventoFinancieroCreate
from api.schemas.evento_financiero import EventoFinancieroDBRead
from api.schemas.evento_financiero import EventoFinancieroListRead
from api.schemas.evento_financiero import EventoFinancieroUpdate
from api.schemas.evento_financiero import EventosFinancierosResponse
from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from fastapi import Query
from fastapi import status
from sqlalchemy import func
from sqlalchemy.orm import Session

router = APIRouter(prefix="/eventos_financieros", tags=["Eventos Financieros"])


@router.post("/",
             response_model=EventoFinancieroDBRead,
             status_code=status.HTTP_201_CREATED)
def crear_evento_financiero(
    data: EventoFinancieroCreate,
    db: Session = Depends(get_db),
    token_user_id: int | None = Depends(get_user_id_from_token),
    id_usuario: int | None = None,
):
  """Crea un evento financiero ('INGRESO' o 'GASTO')."""

  user_id = id_usuario or token_user_id
  if not user_id:
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                        detail="No autorizado o token inválido.")

  user = db.query(Usuario).filter(Usuario.id_usuario == user_id).first()
  if not user:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                        detail="Usuario no encontrado.")

  tipo = data.tipo.upper()

  if tipo not in ("INGRESO", "GASTO"):
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                        detail="El tipo debe ser 'INGRESO' o 'GASTO'.")

  # Normalize fields
  if tipo == "GASTO":
    if not data.id_categoria_gasto:
      raise HTTPException(
          status_code=status.HTTP_400_BAD_REQUEST,
          detail="Debe proporcionar id_categoria_gasto para un gasto.")
    # Validate category exists
    categoria_gasto = db.query(CategoriaGasto).filter(
        CategoriaGasto.id_categoria_gasto == data.id_categoria_gasto).first()
    if not categoria_gasto:
      raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                          detail="Categoría de gasto no válida")
    id_categoria_gasto = data.id_categoria_gasto
    id_categoria_ingreso = None
  else:
    if not data.id_categoria_ingreso:
      raise HTTPException(
          status_code=status.HTTP_400_BAD_REQUEST,
          detail="Debe proporcionar id_categoria_ingreso para un ingreso.")
    # Validate category exists
    categoria_ingreso = db.query(CategoriaIngreso).filter(
        CategoriaIngreso.id_categoria_ingreso ==
        data.id_categoria_ingreso).first()
    if not categoria_ingreso:
      raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                          detail="Categoría de ingreso no válida")
    id_categoria_gasto = None
    id_categoria_ingreso = data.id_categoria_ingreso

  # Handle es_unico / semana_inicio logic
  es_unico = True if data.es_unico is None else data.es_unico
  semana_inicio = None if es_unico else data.semana_inicio

  evento = EventoFinanciero(
      id_usuario=user_id,
      tipo=tipo,
      id_categoria_gasto=id_categoria_gasto,
      id_categoria_ingreso=id_categoria_ingreso,
      monto=data.monto,
      fecha=data.fecha,
      descripcion=data.descripcion,
      es_unico=es_unico,
      semana_inicio=semana_inicio,
  )

  db.add(evento)
  db.commit()
  db.refresh(evento)
  return evento


@router.get("/",
            response_model=EventosFinancierosResponse,
            status_code=status.HTTP_200_OK)
def obtener_eventos_financieros(
    db: Session = Depends(get_db),
    token_user_id: int | None = Depends(get_user_id_from_token),
    id_usuario: int | None = None,
    tipo: Optional[str] = Query(None),
    fecha_inicio: Optional[date] = Query(None),
    fecha_fin: Optional[date] = Query(None),
    id_categoria_gasto: Optional[int] = Query(None),
    id_categoria_ingreso: Optional[int] = Query(None),
    limit: int = Query(100, ge=1, le=500),
    offset: int = Query(0, ge=0),
):
  """Obtiene los eventos financieros de un usuario, con filtros dinámicos."""
  user_id = id_usuario or token_user_id
  if not user_id:
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                        detail="No autorizado o token inválido.")

  user = db.query(Usuario).filter(Usuario.id_usuario == user_id).first()
  if not user:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                        detail="Usuario no encontrado.")

  if not fecha_inicio or not fecha_fin:
    today = date.today()
    fecha_inicio = fecha_inicio or date(today.year, today.month, 1)
    next_month = date(today.year + (today.month // 12), (today.month % 12) + 1,
                      1)
    fecha_fin = fecha_fin or (next_month - timedelta(days=1))

  query = db.query(EventoFinanciero).filter(
      EventoFinanciero.id_usuario == user_id,
      EventoFinanciero.fecha.between(fecha_inicio, fecha_fin))

  if tipo:
    query = query.filter(EventoFinanciero.tipo == tipo.upper())
  if id_categoria_gasto:
    query = query.filter(
        EventoFinanciero.id_categoria_gasto == id_categoria_gasto)
  if id_categoria_ingreso:
    query = query.filter(
        EventoFinanciero.id_categoria_ingreso == id_categoria_ingreso)

  eventos = query.order_by(
      EventoFinanciero.fecha.desc()).offset(offset).limit(limit).all()

  # Enrich with category names
  eventos_enriquecidos = []
  for ev in eventos:
    categoria_nombre = None
    if ev.tipo == "GASTO" and ev.id_categoria_gasto:
      categoria = db.query(CategoriaGasto.nombre).filter(
          CategoriaGasto.id_categoria_gasto == ev.id_categoria_gasto).first()
      categoria_nombre = categoria[0] if categoria else None
    elif ev.tipo == "INGRESO" and ev.id_categoria_ingreso:
      categoria = db.query(
          CategoriaIngreso.nombre).filter(CategoriaIngreso.id_categoria_ingreso
                                          == ev.id_categoria_ingreso).first()
      categoria_nombre = categoria[0] if categoria else None

    eventos_enriquecidos.append(
        EventoFinancieroListRead(id_evento=ev.id_evento,
                                 tipo=ev.tipo,
                                 monto=ev.monto,
                                 fecha=ev.fecha,
                                 descripcion=ev.descripcion,
                                 es_unico=ev.es_unico,
                                 semana_inicio=ev.semana_inicio,
                                 categoria=categoria_nombre))

  total_gastos = db.query(func.coalesce(
      func.sum(EventoFinanciero.monto),
      0)).filter(EventoFinanciero.id_usuario == user_id,
                 EventoFinanciero.tipo == "GASTO",
                 EventoFinanciero.fecha.between(fecha_inicio,
                                                fecha_fin)).scalar()

  total_ingresos = db.query(func.coalesce(
      func.sum(EventoFinanciero.monto),
      0)).filter(EventoFinanciero.id_usuario == user_id,
                 EventoFinanciero.tipo == "INGRESO",
                 EventoFinanciero.fecha.between(fecha_inicio,
                                                fecha_fin)).scalar()

  return EventosFinancierosResponse(
      eventos=eventos_enriquecidos,
      total_eventos=len(eventos_enriquecidos),
      total_gastos=float(total_gastos),
      total_ingresos=float(total_ingresos),
  )


@router.put("/{id_evento}",
            response_model=EventoFinancieroDBRead,
            status_code=status.HTTP_200_OK)
def actualizar_evento_financiero(
    id_evento: int,
    data: EventoFinancieroUpdate,
    db: Session = Depends(get_db),
    token_user_id: int | None = Depends(get_user_id_from_token),
    id_usuario: int | None = None,
):
  """Actualiza un evento financiero existente."""
  user_id = id_usuario or token_user_id
  if not user_id:
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                        detail="No autorizado o token inválido.")

  evento = db.query(EventoFinanciero).filter(
      EventoFinanciero.id_evento == id_evento,
      EventoFinanciero.id_usuario == user_id).first()

  if not evento:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                        detail="Evento no encontrado.")

  if data.tipo:
    tipo = data.tipo.upper()
    if tipo not in ("INGRESO", "GASTO"):
      raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                          detail="El tipo debe ser 'INGRESO' o 'GASTO'.")
    evento.tipo = tipo

  if data.monto is not None:
    evento.monto = data.monto
  if data.fecha is not None:
    evento.fecha = data.fecha
  if data.descripcion is not None:
    evento.descripcion = data.descripcion
  if data.es_unico is not None:
    evento.es_unico = data.es_unico
    evento.semana_inicio = None if data.es_unico else data.semana_inicio

  # Validate and update category fields based on tipo
  if evento.tipo == "GASTO":
    if data.id_categoria_gasto is not None:
      # Validate category exists
      categoria_gasto = db.query(CategoriaGasto).filter(
          CategoriaGasto.id_categoria_gasto == data.id_categoria_gasto).first()
      if not categoria_gasto:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Categoría de gasto no válida")
      evento.id_categoria_gasto = data.id_categoria_gasto
    evento.id_categoria_ingreso = None
  elif evento.tipo == "INGRESO":
    if data.id_categoria_ingreso is not None:
      # Validate category exists
      categoria_ingreso = db.query(CategoriaIngreso).filter(
          CategoriaIngreso.id_categoria_ingreso ==
          data.id_categoria_ingreso).first()
      if not categoria_ingreso:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Categoría de ingreso no válida")
      evento.id_categoria_ingreso = data.id_categoria_ingreso
    evento.id_categoria_gasto = None

  db.commit()
  db.refresh(evento)
  return evento


@router.delete("/{id_evento}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_evento_financiero(
    id_evento: int,
    db: Session = Depends(get_db),
    token_user_id: int | None = Depends(get_user_id_from_token),
    id_usuario: int | None = None,
):
  """Elimina un evento financiero del usuario (hard delete)."""
  user_id = id_usuario or token_user_id
  if not user_id:
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                        detail="No autorizado o token inválido.")

  evento = db.query(EventoFinanciero).filter(
      EventoFinanciero.id_evento == id_evento,
      EventoFinanciero.id_usuario == user_id).first()

  if not evento:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                        detail="Evento no encontrado.")

  db.delete(evento)
  db.commit()
  return None
