import os
import time
import logging
import httpx
from dotenv import load_dotenv
from app.circuit_breaker import CircuitBreaker

load_dotenv()

logger = logging.getLogger("clients")

PRODUCTOS_SERVICE_URL = os.getenv("PRODUCTOS_SERVICE_URL", "http://productos-service:8000")
INVENTARIO_SERVICE_URL = os.getenv("INVENTARIO_SERVICE_URL", "http://inventario-service:8000")
PAGOS_SERVICE_URL = os.getenv("PAGOS_SERVICE_URL", "http://pagos-service:8000")

breaker_productos = CircuitBreaker("productos-service")
breaker_inventario = CircuitBreaker("inventario-service")
breaker_pagos = CircuitBreaker("pagos-service")


class ServicioNoDisponibleError(Exception):
    """Se lanza cuando hay un fallo técnico real: timeout, conexión rechazada, o 5xx."""
    pass


def _llamar_con_resiliencia(breaker: CircuitBreaker, peticion, reintentos: int = 2, espera: float = 0.5):
    if not breaker.permitir_llamada():
        logger.warning(f"[{breaker.nombre}] Circuito ABIERTO, no se intenta la llamada")
        return None

    intento = 0
    while True:
        try:
            response = peticion()
            breaker.registrar_exito()
            return response
        except ServicioNoDisponibleError:
            intento += 1
            if intento > reintentos:
                breaker.registrar_fallo()
                logger.error(f"[{breaker.nombre}] Fallo técnico tras {reintentos} reintentos")
                return None
            logger.warning(f"[{breaker.nombre}] Fallo técnico, reintentando ({intento}/{reintentos})")
            time.sleep(espera)


def obtener_producto(producto_id: int, token: str):
    headers = {"Authorization": f"Bearer {token}"}

    def _peticion():
        try:
            r = httpx.get(f"{PRODUCTOS_SERVICE_URL}/productos/{producto_id}", headers=headers, timeout=5.0)
        except httpx.RequestError:
            raise ServicioNoDisponibleError()
        if r.status_code >= 500:
            raise ServicioNoDisponibleError()
        return r

    response = _llamar_con_resiliencia(breaker_productos, _peticion)
    if response is None or response.status_code != 200:
        return None
    return response.json()


def descontar_stock(producto_id: int, cantidad: int, token: str) -> bool:
    headers = {"Authorization": f"Bearer {token}"}

    def _peticion():
        try:
            r = httpx.post(
                f"{INVENTARIO_SERVICE_URL}/inventario/{producto_id}/descontar",
                params={"cantidad": cantidad}, headers=headers, timeout=5.0
            )
        except httpx.RequestError:
            raise ServicioNoDisponibleError()
        if r.status_code >= 500:
            raise ServicioNoDisponibleError()
        return r

    response = _llamar_con_resiliencia(breaker_inventario, _peticion)
    if response is None:
        return False
    return response.status_code == 200


def reponer_stock(producto_id: int, cantidad: int, token: str) -> bool:
    headers = {"Authorization": f"Bearer {token}"}

    def _peticion():
        try:
            r = httpx.post(
                f"{INVENTARIO_SERVICE_URL}/inventario/{producto_id}/reponer",
                params={"cantidad": cantidad}, headers=headers, timeout=5.0
            )
        except httpx.RequestError:
            raise ServicioNoDisponibleError()
        if r.status_code >= 500:
            raise ServicioNoDisponibleError()
        return r

    response = _llamar_con_resiliencia(breaker_inventario, _peticion)
    if response is None:
        return False
    return response.status_code == 200


def procesar_pago(pedido_id: int, monto: float, token: str) -> bool:
    headers = {"Authorization": f"Bearer {token}"}

    def _peticion():
        try:
            r = httpx.post(
                f"{PAGOS_SERVICE_URL}/pagos",
                json={"pedido_id": pedido_id, "monto": monto}, headers=headers, timeout=5.0
            )
        except httpx.RequestError:
            raise ServicioNoDisponibleError()
        if r.status_code >= 500:
            raise ServicioNoDisponibleError()
        return r

    response = _llamar_con_resiliencia(breaker_pagos, _peticion)
    if response is None or response.status_code != 201:
        return False
    return response.json()["estado"] == "aprobado"