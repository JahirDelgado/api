from pymongo import MongoClient
from dotenv import load_dotenv
import os

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI", "mongodb+srv://dhnc464:dhnc464@cluster0.ve4qv.mongodb.net/citasSalon?retryWrites=true&w=majority")

client = MongoClient(MONGO_URI)
db = client["citasSalon"]

# Colecciones
cuentas_usuario_collection = db["cuentas_usuario"]
usuarios_collection = db["usuarios"]
