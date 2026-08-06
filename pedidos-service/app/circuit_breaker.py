import time
import logging

logger = logging.getLogger("circuit_breaker")


class CircuitBreaker:
    def __init__(self, nombre: str, umbral_fallos: int = 3, tiempo_espera: int = 30):
        self.nombre = nombre
        self.umbral_fallos = umbral_fallos
        self.tiempo_espera = tiempo_espera
        self.fallos = 0
        self.estado = "cerrado"
        self.abierto_desde = None

    def permitir_llamada(self) -> bool:
        if self.estado == "cerrado":
            return True

        if self.estado == "abierto":
            if time.time() - self.abierto_desde >= self.tiempo_espera:
                self.estado = "semi-abierto"
                logger.warning(f"[{self.nombre}] Circuito pasa a SEMI-ABIERTO, probando de nuevo")
                return True
            return False

        return True  # semi-abierto: deja pasar la llamada de prueba

    def registrar_exito(self):
        if self.estado != "cerrado":
            logger.info(f"[{self.nombre}] Circuito vuelve a CERRADO")
        self.fallos = 0
        self.estado = "cerrado"

    def registrar_fallo(self):
        self.fallos += 1
        if self.estado == "semi-abierto":
            self.estado = "abierto"
            self.abierto_desde = time.time()
            logger.error(f"[{self.nombre}] La prueba falló, circuito vuelve a ABIERTO")
        elif self.fallos >= self.umbral_fallos:
            self.estado = "abierto"
            self.abierto_desde = time.time()
            logger.error(f"[{self.nombre}] {self.fallos} fallos seguidos, circuito ABIERTO")