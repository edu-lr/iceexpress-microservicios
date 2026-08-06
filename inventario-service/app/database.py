import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from dotenv import load_dotenv

# Carga las variables del archivo .env
load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://user:pass@localhost:5432/inventario_db")

# El "engine" es el objeto que sabe cómo hablar con Postgres
engine = create_engine(DATABASE_URL)

# SessionLocal genera sesiones — conversaciones individuales con la base de datos
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base es la clase de la que van a heredar nuestros modelos (tablas)
Base = declarative_base()

# Se la inyectamos a FastAPI para que abra y cierre la conexión automáticamente
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()