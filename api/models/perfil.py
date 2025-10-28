from api.models.base import Base
from sqlalchemy import ARRAY
from sqlalchemy import Boolean
from sqlalchemy import Column
from sqlalchemy import Date
from sqlalchemy import DateTime
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import Numeric
from sqlalchemy import String
from sqlalchemy import Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func


class PerfilUsuario(Base):
  __tablename__ = "perfiles_usuario"

  id_perfil = Column(Integer, primary_key=True, index=True)
  id_usuario = Column(Integer,
                      ForeignKey("usuarios.id_usuario"),
                      unique=True,
                      nullable=False)

  nombre = Column(String(100))
  apellido = Column(String(100))
  fecha_nacimiento = Column(Date)
  # id_pais_residencia = Column(Integer, ForeignKey("paises_latam.id_pais"))
  id_pais_residencia = Column(Integer, nullable=False)
  acepta_terminos = Column(Boolean, default=False)

  ingreso_mensual_estimado = Column(Numeric(12, 2))
  gastos_fijos_mensuales = Column(Numeric(12, 2))
  gastos_variables_mensuales = Column(Numeric(12, 2))
  ahorro_actual = Column(Numeric(12, 2), server_default="0")
  deuda_total = Column(Numeric(12, 2), server_default="0")
  monto_meta_ahorro = Column(Numeric(12, 2))
  plazo_meta_ahorro_meses = Column(Integer)
  ahorro_planificado_mensual = Column(Numeric(12, 2))
  fuentes_ingreso = Column(ARRAY(Text))

  fecha_creacion = Column(DateTime, server_default=func.now())
  ultima_actualizacion = Column(DateTime,
                                server_default=func.now(),
                                onupdate=func.now())

  usuario = relationship("Usuario", back_populates="perfil")
  # pais = relationship("PaisLatam", lazy="joined")
