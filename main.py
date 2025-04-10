from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from datetime import datetime
import uuid
from typing import Dict, List

app = FastAPI()

# Permitir acceso desde React (CORS)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Nueva estructura de productos por sección
class Comanda(BaseModel):
    mesa: int
    productos: Dict[str, List[str]]  # ej: {"aperitivo": [...], "bebida": [...]}

# Historial en memoria
historial_comandas = []

# Recibir nueva comanda
@app.post("/comanda")
def recibir_comanda(comanda: Comanda):
    nueva = {
        "id": str(uuid.uuid4()),
        "mesa": comanda.mesa,
        "productos": comanda.productos,
        "hora": datetime.now().strftime("%H:%M:%S"),
        "fecha": datetime.now().strftime("%Y-%m-%d"),
        "atendida": False
    }
    historial_comandas.append(nueva)
    return {"mensaje": "Comanda recibida"}

# Obtener historial (con filtro por fecha opcional)
@app.get("/historial")
def obtener_historial(fecha: str = Query(None)):
    if fecha:
        return [c for c in historial_comandas if c["fecha"] == fecha]
    return historial_comandas

# Marcar comanda como atendida por ID
@app.put("/comanda/atendida/{comanda_id}")
def marcar_atendida(comanda_id: str):
    for comanda in historial_comandas:
        if comanda["id"] == comanda_id:
            comanda["atendida"] = True
            return {"mensaje": "Comanda marcada como atendida"}
    raise HTTPException(status_code=404, detail="Comanda no encontrada")
