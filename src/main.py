from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime
from routers import autenticacion, animales, solicitudes
from db import create_tables  



app = FastAPI(lifespan=create_tables)
app.include_router(autenticacion.router)
app.include_router(animales.router)
app.include_router(solicitudes.router)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    return {
        "message": "Hello World",
        "date":f"{datetime.now().hour}:{datetime.now().minute}:{datetime.now().second}"}




