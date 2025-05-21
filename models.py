from pydantic import BaseModel, EmailStr

class UserLogin(BaseModel):
    correo: Str
    contrasena: str

class UserInfo(BaseModel):
    nombre: str
    posicion: str
