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
    date: str  # formato: "dd/mm/yyyy"
    time: str  # formato: "HH:MM"
    phone: Optional[str] = "manual"
    status: str = "manual"
