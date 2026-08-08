from pydantic import BaseModel
from datetime import datetime

# Esquema para validar los datos enviados al crear un nuevo pago (pedido_id y monto).
class PagoCreate(BaseModel):
    pedido_id: int
    monto: float

# Esquema para devolver la información del pago al cliente (incluye ID y estado generados por la BD).
class PagoResponse(BaseModel):
    id: int
    pedido_id: int
    monto: float
    estado: str
    creado_en: datetime

    class Config:
        from_attributes = True