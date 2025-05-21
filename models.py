from pydantic import BaseModel, EmailStr

class UserLogin(BaseModel):
    correo: str
    contrasena: str

class UserInfo(BaseModel):
    nombre: str
    posicion: str

class CitaCreate(BaseModel):
    name: str
    service: str
    professional: str
    date: str
    time: str
    phone: str = "manual"
    status: str = "manual"
