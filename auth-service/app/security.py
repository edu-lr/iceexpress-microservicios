import os
from datetime import datetime, timedelta
from jose import jwt, JWTError
from passlib.context import CryptContext
from dotenv import load_dotenv

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 30))

# Contexto de hashing para gestionar la encriptación de contraseñas con bcrypt.
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Toma una contraseña en texto plano y devuelve su hash seguro utilizando bcrypt.
def hashear_password(password: str) -> str:
    return pwd_context.hash(password)

# Compara una contraseña en texto plano contra un hash guardado, retorna True si coinciden.
def verificar_password(password_plano: str, password_hash: str) -> bool:
    return pwd_context.verify(password_plano, password_hash)

# Crea un nuevo token JWT con el payload, agregando la fecha de expiración calculada.
def crear_access_token(data: dict) -> str:
    to_encode = data.copy()
    expira = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expira})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

# Decodifica y valida un token JWT. Retorna el payload si es válido, o None si expiró o es inválido.
def decodificar_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        return None