from fastapi import APIRouter, HTTPException
from db import db
from models import LoginRequest, UsuarioInfo

router = APIRouter()

@router.post("/login", response_model=UsuarioInfo)
def login_user(login: LoginRequest):
    cuentas_usuario = db["cuentas_usuario"]
    usuarios = db["usuarios"]

    cuenta = cuentas_usuario.find_one({
        "correo": login.correo,
        "contrasena": login.contrasena
    })

    if not cuenta:
        raise HTTPException(status_code=401, detail="Correo o contraseña incorrectos")

    usuario = usuarios.find_one({"nombre": cuenta["nombre"]})

    if not usuario:
        raise HTTPException(status_code=404, detail="No se encontró el usuario")

    return UsuarioInfo(nombre=cuenta["nombre"], posicion=usuario["posicion"])