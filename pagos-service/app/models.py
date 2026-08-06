from sqlalchemy import Column, Integer, Float, String, DateTime
from datetime import datetime
from app.database import Base

class Pago(Base):
    __tablename__ = "pagos"

    id = Column(Integer, primary_key=True, index=True)
    pedido_id = Column(Integer, nullable=False, index=True)
    monto = Column(Float, nullable=False)
    estado = Column(String, nullable=False)  # "aprobado" o "rechazado"
    creado_en = Column(DateTime, default=datetime.utcnow)