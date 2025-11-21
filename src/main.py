from fastapi import FastAPI
from datetime import datetime
from routers import autenticacion
from db import create_tables  



app = FastAPI(lifespan=create_tables)
app.include_router(autenticacion.router)



@app.get("/")
async def root():
    return {
        "message": "Hello World",
        "date":f"{datetime.now().hour}:{datetime.now().minute}:{datetime.now().second}"}




