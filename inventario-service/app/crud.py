from sqlalchemy.orm import Session
from app import models, schemas

def get_inventario_by_producto(db: Session, producto_id: int):
    return db.query(models.Inventario).filter(models.Inventario.producto_id == producto_id).first()

def get_todo_inventario(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Inventario).offset(skip).limit(limit).all()

def create_inventario(db: Session, inventario: schemas.InventarioCreate):
    existente = get_inventario_by_producto(db, inventario.producto_id)
    if existente is not None:
        return None

    nuevo = models.Inventario(
        producto_id=inventario.producto_id,
        cantidad=inventario.cantidad
    )
    db.add(nuevo)
    db.commit()
    db.refresh(nuevo)
    return nuevo

def actualizar_cantidad(db: Session, producto_id: int, cantidad: int):
    item = get_inventario_by_producto(db, producto_id)
    if item is None:
        return None
    item.cantidad = cantidad
    db.commit()
    db.refresh(item)
    return item

def descontar_stock(db: Session, producto_id: int, cantidad: int):
    item = get_inventario_by_producto(db, producto_id)
    if item is None or item.cantidad < cantidad:
        return None
    item.cantidad -= cantidad
    db.commit()
    db.refresh(item)
    return item

def reponer_stock(db: Session, producto_id: int, cantidad: int):
    item = get_inventario_by_producto(db, producto_id)
    if item is None:
        return None
    item.cantidad += cantidad
    db.commit()
    db.refresh(item)
    return item