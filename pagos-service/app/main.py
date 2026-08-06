from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session

from app import models, schemas, crud, security
from app.database import engine, get_db
from app.logging_config import configurar_logging

configurar_logging()

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Pagos Service - IceExpress")

@app.get("/")
def health_check():
    return {"status": "ok", "service": "pagos-service"}

@app.post("/pagos", response_model=schemas.PagoResponse, status_code=201)
def crear_pago(pago: schemas.PagoCreate, db: Session = Depends(get_db), usuario=Depends(security.verificar_token)):
    return crud.procesar_pago(db, pago)

@app.get("/pagos", response_model=list[schemas.PagoResponse])
def listar_pagos(skip: int = 0, limit: int = 100, db: Session = Depends(get_db), usuario=Depends(security.verificar_token)):
    return crud.get_pagos(db, skip=skip, limit=limit)

@app.get("/pagos/{pago_id}", response_model=schemas.PagoResponse)
def obtener_pago(pago_id: int, db: Session = Depends(get_db), usuario=Depends(security.verificar_token)):
    pago = crud.get_pago(db, pago_id)
    if pago is None:
        raise HTTPException(status_code=404, detail="Pago no encontrado")
    return pago

@app.get("/pagos/pedido/{pedido_id}", response_model=list[schemas.PagoResponse])
def obtener_pagos_de_pedido(pedido_id: int, db: Session = Depends(get_db), usuario=Depends(security.verificar_token)):
    return crud.get_pagos_by_pedido(db, pedido_id)