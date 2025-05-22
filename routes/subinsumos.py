from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List
from database import db

router = APIRouter(tags=["Subinsumos"])
subinsumos_collection = db["subinsumos"]

class Subinsumo(BaseModel):
    nombre: str
    insumo: str
    nombre_usuario: str
    cantidad: int
    unitario: float
    total: float
    minimo: int

@router.get("/subinsumos/{nombre_usuario}/{insumo}", response_model=List[Subinsumo])
def obtener_subinsumos(nombre_usuario: str, insumo: str):
    try:
        subinsumos = list(subinsumos_collection.find(
            {"nombre_usuario": nombre_usuario, "insumo": insumo},
            {"_id": 0}
        ))
        return subinsumos
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al obtener subinsumos: {str(e)}")

class ActualizarSubinsumo(BaseModel):
    cantidad: int
    total: float

@router.patch("/subinsumos/{nombre_usuario}/{insumo}/{nombre}")
def actualizar_subinsumo(nombre_usuario: str, insumo: str, nombre: str, datos: ActualizarSubinsumo):
    try:
        result = subinsumos_collection.update_one(
            {"nombre_usuario": nombre_usuario, "insumo": insumo, "nombre": nombre},
            {"$set": {"cantidad": datos.cantidad, "total": datos.total}}
        )
        if result.modified_count == 0:
            raise HTTPException(status_code=404, detail="Subinsumo no encontrado o sin cambios")
        return {"mensaje": "Subinsumo actualizado correctamente"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al actualizar subinsumo: {str(e)}")


class Subinsumo(BaseModel):
    insumo: str
    nombre_usuario: str
    nombre: str
    cantidad: int
    total: float
    unitario: float
    minimo: int

# POST - Crear nuevo subinsumo
@router.post("/subinsumos")
def crear_subinsumo(subinsumo: Subinsumo):
    try:
        existente = subinsumos_collection.find_one({
            "insumo": subinsumo.insumo,
            "nombre_usuario": subinsumo.nombre_usuario,
            "nombre": subinsumo.nombre
        })

        if existente:
            raise HTTPException(status_code=400, detail=f"{subinsumo.nombre} ya existe.")

        subinsumos_collection.insert_one(subinsumo.dict())
        return {"message": "Subinsumo creado con éxito."}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al crear subinsumo: {str(e)}")


@router.get("/subinsumos/{nombre_usuario}/{insumo}/{nombre}", response_model=Subinsumo)
def obtener_subinsumo(nombre_usuario: str, insumo: str, nombre: str):
    try:
        sub = subinsumos_collection.find_one({
            "nombre_usuario": nombre_usuario,
            "insumo": insumo,
            "nombre": nombre
        }, {"_id": 0})

        if not sub:
            raise HTTPException(status_code=404, detail="Subinsumo no encontrado")

        return sub
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al obtener subinsumo: {str(e)}")


# Actualizar solo el mínimo
class ActualizarMinimo(BaseModel):
    nombre_usuario: str
    insumo: str
    nombre: str
    minimo: int

@router.put("/subinsumos/minimo")
def actualizar_minimo(data: ActualizarMinimo):
    try:
        result = subinsumos_collection.update_one(
            {
                "nombre_usuario": data.nombre_usuario,
                "insumo": data.insumo,
                "nombre": data.nombre
            },
            {"$set": {"minimo": data.minimo}}
        )

        if result.matched_count == 0:
            raise HTTPException(status_code=404, detail="Subinsumo no encontrado")

        return {"message": "Mínimo actualizado correctamente"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al actualizar mínimo: {str(e)}")


# Eliminar un subinsumo
@router.delete("/subinsumos/{nombre_usuario}/{insumo}/{nombre}")
def eliminar_subinsumo(nombre_usuario: str, insumo: str, nombre: str):
    try:
        result = subinsumos_collection.delete_one({
            "nombre_usuario": nombre_usuario,
            "insumo": insumo,
            "nombre": nombre
        })

        if result.deleted_count == 0:
            raise HTTPException(status_code=404, detail="Subinsumo no encontrado")

        return {"message": "Subinsumo eliminado correctamente"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al eliminar subinsumo: {str(e)}")
