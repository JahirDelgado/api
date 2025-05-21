from fastapi import APIRouter, HTTPException
from datetime import datetime
from models import CitaCreate
from database import db

router = APIRouter(prefix="/citas", tags=["Citas"])

@router.get("/servicios")
async def get_servicios(posicion: str, profesional: str = None):
    if posicion == "empleado":
        # Obtener servicios del profesional
        profesional_data = db.usuarios.find_one({"nombre": profesional})
        servicios = profesional_data.get("servicio", [])
        return [{"nombreServicio": s} for s in (servicios if isinstance(servicios, list) else [servicios])]
    else:
        # Obtener todos los servicios
        return list(db.servicios.find())

@router.get("/profesionales")
async def get_profesionales(servicio: str = None):
    query = {"posicion": "empleado"}
    if servicio:
        query["servicio"] = servicio
    return list(db.usuarios.find(query))

@router.get("/existentes")
async def get_citas(fecha: str, profesional: str = None):
    query = {
        "date": fecha,
        "status": {"$ne": "cancelada"}
    }
    if profesional:
        query["professional"] = profesional
    return list(db.citas.find(query))

@router.post("/nueva")
async def crear_cita(cita: CitaCreate):
    # Validaciones de horario aquí...
    nueva_cita = cita.dict()
    nueva_cita["createdAt"] = datetime.now()
    db.citas.insert_one(nueva_cita)
    return {"message": "Cita creada exitosamente"}
