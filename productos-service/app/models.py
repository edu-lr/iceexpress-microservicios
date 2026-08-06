from sqlalchemy import Column, Integer, String, Float
from app.database import Base

class Producto(Base):
    __tablename__ = "productos"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, nullable=False)
    tipo_hielo = Column(String, nullable=False)  # ej: "cubos", "escamas", "bloque"
    precio = Column(Float, nullable=False)
    descripcion = Column(String, nullable=True)