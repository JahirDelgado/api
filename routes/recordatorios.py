from fastapi import APIRouter, HTTPException, Query
from database import db

router = APIRouter(prefix="/recordatorios", tags=["Recordatorios"])

# Accedemos a la colección Recordatorios desde db
servicios_collection = db["Recordatorios"]

@router.get("/")
async def listar_recordatorios(nombre: str = Query(..., description="Nombre del usuario")):
    try:
        servicios = list(servicios_collection.find({"nombre": nombre}, {"_id": 0}))
        return servicios
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al obtener recordatorios: {e}")

@router.delete("/{nombre_servicio}")
async def eliminar_recordatorio(nombre_servicio: str, nombre: str = Query(..., description="Nombre del usuario")):
    resultado = servicios_collection.delete_one({
        "nombreServicio": nombre_servicio,
        "nombre": nombre
    })

    if resultado.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Servicio no encontrado o no pertenece al usuario")

    return {"message": "Servicio eliminado correctamente"}
