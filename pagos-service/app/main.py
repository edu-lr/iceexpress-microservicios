from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session

from app import models, schemas, crud, security
from app.database import engine, get_db
from app.logging_config import configurar_logging

configurar_logging()

# Crea las tablas en la base de datos si no existen al iniciar el servicio.
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Pagos Service - IceExpress")

# Endpoint de verificación de salud para monitorear que el servicio de pagos está activo.
@app.get("/")
def health_check():
    return {"status": "ok", "service": "pagos-service"}

# Procesa y registra un nuevo pago en el sistema. Valida los datos y guarda el resultado en la BD.
@app.post("/pagos", response_model=schemas.PagoResponse, status_code=201)
def crear_pago(pago: schemas.PagoCreate, db: Session = Depends(get_db), usuario=Depends(security.verificar_token)):
    return crud.procesar_pago(db, pago)

# Obtiene una lista paginada del historial de todos los pagos registrados.
@app.get("/pagos", response_model=list[schemas.PagoResponse])
def listar_pagos(skip: int = 0, limit: int = 100, db: Session = Depends(get_db), usuario=Depends(security.verificar_token)):
    return crud.get_pagos(db, skip=skip, limit=limit)

# Obtiene los detalles de un pago específico por su ID. Lanza 404 si no existe.
@app.get("/pagos/{pago_id}", response_model=schemas.PagoResponse)
def obtener_pago(pago_id: int, db: Session = Depends(get_db), usuario=Depends(security.verificar_token)):
    pago = crud.get_pago(db, pago_id)
    if pago is None:
        raise HTTPException(status_code=404, detail="Pago no encontrado")
    return pago

# Obtiene el historial de todos los pagos asociados a un pedido específico.
@app.get("/pagos/pedido/{pedido_id}", response_model=list[schemas.PagoResponse])
def obtener_pagos_de_pedido(pedido_id: int, db: Session = Depends(get_db), usuario=Depends(security.verificar_token)):
    return crud.get_pagos_by_pedido(db, pedido_id)