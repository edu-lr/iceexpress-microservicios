import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from dotenv import load_dotenv

# Carga las variables del archivo .env
load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://user:pass@localhost:5432/productos_db")

# Crea el motor de conexión que administra los pools de conexiones a la BD.
engine = create_engine(DATABASE_URL)

# SessionLocal genera "sesiones" — conversaciones individuales con la base de datos
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base es la clase de la que van a heredar todos nuestros modelos (tablas)
Base = declarative_base()

# Esta función se la vamos a inyectar a FastAPI para que abra y cierre la conexión automáticamente
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()