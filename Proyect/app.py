import datetime
import json
import uvicorn
from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from backend import consultas

app = FastAPI()

# Configurar el middleware de CORS para permitir solicitudes desde cualquier origen
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["GET"],
    allow_headers=["*"],
)

@app.get("/logo")
async def logo():
    return FileResponse("logo.png")

@app.get("/")
async def root():
    return FileResponse("index.html")

@app.get("/ventasAnuales")
async def ventasAnuales():
    return consultas.TotalVentasAnuales()

@app.get("/ventasMensuales")
async def ventasMensuales():
    return consultas.TotalVentasMensuales()

@app.get("/Top10Porductos")
async def top10productos():
    return consultas.Top10Productos()

@app.get("/Todos")
async def todoslosproductos():
    return consultas.TodosLosProductos()

@app.get("/Top10codigosPostales")
async def codigosPostales():
    return consultas.codigosPostales()


if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8081)

