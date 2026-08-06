from sqlalchemy.orm import Session
from app import models, schemas, clients


def crear_pedido(db: Session, pedido: schemas.PedidoCreate, token: str):
    items_creados = []
    items_descontados = []
    total = 0.0

    for item in pedido.items:
        producto = clients.obtener_producto(item.producto_id, token)
        if producto is None:
            _revertir(items_descontados, token)
            return None, f"El producto {item.producto_id} no existe o no está disponible", 400

        precio = producto["precio"]
        descontado = clients.descontar_stock(item.producto_id, item.cantidad, token)
        if not descontado:
            _revertir(items_descontados, token)
            return None, f"Stock insuficiente para el producto {item.producto_id}", 400

        items_descontados.append((item.producto_id, item.cantidad))
        items_creados.append(models.PedidoItem(
            producto_id=item.producto_id, cantidad=item.cantidad, precio_unitario=precio
        ))
        total += precio * item.cantidad

    # Creamos el pedido YA (estado provisorio) para tener un id real antes de cobrar
    nuevo_pedido = models.Pedido(estado="pendiente_pago", total=total, items=items_creados)
    db.add(nuevo_pedido)
    db.commit()
    db.refresh(nuevo_pedido)

    if not clients.procesar_pago(nuevo_pedido.id, total, token):
        nuevo_pedido.estado = "rechazado"
        db.commit()
        _revertir(items_descontados, token)
        return None, "El pago fue rechazado", 402

    nuevo_pedido.estado = "confirmado"
    db.commit()
    db.refresh(nuevo_pedido)
    return nuevo_pedido, None, None


def _revertir(items_descontados, token: str):
    """Compensación: repone el stock de los ítems que ya se habían descontado."""
    for producto_id, cantidad in items_descontados:
        clients.reponer_stock(producto_id, cantidad, token)


def get_pedido(db: Session, pedido_id: int):
    return db.query(models.Pedido).filter(models.Pedido.id == pedido_id).first()


def get_pedidos(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Pedido).offset(skip).limit(limit).all()