from fastapi import APIRouter, HTTPException
from database import cuentas_usuario_collection, usuarios_collection
from models import UserLogin, UserInfo

router = APIRouter(prefix="/auth", tags=["Authentication"])

@router.post("/login")
async def login(user: UserLogin):
    # Verificar credenciales
    cuenta_existente = cuentas_usuario_collection.find_one({
        "correo": user.correo,
        "contrasena": user.contrasena
    })
    
    if not cuenta_existente:
        raise HTTPException(status_code=401, detail="Correo o contraseña incorrectos")
    
    # Obtener información adicional del usuario
    usuario_info = usuarios_collection.find_one({
        "nombre": cuenta_existente["nombre"]
    })
    
    if not usuario_info:
        raise HTTPException(status_code=404, detail="Información de usuario no encontrada")
    
    return {
        "nombre": usuario_info["nombre"],
        "posicion": usuario_info["posicion"],
        "message": "Login exitoso"
    }
