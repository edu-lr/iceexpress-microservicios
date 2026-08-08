from sqlalchemy import Column, Integer
from app.database import Base

# Define la tabla 'inventario' que lleva el control del stock de cada producto.
class Inventario(Base):
    __tablename__ = "inventario"

    id = Column(Integer, primary_key=True, index=True)
    producto_id = Column(Integer, nullable=False, unique=True, index=True)
    cantidad = Column(Integer, nullable=False, default=0)