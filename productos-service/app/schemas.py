from pydantic import BaseModel
from typing import Optional

# Lo que el cliente manda para CREAR un producto (no incluye id, porque lo genera la base de datos)
class ProductoCreate(BaseModel):
    nombre: str
    tipo_hielo: str
    precio: float
    descripcion: Optional[str] = None

# Lo que el cliente puede mandar para ACTUALIZAR (todos los campos opcionales)
class ProductoUpdate(BaseModel):
    nombre: Optional[str] = None
    tipo_hielo: Optional[str] = None
    precio: Optional[float] = None
    descripcion: Optional[str] = None

# Lo que la API DEVUELVE al cliente (sí incluye el id)
class ProductoResponse(BaseModel):
    id: int
    nombre: str
    tipo_hielo: str
    precio: float
    descripcion: Optional[str] = None

    class Config:
        from_attributes = True