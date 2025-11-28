from fastapi import APIRouter, Depends, HTTPException
from typing import Annotated
from db import SessionDep
from models import User, EntidadCreate, PublicanteCreate, ResponsePublicante, ResponseEntidad 
from dependencies.security import get_password_hash, autenticated_user
from dependencies.jwt import create_access_token, depGetCurrentUser
from fastapi.security import OAuth2PasswordRequestForm 
from dependencies.Repository import QueryDep


router = APIRouter()

### Autenticacion y token jwt#
@router.post("/token", tags=["autenticacion"])
async def login( session: SessionDep, form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    """   
    La logica de autenticacion va aqui  

    ARGS:
        session: La sesion de la base de datos -> SessionDep
        form_data: Los datos del usuario -> OAuth2PasswordRequestForm
    """
    user = autenticated_user(session, form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=401, detail="Incorrect username or password")    
    
    access_token = create_access_token(data={"sub": user.correo})
    
    
    return {"access_token": access_token, "token_type": "bearer"}



### REGISTRO DE USUARIOS##
@router.post("/CreatePublicante", response_model=ResponsePublicante, tags=["autenticacion"])
async def register_publicante(userPublicante: PublicanteCreate, querydep: QueryDep):
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
   
   # Implementar querydep
    querydep.crearEnDB(publicante)
    
    return publicante


@router.post("/CreateEntidad", response_model=ResponseEntidad, tags=["autenticacion"])
async def register_entidad(userEntidad: EntidadCreate, querydep: QueryDep):
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
    
    querydep.crearEnDB(entidad)
    
    return entidad




### Prueba Login###


@router.get("/users/me", tags=["autenticacion"])
async def read_users_me(current_user: depGetCurrentUser):
    return current_user





























