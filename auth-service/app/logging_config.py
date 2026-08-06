import logging
import sys

def configurar_logging():
    formato = "%(asctime)s | %(levelname)-8s | %(name)s | %(message)s"
    fecha_formato = "%Y-%m-%d %H:%M:%S"

    logging.basicConfig(
        level=logging.INFO,
        format=formato,
        datefmt=fecha_formato,
        handlers=[logging.StreamHandler(sys.stdout)]
    )