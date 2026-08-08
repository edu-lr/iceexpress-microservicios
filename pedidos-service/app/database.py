import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from dotenv import load_dotenv

# Carga las variables de entorno desde el archivo .env.
load_dotenv()

# URL de conexión a la base de datos (con valor por defecto para desarrollo local).
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://user:pass@localhost:5432/pedidos_db")

# Crea el motor de conexión que gestiona los pools de conexiones a la BD.
engine = create_engine(DATABASE_URL)

# Fábrica de sesiones que crea las conexiones para ejecutar las transacciones.
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Clase base declarativa que servirá de molde para definir las tablas (modelos).
Base = declarative_base()


# Generador de dependencia de FastAPI: abre una sesión y la cierra automáticamente al finalizar la petición.
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()