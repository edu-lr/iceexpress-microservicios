from pydantic import BaseModel

# Lo que el cliente manda para CREAR un registro de inventario
class InventarioCreate(BaseModel):
    producto_id: int
    cantidad: int

# Lo que el cliente manda para ACTUALIZAR la cantidad
class InventarioUpdate(BaseModel):
    cantidad: int

# Lo que la API DEVUELVE al cliente
class InventarioResponse(BaseModel):
    id: int
    producto_id: int
    cantidad: int

    class Config:
        from_attributes = True