from app.logging_config import configurar_logging
from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials
from sqlalchemy.orm import Session

from app import models, schemas, crud, security
from app.database import engine, get_db

configurar_logging()

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Pedidos Service - IceExpress")

@app.get("/")
def health_check():
    return {"status": "ok", "service": "pedidos-service"}

@app.post("/pedidos", response_model=schemas.PedidoResponse, status_code=201)
def crear_pedido(
    pedido: schemas.PedidoCreate, 
    db: Session = Depends(get_db),
    payload=Depends(security.verificar_token),
    credentials: HTTPAuthorizationCredentials = Depends(security.bearer_scheme)
):  
    token = credentials.credentials
    nuevo_pedido, error, status_code = crud.crear_pedido(db, pedido, token)
    if nuevo_pedido is None:
        raise HTTPException(status_code=status_code, detail=error)
    return nuevo_pedido

@app.get("/pedidos", response_model=list[schemas.PedidoResponse])
def listar_pedidos(skip: int = 0, limit: int = 100, db: Session = Depends(get_db), usuario=Depends(security.verificar_token)):
    return crud.get_pedidos(db, skip=skip, limit=limit)

@app.get("/pedidos/{pedido_id}", response_model=schemas.PedidoResponse)
def obtener_pedido(pedido_id: int, db: Session = Depends(get_db), usuario=Depends(security.verificar_token)):
    pedido = crud.get_pedido(db, pedido_id)
    if pedido is None:
        raise HTTPException(status_code=404, detail="Pedido no encontrado")
    return pedido