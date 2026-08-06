import random
from sqlalchemy.orm import Session
from app import models, schemas

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

def get_pago(db: Session, pago_id: int):
    return db.query(models.Pago).filter(models.Pago.id == pago_id).first()

def get_pagos(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Pago).offset(skip).limit(limit).all()

def get_pagos_by_pedido(db: Session, pedido_id: int):
    return db.query(models.Pago).filter(models.Pago.pedido_id == pedido_id).all()