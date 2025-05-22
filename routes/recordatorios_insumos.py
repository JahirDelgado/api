from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List
from database import db

router = APIRouter(tags=["Recordatorios"])
subinsumos_collection = db["subinsumos"]

class SubinsumoRecordatorio(BaseModel):
    insumo: str
    nombre: str
    cantidad: int
    minimo: int

@router.get("/insumo/recordatorio/{nombre_usuario}", response_model=List[SubinsumoRecordatorio])
def obtener_recordatorios(nombre_usuario: str):
    try:
        subinsumos = list(subinsumos_collection.find(
            {"nombre_usuario": nombre_usuario, "$expr": {"$lte": ["$cantidad", "$minimo"]}},
            {"_id": 0, "insumo": 1, "nombre": 1, "cantidad": 1, "minimo": 1}
        ))
        return subinsumos
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al obtener recordatorios: {str(e)}")
