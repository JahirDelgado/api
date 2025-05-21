from pydantic import BaseModel, EmailStr

class UserLogin(BaseModel):
    correo: EmailStr
    contrasena: str

class UserInfo(BaseModel):
    nombre: str
    posicion: str
