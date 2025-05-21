from pymongo import MongoClient
import os
from dotenv import load_dotenv

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI")  # o puedes pegar tu URI directamente aquí
client = MongoClient(MONGO_URI)
db = client["citasSalon"]