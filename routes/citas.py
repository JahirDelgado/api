from fastapi import APIRouter, HTTPException, Query
from datetime import datetime, timedelta
from typing import List, Optional
from models import CitaCreate, ServicioInfo
from database import db

router = APIRouter(prefix="/citas", tags=["Citas"])

@router.get("/servicios")
async def get_servicios(posicion: str, profesional: Optional[str] = None):
    if posicion == "empleado":
        if not profesional:
            raise HTTPException(status_code=400, detail="Se requiere el nombre del profesional para empleados.")
        
        # Buscar TODOS los documentos del profesional
        profesional_docs = db.usuarios.find({"nombre": profesional})
        
        servicios_set = set()
        for doc in profesional_docs:
            servicio = doc.get("servicio")
            if isinstance(servicio, list):
                servicios_set.update(servicio)
            elif isinstance(servicio, str):
                servicios_set.add(servicio)

        return [{"nombreServicio": s} for s in servicios_set]
    else:
        servicios_raw = db.servicios.find({}, {"_id": 0, "nombreServicio": 1})
        return list(servicios_raw)

@router.get("/profesionales")
async def get_profesionales(servicio: Optional[str] = None):
    query = {"posicion": "empleado"}
    if servicio:
        query["servicio"] = servicio

    profesionales = db.usuarios.find(query, {"_id": 0, "nombre": 1, "servicio": 1})
    return list(profesionales)

@router.get("/por-dia")
async def get_citas_por_dia(fecha: str, profesional: Optional[str] = None):
    try:
        datetime.strptime(fecha, "%d/%m/%Y")
    except ValueError:
        raise HTTPException(status_code=400, detail="Formato de fecha inválido. Usa dd/mm/yyyy.")

    query = {"date": fecha, "status": {"$ne": "cancelada"}}
    if profesional:
        query["professional"] = profesional

    citas = db.citas.find(query, {"_id": 0})
    return list(citas)

@router.post("/verificar-disponibilidad")
async def verificar_disponibilidad(data: dict):
    profesional = data.get("profesional")
    fecha = data.get("fecha")
    hora = data.get("hora")
    duracion = data.get("duracion", 0)

    if not profesional or not fecha or not hora:
        raise HTTPException(status_code=400, detail="Faltan parámetros para verificar disponibilidad.")

    try:
        hora_inicio = datetime.strptime(f"{fecha} {hora}", "%d/%m/%Y %H:%M")
        hora_fin = hora_inicio + timedelta(minutes=int(duracion))
        fecha_dt = datetime.strptime(fecha, "%d/%m/%Y")
    except ValueError:
        raise HTTPException(status_code=400, detail="Formato de fecha/hora inválido.")

    # Validar día y horario
    if fecha_dt.weekday() == 0:  # Lunes
        raise HTTPException(status_code=400, detail="No se pueden agendar citas los lunes.")

    if fecha_dt.weekday() == 6:  # Domingo
        cierre_oficial = hora_inicio.replace(hour=15, minute=0)
        cierre_tolerado = cierre_oficial + timedelta(minutes=30)
        if hora_inicio.hour < 10 or hora_fin > cierre_tolerado:
            raise HTTPException(status_code=400, detail="Domingos: horario de 10:00 a 15:00 hrs (30 min tolerancia).")
    else:  # Martes a Sábado
        cierre_oficial = hora_inicio.replace(hour=19, minute=0)
        cierre_tolerado = cierre_oficial + timedelta(minutes=30)
        if hora_inicio.hour < 10 or hora_fin > cierre_tolerado:
            raise HTTPException(status_code=400, detail="Martes a Sábado: horario de 10:00 a 19:00 hrs (30 min tolerancia).")

    # Checar conflictos de horario
    citas_existentes = db.citas.find({
        "professional": profesional,
        "date": fecha,
        "status": {"$ne": "cancelada"}
    })

    for cita in citas_existentes:
        cita_inicio = datetime.strptime(f"{cita['date']} {cita['time']}", "%d/%m/%Y %H:%M")
        servicio = db.servicios.find_one({"nombreServicio": cita["service"]})
        duracion_existente = int(servicio["duracion"]) if servicio else 0
        cita_fin = cita_inicio + timedelta(minutes=duracion_existente)

        if hora_inicio < cita_fin and hora_fin > cita_inicio:
            raise HTTPException(status_code=400, detail=f"Conflicto con cita existente a las {cita_inicio.strftime('%H:%M')}.")

    return {"detail": "Horario disponible."}

@router.post("/crear")
async def crear_cita(cita: CitaCreate):
    try:
        cita_dict = cita.dict()
        cita_dict["createdAt"] = datetime.now()
        db.citas.insert_one(cita_dict)
        return {"message": "Cita creada exitosamente"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al crear cita: {str(e)}")

@router.get("/servicio-info")
async def get_servicio_info(nombre: str):
    servicio = db.servicios.find_one({"nombreServicio": nombre}, {"_id": 0})
    if not servicio:
        raise HTTPException(status_code=404, detail="Servicio no encontrado")
    return servicio

@router.get("/{fecha}")
async def get_citas_segun_usuario(
    fecha: str,
    usuario: str = Query(...),
    rol: str = Query(...)
):
    try:
        datetime.strptime(fecha, "%d/%m/%Y")
    except ValueError:
        raise HTTPException(status_code=400, detail="Formato de fecha inválido. Usa dd/mm/yyyy.")

    query = {"date": fecha, "status": {"$ne": "cancelada"}}

    if rol == "empleado":
        query["professional"] = usuario
    # Si es admin, no se filtra por profesional

    citas = db.citas.find(query)
    resultados = []
    for cita in citas:
        cita["_id"] = str(cita["_id"])
        resultados.append(cita)

    return resultados
