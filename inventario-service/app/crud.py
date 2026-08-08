from sqlalchemy.orm import Session
from app import models, schemas

# Busca el registro de inventario asociado a un producto_id específico.
def get_inventario_by_producto(db: Session, producto_id: int):
    return db.query(models.Inventario).filter(models.Inventario.producto_id == producto_id).first()

# Obtiene una lista paginada de todos los registros de inventario.
def get_todo_inventario(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Inventario).offset(skip).limit(limit).all()

# Inserta un nuevo registro de inventario. Retorna None si ya existe un registro para ese producto.
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

# Sobrescribe manualmente la cantidad exacta de stock para un producto. Retorna None si el producto no existe.
def actualizar_cantidad(db: Session, producto_id: int, cantidad: int):
    item = get_inventario_by_producto(db, producto_id)
    if item is None:
        return None
    item.cantidad = cantidad
    db.commit()
    db.refresh(item)
    return item

# Reduce el stock de un producto. Retorna None si el producto no existe o si el stock actual es insuficiente.
def descontar_stock(db: Session, producto_id: int, cantidad: int):
    item = get_inventario_by_producto(db, producto_id)
    if item is None or item.cantidad < cantidad:
        return None
    item.cantidad -= cantidad
    db.commit()
    db.refresh(item)
    return item

# Aumenta el stock de un producto (para devoluciones o compensaciones). Retorna None si el producto no existe.
def reponer_stock(db: Session, producto_id: int, cantidad: int):
    item = get_inventario_by_producto(db, producto_id)
    if item is None:
        return None
    item.cantidad += cantidad
    db.commit()
    db.refresh(item)
    return item