from pydantic import BaseModel, EmailStr

# Lo que el cliente manda para registrarse
class UsuarioCreate(BaseModel):
    email: EmailStr
    password: str

# Lo que el cliente manda para loguearse
class UsuarioLogin(BaseModel):
    email: EmailStr
    password: str

# Lo que la API devuelve tras un registro (nunca el hash)
class UsuarioResponse(BaseModel):
    id: int
    email: EmailStr

    class Config:
        from_attributes = True

# Lo que la API devuelve tras un login exitoso
class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"