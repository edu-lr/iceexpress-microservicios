from sqlalchemy.orm import Session
from app import models, schemas, security


# Busca un usuario en la base de datos por su correo electrónico.
def get_usuario_by_email(db: Session, email: str):
    return db.query(models.Usuario).filter(models.Usuario.email == email).first()


# Hashea la contraseña, verifica que el email no esté registrado y guarda el nuevo usuario. Retorna None si el email ya existe.
def crear_usuario(db: Session, usuario: schemas.UsuarioCreate):
    existente = get_usuario_by_email(db, usuario.email)
    if existente is not None:
        return None

    nuevo_usuario = models.Usuario(
        email=usuario.email,
        password_hash=security.hashear_password(usuario.password)
    )
    db.add(nuevo_usuario)
    db.commit()
    db.refresh(nuevo_usuario)
    return nuevo_usuario


# Busca al usuario por email y valida su contraseña. Retorna el objeto usuario si las credenciales son válidas, o None si falla.
def autenticar_usuario(db: Session, email: str, password: str):
    usuario = get_usuario_by_email(db, email)
    if usuario is None:
        return None
    if not security.verificar_password(password, usuario.password_hash):
        return None
    return usuario