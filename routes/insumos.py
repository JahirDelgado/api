from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List
from database import db
from fastapi import Path


router = APIRouter(tags=["Insumos"])

insumos_collection = db["Insumos"]

class Insumo(BaseModel):
    nombre: str
    nombre_usuario: str

@router.get("/insumos/{nombre_usuario}", response_model=List[Insumo])
def obtener_insumos(nombre_usuario: str):
    try:
        insumos = list(insumos_collection.find({"nombre_usuario": nombre_usuario}, {"_id": 0}))
        return insumos
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al obtener insumos: {str(e)}")

@router.post("/insumos", status_code=201)
def crear_insumo(insumo: Insumo):
    try:
        insumos_collection.insert_one(insumo.dict())
        return {"mensaje": "Insumo agregado correctamente"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al insertar insumo: {str(e)}")

@router.delete("/insumos/{nombre}", status_code=200)
def eliminar_insumo(nombre: str = Path(...)):
    try:
        resultado = insumos_collection.delete_one({"nombre": nombre})
        if resultado.deleted_count == 0:
            raise HTTPException(status_code=404, detail="Insumo no encontrado")
        return {"mensaje": "Insumo eliminado correctamente"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al eliminar insumo: {str(e)}")
