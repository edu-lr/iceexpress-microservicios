from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from app.logging_config import configurar_logging
from app import models, schemas, crud, security
from app.database import engine, get_db

configurar_logging()

# Crea las tablas en la base de datos si no existen (basándose en models.py)
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Productos Service - IceExpress")


# Endpoint de verificación de salud para monitoreo.
@app.get("/")
def health_check():
    return {"status": "ok", "service": "productos-service"}


# Crea un nuevo producto en el catálogo con los datos validados.
@app.post("/productos", response_model=schemas.ProductoResponse, status_code=201)
def crear_producto(producto: schemas.ProductoCreate, db: Session = Depends(get_db), usuario=Depends(security.verificar_token)):
    return crud.create_producto(db, producto)


# Obtiene una lista paginada de todos los productos.
@app.get("/productos", response_model=list[schemas.ProductoResponse])
def listar_productos(skip: int = 0, limit: int = 100, db: Session = Depends(get_db), usuario=Depends(security.verificar_token)):
    return crud.get_productos(db, skip=skip, limit=limit)


# Obtiene un producto específico por su ID. Lanza 404 si no existe.
@app.get("/productos/{producto_id}", response_model=schemas.ProductoResponse)
def obtener_producto(producto_id: int, db: Session = Depends(get_db), usuario=Depends(security.verificar_token)):
    db_producto = crud.get_producto(db, producto_id)
    if db_producto is None:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    return db_producto


# Actualiza los datos de un producto existente. Lanza 404 si no existe.
@app.put("/productos/{producto_id}", response_model=schemas.ProductoResponse)
def actualizar_producto(producto_id: int, producto: schemas.ProductoUpdate, db: Session = Depends(get_db), usuario=Depends(security.verificar_token)):
    db_producto = crud.update_producto(db, producto_id, producto)
    if db_producto is None:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    return db_producto


# Elimina un producto del catálogo de forma permanente. Lanza 404 si no existe.
@app.delete("/productos/{producto_id}", status_code=204)
def eliminar_producto(producto_id: int, db: Session = Depends(get_db), usuario=Depends(security.verificar_token)):
    db_producto = crud.delete_producto(db, producto_id)
    if db_producto is None:
        raise HTTPException(status_code=404, detail="Producto no encontrado")