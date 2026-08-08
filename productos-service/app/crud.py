from sqlalchemy.orm import Session
from app import models, schemas

# Busca un producto en la BD por su ID.
def get_producto(db: Session, producto_id: int):
    return db.query(models.Producto).filter(models.Producto.id == producto_id).first()

# Obtiene una lista paginada de productos.
def get_productos(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Producto).offset(skip).limit(limit).all()

# Inserta un nuevo producto en la base de datos.
def create_producto(db: Session, producto: schemas.ProductoCreate):
    nuevo_producto = models.Producto(
        nombre=producto.nombre,
        tipo_hielo=producto.tipo_hielo,
        precio=producto.precio,
        descripcion=producto.descripcion
    )
    db.add(nuevo_producto)
    db.commit()
    db.refresh(nuevo_producto)
    return nuevo_producto

# Actualiza los datos de un producto existente.
def update_producto(db: Session, producto_id: int, producto: schemas.ProductoUpdate):
    db_producto = get_producto(db, producto_id)
    if db_producto is None:
        return None

    datos_actualizados = producto.model_dump(exclude_unset=True)
    for campo, valor in datos_actualizados.items():
        setattr(db_producto, campo, valor)

    db.commit()
    db.refresh(db_producto)
    return db_producto

# Elimina un producto de la base de datos por su ID.
def delete_producto(db: Session, producto_id: int):
    db_producto = get_producto(db, producto_id)
    if db_producto is None:
        return None

    db.delete(db_producto)
    db.commit()
    return db_producto