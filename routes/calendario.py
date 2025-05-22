from fastapi import APIRouter, Query, HTTPException
from typing import List
from datetime import datetime
from pydantic import BaseModel
from bson import ObjectId
from models import CitaResponse
from database import db

router = APIRouter()

@router.get("/citas/{fecha}", response_model=List[CitaResponse])
async def obtener_citas(
    fecha: str,  # Fecha en formato dd/mm/yyyy desde la ruta
    usuario: str = Query(..., description="Nombre del usuario que solicita las citas"),
    rol: str = Query(..., description="Rol del usuario")
):
    """
    Obtiene la lista de citas para un día específico y usuario dado.
    """

    try:
        # Convertir fecha string a datetime para validación
        fecha_dt = datetime.strptime(fecha, "%d/%m/%Y")
    except ValueError:
        raise HTTPException(status_code=400, detail="Formato de fecha inválido, debe ser dd/mm/yyyy")

    # Construir filtro para MongoDB
    filtro = {
        "date": fecha,  # o el formato que uses para almacenar fecha en tu BD
    }

    # Puedes filtrar por profesional (usuario) o rol, según lógica de negocio
    if rol.lower() == "profesional":
        filtro["professional"] = usuario
    else:
        # Si el usuario no es profesional, puedes filtrar de otra forma o devolver todas las citas del día
        pass

    citas_cursor = db.citas.find(filtro)

    citas = []
    for cita in citas_cursor:
        # Convertir ObjectId a str
        cita["_id"] = str(cita["_id"])
        citas.append(cita)

    return citas
