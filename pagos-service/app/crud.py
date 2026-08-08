import random
from sqlalchemy.orm import Session
from app import models, schemas

# Registra el intento de pago en la BD, simula el resultado (aprobado/rechazado) y guarda el estado final.
def procesar_pago(db: Session, pago: schemas.PagoCreate):
    exito = random.random() < 0.85  # 85% de aprobación simulada
    estado = "aprobado" if exito else "rechazado"

    nuevo_pago = models.Pago(
        pedido_id=pago.pedido_id,
        monto=pago.monto,
        estado=estado
    )
    db.add(nuevo_pago)
    db.commit()
    db.refresh(nuevo_pago)
    return nuevo_pago

# Obtiene un pago específico de la base de datos por su ID. Retorna None si no existe.
def get_pago(db: Session, pago_id: int):
    return db.query(models.Pago).filter(models.Pago.id == pago_id).first()

# Obtiene una lista paginada de todos los pagos registrados en el sistema.
def get_pagos(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Pago).offset(skip).limit(limit).all()

# Obtiene todos los pagos asociados a un ID de pedido específico (historial del pedido).
def get_pagos_by_pedido(db: Session, pedido_id: int):
    return db.query(models.Pago).filter(models.Pago.pedido_id == pedido_id).all()