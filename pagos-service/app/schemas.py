from pydantic import BaseModel
from datetime import datetime

class PagoCreate(BaseModel):
    pedido_id: int
    monto: float

class PagoResponse(BaseModel):
    id: int
    pedido_id: int
    monto: float
    estado: str
    creado_en: datetime

    class Config:
        from_attributes = True