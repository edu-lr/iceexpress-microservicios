from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from app.logging_config import configurar_logging

from app import models, schemas, crud, security
from app.database import engine, get_db

configurar_logging()

# Crea las tablas en la base de datos si no existen
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Inventario Service - IceExpress")

@app.get("/")
def health_check():
    return {"status": "ok", "service": "inventario-service"}

@app.post("/inventario", response_model=schemas.InventarioResponse, status_code=201)
def crear_inventario(inventario: schemas.InventarioCreate, db: Session = Depends(get_db), usuario=Depends(security.verificar_token)):
    nuevo = crud.create_inventario(db, inventario)
    if nuevo is None:
        raise HTTPException(status_code=409, detail="Ya existe un registro de inventario para ese producto")
    return nuevo

@app.get("/inventario", response_model=list[schemas.InventarioResponse])
def listar_inventario(skip: int = 0, limit: int = 100, db: Session = Depends(get_db), usuario=Depends(security.verificar_token)):
    return crud.get_todo_inventario(db, skip=skip, limit=limit)

@app.get("/inventario/{producto_id}", response_model=schemas.InventarioResponse)
def obtener_inventario(producto_id: int, db: Session = Depends(get_db), usuario=Depends(security.verificar_token)):
    item = crud.get_inventario_by_producto(db, producto_id)
    if item is None:
        raise HTTPException(status_code=404, detail="No hay registro de inventario para ese producto")
    return item

@app.put("/inventario/{producto_id}", response_model=schemas.InventarioResponse)
def actualizar_inventario(producto_id: int, datos: schemas.InventarioUpdate, db: Session = Depends(get_db), usuario=Depends(security.verificar_token)):
    item = crud.actualizar_cantidad(db, producto_id, datos.cantidad)
    if item is None:
        raise HTTPException(status_code=404, detail="No hay registro de inventario para ese producto")
    return item

@app.post("/inventario/{producto_id}/descontar", response_model=schemas.InventarioResponse)
def descontar_inventario(producto_id: int, cantidad: int, db: Session = Depends(get_db), usuario=Depends(security.verificar_token)):
    item = crud.descontar_stock(db, producto_id, cantidad)
    if item is None:
        raise HTTPException(status_code=400, detail="Stock insuficiente o producto no encontrado")
    return item

@app.post("/inventario/{producto_id}/reponer", response_model=schemas.InventarioResponse)
def reponer_inventario(producto_id: int, cantidad: int, db: Session = Depends(get_db), usuario=Depends(security.verificar_token)):
    item = crud.reponer_stock(db, producto_id, cantidad)
    if item is None:
        raise HTTPException(status_code=404, detail="No hay registro de inventario para ese producto")
    return item