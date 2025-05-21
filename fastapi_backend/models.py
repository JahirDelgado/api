from pydantic import BaseModel

class LoginRequest(BaseModel):
    correo: str
    contrasena: str

class UsuarioInfo(BaseModel):
    nombre: str
    posicion: str