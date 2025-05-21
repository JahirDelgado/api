from fastapi import APIRouter, HTTPException, Query
from datetime import datetime
from typing import List, Optional
from models import CitaCreate
from database import db

router = APIRouter(prefix="/citas", tags=["Citas"])

@router.get("/servicios")
async def get_servicios(posicion: str, profesional: Optional[str] = None):
    if posicion == "empleado":
        if not profesional:
            raise HTTPException(status_code=400, detail="Se requiere el nombre del profesional para empleados.")
        
        profesional_data = db.usuarios.find_one({"nombre": profesional})
        if not profesional_data:
            raise HTTPException(status_code=404, detail="Profesional no encontrado.")

        servicios = profesional_data.get("servicio", [])
        if isinstance(servicios, str):
            servicios = [servicios]

        return [{"nombreServicio": s} for s in servicios]
    else:
        return list(db.servicios.find({}, {"_id": 0}))

@router.get("/profesionales")
async def get_profesionales(servicio: Optional[str] = None):
    query = {"posicion": {"$ne": "admin"}}
    if servicio:
        query["servicio"] = servicio
    return list(db.usuarios.find(query, {"_id": 0}))

@router.get("/existentes")
async def get_citas_existentes(fecha: str, profesional: Optional[str] = None):
    try:
        datetime.strptime(fecha, "%d/%m/%Y")  # Validar formato
    except ValueError:
        raise HTTPException(status_code=400, detail="Formato de fecha inválido. Usa dd/mm/yyyy.")

    query = {"date": fecha, "status": {"$ne": "cancelada"}}
    if profesional:
        query["professional"] = profesional

    return list(db.citas.find(query, {"_id": 0}))

@router.post("/nueva")
async def crear_cita(cita: CitaCreate):
    try:
        # Validación de campos requeridos ya debe hacerse en el modelo Pydantic
        cita_dict = cita.dict()
        cita_dict["createdAt"] = datetime.now()
        db.citas.insert_one(cita_dict)
        return {"message": "Cita creada exitosamente"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al crear cita: {str(e)}")
