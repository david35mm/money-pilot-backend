from pydantic import BaseModel


class BaseSchema(BaseModel):

  class Config:
    # Permite que los modelos se puedan crear a partir de objetos ORM de SQLAlchemy
    from_attributes = True
