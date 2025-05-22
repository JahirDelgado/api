from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes import auth, citas, recordatorios, usuarios, insumos

app = FastAPI(
    title="BeautyTech API",
    description="API para el sistema de gestión de citas beautytech",
    version="0.1.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(citas.router, prefix="/citas", tags=["Citas"])
app.include_router(recordatorios.router)
app.include_router(usuarios.router, prefix="/usuarios", tags=["Usuarios"])
app.include_router(insumos.router)

@app.get("/")
def read_root():
    return {"message": "Bienvenido a BeautyTech API"}
