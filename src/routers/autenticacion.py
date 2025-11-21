from fastapi import APIRouter
from sqlmodel import select
from db import SessionDep
from pydantic import BaseModel
from models import User, EntidadCreate, PublicanteCreate 


router = APIRouter()




@router.get("/token", tags=["autenticacion"])
async def login(user: UserCreate, session: SessionDep):
    # La logica de autenticacion va aqui    

    return {"message": "Login successful"}







@router.post("/CreatePublicante", tags=["autenticacion"])
async def register_publicante(user: PublicanteCreate, session: SessionDep):
    # La logica de registro va aqui

    return {"message": "Registration successful"}


@router.post("/CreateEntidad", tags=["autenticacion"])
async def register_entidad(user: EntidadCreate, session: SessionDep):
    # La logica de registro va aqui

    return {"message": "Registration successful"}



