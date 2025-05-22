from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, EmailStr
from typing import List
from database import db

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
