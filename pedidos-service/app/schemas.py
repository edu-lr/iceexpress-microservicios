from pydantic import BaseModel
from typing import List
from datetime import datetime

# Lo que el cliente manda para pedir UN producto dentro del pedido
class PedidoItemCreate(BaseModel):
    producto_id: int
    cantidad: int

# Lo que el cliente manda para crear el pedido completo
class PedidoCreate(BaseModel):
    items: List[PedidoItemCreate]

# Lo que la API devuelve por cada ítem (ya con precio calculado)
class PedidoItemResponse(BaseModel):
    id: int
    producto_id: int
    cantidad: int
    precio_unitario: float

    class Config:
        from_attributes = True

# Lo que la API devuelve del pedido completo
class PedidoResponse(BaseModel):
    id: int
    estado: str
    total: float
    creado_en: datetime
    items: List[PedidoItemResponse]

    class Config:
        from_attributes = True