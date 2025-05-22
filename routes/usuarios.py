from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, EmailStr, Field
from database import db
from typing import List

router = APIRouter(prefix="/usuarios", tags=["Usuarios"])

usuarios_collection = db["cuentas_usuario"]
servicios_collection = db["servicios"]
servicios_asignados_collection = db["usuarios"]

# Modelo para crear usuario
class Usuario(BaseModel):
    nombre: str = Field(..., example="Juan Perez")
    correo: EmailStr = Field(..., example="juan@mail.com")
    contrasena: str = Field(..., min_length=8, example="12345678")

class Servicio(BaseModel):
    nombreServicio: str = Field(..., example="Corte de cabello")
    duracion: str = Field(..., example="30")

class ServiciosAsignadosUsuario(BaseModel):
    correo: EmailStr
    nombre: str
    posicion: str = Field("empleado", example="empleado")
    servicios: List[str] = Field(..., example=["Corte de cabello", "Manicure"])

# Ruta POST para crear usuario
@router.post("/")
async def crear_usuario(usuario: Usuario):
    if await usuarios_collection.find_one({"correo": usuario.correo}):
        raise HTTPException(status_code=400, detail="El correo ya está registrado")
    if await usuarios_collection.find_one({"nombre": usuario.nombre}):
        raise HTTPException(status_code=400, detail="El nombre ya está registrado")
    await usuarios_collection.insert_one(usuario.dict())
    return {"message": "Usuario registrado exitosamente"}

# Rutas ya existentes para servicios
@router.get("/servicios", response_model=List[Servicio])
async def listar_servicios():
    servicios = []
    cursor = servicios_collection.find({})
    async for servicio in cursor:
        servicios.append(Servicio(**servicio))
    return servicios

@router.post("/servicios")
async def guardar_servicios_usuario(data: ServiciosAsignadosUsuario):
    usuario = await usuarios_collection.find_one({"correo": data.correo})
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    await servicios_asignados_collection.delete_many({"correo": data.correo})

    servicios_docs = [
        {
            "correo": data.correo,
            "nombre": data.nombre,
            "posicion": data.posicion,
            "servicio": servicio_nombre
        }
        for servicio_nombre in data.servicios
    ]

    if servicios_docs:
        resultado = await servicios_asignados_collection.insert_many(servicios_docs)
        if resultado.inserted_ids:
            return {"mensaje": "Servicios asignados guardados correctamente"}
    
    raise HTTPException(status_code=500, detail="Error al guardar servicios asignados")
