from sqlalchemy.ext.declarative import as_declarative
from sqlalchemy.ext.declarative import declared_attr


@as_declarative()
class Base:

  @declared_attr
  def __tablename__(cls):
    # Genera el nombre de la tabla automáticamente a partir del nombre de la clase
    return cls.__name__.lower()
