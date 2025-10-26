from api.database import get_db
from api.models.perfil import PerfilUsuario
from api.models.usuario import Usuario
from api.schemas.perfil import PerfilCompletoCreate
from api.schemas.perfil import PerfilUsuarioRead
from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from fastapi import status
from sqlalchemy.orm import Session

router = APIRouter(prefix="/perfil_financiero", tags=["Perfiles"])


@router.post("/{id_usuario}",
             response_model=PerfilUsuarioRead,
             status_code=status.HTTP_201_CREATED)
def crear_perfil_financiero(id_usuario: int,
                            data: PerfilCompletoCreate,
                            db: Session = Depends(get_db)):
  user = db.query(Usuario).filter(Usuario.id_usuario == id_usuario).first()
  if not user:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                        detail="Usuario no encontrado.")

  personal = data.informacion_personal
  financiero = data.datos_financieros.perfil_financiero

  pais = db.execute("SELECT id_pais FROM paises_latam WHERE codigo = :codigo", {
      "codigo": personal.codigo_pais
  }).fetchone()
  id_pais = pais[0] if pais else None

  perfil = PerfilUsuario(
      id_usuario=id_usuario,
      nombre=personal.nombre,
      apellido=personal.apellido,
      fecha_nacimiento=personal.fecha_nacimiento,
      id_pais_residencia=id_pais,
      acepta_terminos=personal.acepta_terminos,
      ingreso_mensual_estimado=financiero.ingreso_mensual_estimado,
      gastos_fijos_mensuales=financiero.gastos_fijos_mensuales,
      gastos_variables_mensuales=financiero.gastos_variables_mensuales,
      ahorro_actual=financiero.ahorro_actual,
      deuda_total=financiero.deuda_total,
      monto_meta_ahorro=financiero.meta_ahorro.monto,
      plazo_meta_ahorro_meses=financiero.meta_ahorro.plazo_meses,
      ahorro_planificado_mensual=financiero.ahorro_planificado_mensual,
      fuentes_ingreso=financiero.fuentes_ingreso)

  db.add(perfil)
  db.commit()
  db.refresh(perfil)
  return perfil
