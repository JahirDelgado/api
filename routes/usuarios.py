from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, EmailStr, Field
from database import db, cuentas_usuario_collection
from typing import List

router = APIRouter(tags=["Usuarios"])

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
def crear_usuario(usuario: Usuario):
    if cuentas_usuario_collection.find_one({"correo": usuario.correo}):
        raise HTTPException(status_code=400, detail="El correo ya está registrado")
    if cuentas_usuario_collection.find_one({"nombre": usuario.nombre}):
        raise HTTPException(status_code=400, detail="El nombre ya está registrado")
    cuentas_usuario_collection.insert_one(usuario.dict())
    return {"message": "Usuario registrado exitosamente"}

# Ruta GET para listar servicios
@router.get("/servicios", response_model=List[Servicio])
def listar_servicios():
    servicios = []
    cursor = servicios_collection.find({})
    for servicio in cursor:
        servicios.append(Servicio(**servicio))
    return servicios

# Ruta POST para guardar servicios asignados a un usuario
@router.post("/servicios")
def guardar_servicios_usuario(data: ServiciosAsignadosUsuario):
    usuario = cuentas_usuario_collection.find_one({"correo": data.correo})
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    servicios_asignados_collection.delete_many({"correo": data.correo})

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
        resultado = servicios_asignados_collection.insert_many(servicios_docs)
        if resultado.inserted_ids:
            return {"mensaje": "Servicios asignados guardados correctamente"}

    raise HTTPException(status_code=500, detail="Error al guardar servicios asignados")


@router.post("/servicios/nuevo")
def crear_servicio(servicio: Servicio):
    if servicios_collection.find_one({"nombreServicio": servicio.nombreServicio}):
        raise HTTPException(status_code=400, detail="El servicio ya existe")
    servicios_collection.insert_one(servicio.dict())
    return {"mensaje": "Servicio creado exitosamente"}
