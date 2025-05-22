from pydantic import BaseModel, EmailStr
from typing import Optional, List

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
    date: str  # dd/mm/yyyy
    time: str  # HH:MM
    phone: Optional[str] = None
    status: Optional[str] = "manual"

class ServicioInfo(BaseModel):
    nombreServicio: str

# Si quieres validar listas de servicios (por ejemplo, en get_servicios):
class ServiciosResponse(BaseModel):
    servicios: List[ServicioInfo]
