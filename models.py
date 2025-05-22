from pydantic import BaseModel, EmailStr
from typing import Optional

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
    phone: str
    status: str
