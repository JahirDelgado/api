from pydantic import BaseModel, EmailStr

class UserLogin(BaseModel):
    correo: str
    contrasena: str

class UserInfo(BaseModel):
    nombre: str
    posicion: str
