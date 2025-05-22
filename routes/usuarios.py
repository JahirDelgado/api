from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, EmailStr, Field
from database import db

router = APIRouter(prefix="/usuarios", tags=["Usuarios"])
usuarios_collection = db["cuentas_usuario"]

class Usuario(BaseModel):
    nombre: str = Field(..., example="Juan Perez")
    correo: EmailStr = Field(..., example="juan@mail.com")
    contrasena: str = Field(..., min_length=8, example="12345678")

@router.post("/")
async def crear_usuario(usuario: Usuario):
    # Verificar si ya existe correo o nombre
    if usuarios_collection.find_one({"correo": usuario.correo}):
        raise HTTPException(status_code=400, detail="El correo ya está registrado")
    if usuarios_collection.find_one({"nombre": usuario.nombre}):
        raise HTTPException(status_code=400, detail="El nombre ya está registrado")

    try:
        usuarios_collection.insert_one(usuario.dict())
        return {"message": "Usuario registrado exitosamente"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al registrar usuario: {e}")
