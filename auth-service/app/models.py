from sqlalchemy import Column, Integer, String
from app.database import Base

# Define la tabla 'usuarios' donde se almacenan las credenciales y datos del perfil.
class Usuario(Base):
    __tablename__ = "usuarios"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, nullable=False, unique=True, index=True)
    password_hash = Column(String, nullable=False)