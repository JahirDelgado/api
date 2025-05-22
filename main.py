from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes import auth
from routes import citas
from routes import calendario

app = FastAPI(
    title="BeautyTech API",
    description="API para el sistema de gestión de citas beautytech",
    version="0.1.0"
)

# Configurar CORS (permite conexiones desde tu app Flet)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # En producción, reemplaza con tu dominio
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Incluir rutas
app.include_router(auth.router)

@app.get("/")
def read_root():
    return {"message": "Bienvenido a BeautyTech API"}

app.include_router(citas.router, prefix="/citas", tags=["Citas"])
