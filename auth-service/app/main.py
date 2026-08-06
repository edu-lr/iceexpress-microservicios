from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from app.logging_config import configurar_logging

from app import models, schemas, crud, security
from app.database import engine, get_db

configurar_logging()

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Auth Service - IceExpress")

@app.get("/")
def health_check():
    return {"status": "ok", "service": "auth-service"}

@app.post("/registro", response_model=schemas.UsuarioResponse, status_code=201)
def registrar_usuario(usuario: schemas.UsuarioCreate, db: Session = Depends(get_db)):
    nuevo_usuario = crud.crear_usuario(db, usuario)
    if nuevo_usuario is None:
        raise HTTPException(status_code=409, detail="Ya existe un usuario con ese email")
    return nuevo_usuario

@app.post("/login", response_model=schemas.Token)
def login(credenciales: schemas.UsuarioLogin, db: Session = Depends(get_db)):
    usuario = crud.autenticar_usuario(db, credenciales.email, credenciales.password)
    if usuario is None:
        raise HTTPException(status_code=401, detail="Email o contraseña incorrectos")

    token = security.crear_access_token(data={"sub": usuario.email, "user_id": usuario.id})
    return {"access_token": token, "token_type": "bearer"}