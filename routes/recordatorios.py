from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel, Field
from database import db

router = APIRouter(prefix="/recordatorios", tags=["Recordatorios"])

# Accedemos a la colección Recordatorios desde db
servicios_collection = db["Recordatorios"]

class Recordatorio(BaseModel):
    nombreServicio: str = Field(..., example="Luz")
    vencimiento: str = Field("", example="25/05/25")
    fechaCorte: str = Field("", example="27/05/25")
    monto: str = Field("", example="100")
    nombre: str = Field(..., example="Juan")

@router.get("/")
async def listar_recordatorios(nombre: str = Query(..., description="Nombre del usuario")):
    try:
        servicios = list(servicios_collection.find({"nombre": nombre}, {"_id": 0}))
        return servicios
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al obtener recordatorios: {e}")

@router.post("/")
async def agregar_recordatorio(recordatorio: Recordatorio):
    existente = servicios_collection.find_one({
        "nombreServicio": recordatorio.nombreServicio,
        "nombre": recordatorio.nombre
    })

    if existente:
        raise HTTPException(status_code=400, detail="El servicio ya existe para este usuario")

    try:
        servicios_collection.insert_one(recordatorio.dict())
        return {"message": "Servicio agregado exitosamente"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al guardar el servicio: {e}")

@router.delete("/{nombre_servicio}")
async def eliminar_recordatorio(nombre_servicio: str, nombre: str = Query(..., description="Nombre del usuario")):
    resultado = servicios_collection.delete_one({
        "nombreServicio": nombre_servicio,
        "nombre": nombre
    })

    if resultado.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Servicio no encontrado o no pertenece al usuario")

    return {"message": "Servicio eliminado correctamente"}
