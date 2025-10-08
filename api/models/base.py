from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.orm import as_declarative


@as_declarative()
class Base:

  @declared_attr
  def __tablename__(cls):
    # Genera el nombre de la tabla automáticamente a partir del nombre de la clase
    return cls.__name__.lower()
