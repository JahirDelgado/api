from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, EmailStr, Field
from database import db  # asumo que es motor async
from typing import List

router = APIRouter(prefix="/usuarios", tags=["Usuarios"])

usuarios_collection = db["cuentas_usuario"]
servicios_collection = db["servicios"]
servicios_asignados_collection = db["usuarios"]  # colección donde guardas servicios asignados

# Modelos Pydantic

class Servicio(BaseModel):
    nombreServicio: str = Field(..., example="Corte de cabello")
    duracion: str = Field(..., example="30")

class ServiciosAsignadosUsuario(BaseModel):
    correo: EmailStr
    nombre: str
    posicion: str = Field("empleado", example="empleado")
    servicios: List[str] = Field(..., example=["Corte de cabello", "Manicure"])

# Ruta para obtener todos los servicios disponibles
@router.get("/servicios", response_model=List[Servicio])
async def listar_servicios():
    servicios = []
    cursor = servicios_collection.find({})
    async for servicio in cursor:
        servicios.append(Servicio(**servicio))
    return servicios

# Ruta para asignar servicios a un usuario
@router.post("/servicios")
async def guardar_servicios_usuario(data: ServiciosAsignadosUsuario):
    # Validar que usuario exista en cuentas_usuario
    usuario = await usuarios_collection.find_one({"correo": data.correo})
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    # Eliminar servicios asignados previos de este usuario
    await servicios_asignados_collection.delete_many({"correo": data.correo})

    # Insertar servicios asignados
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
