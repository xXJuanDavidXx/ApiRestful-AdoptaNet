from fastapi import APIRouter
from sqlmodel import select
from db import SessionDep
from pydantic import BaseModel
from models import User, EntidadCreate, PublicanteCreate, ResponsePublicante, ResponseEntidad 
from dependencies.security import get_password_hash

router = APIRouter()




#@router.get("/token", tags=["autenticacion"])
#async def login(user: UserCreate, session: SessionDep):
    # La logica de autenticacion va aqui    

#    return {"message": "Login successful"}






### REGISTRO DE USUARIOS##
@router.post("/CreatePublicante", response_model=ResponsePublicante, tags=["autenticacion"])
async def register_publicante(userPublicante: PublicanteCreate, session: SessionDep):
    """
    Funcion para registrar un usuario publicante que representaria a cualquier persona comun y corriente que 
    sepa de animales para dar en adopcion

    ARGS:
        userPublicante: El usuario publicante que se va a registrar -> PublicanteCreate
        session: La sesion de la base de datos -> SessionDep
    """


    passHash = get_password_hash(userPublicante.contrasena)

    publicante = User.model_validate(userPublicante.model_dump(exclude="contrasena"))
    publicante.contrasena_hash = passHash
    session.add(publicante)
    session.commit()
    session.refresh(publicante)

    return publicante


@router.post("/CreateEntidad", response_model=ResponseEntidad, tags=["autenticacion"])
async def register_entidad(userEntidad: EntidadCreate, session: SessionDep):
    """
    Funcion para registrar un usuario entidad que representaria a cualquier entidad, fundacion o alverge que 
    sepa de animales para dar en adopcion.

    ARGS:
        userEntidad: El usuario entidad que se va a registrar -> EntidadCreate
        session: La sesion de la base de datos -> SessionDep
    """
    passHash = get_password_hash(userEntidad.contrasena)    

    entidad = User.model_validate(userEntidad.model_dump(exclude="contrasena"))
    entidad.contrasena_hash = passHash
    session.add(entidad)
    session.commit()
    session.refresh(entidad)

    return entidad




### LOGIN DE USUARIOS###































