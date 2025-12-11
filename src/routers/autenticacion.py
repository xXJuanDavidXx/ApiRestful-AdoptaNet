from fastapi import APIRouter, Depends, HTTPException
from typing import Annotated
from db import SessionDep
from models import User, EntidadCreate, PublicanteCreate, ResponsePublicante, ResponseEntidad, UserUpdate 
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
        querydep: La dependencia del repositorio -> QueryDep
    """

    # Verificar si el correo ya existe
    existing_user = querydep.obtener_uno(User, User.correo == userPublicante.correo)
    if existing_user:
        raise HTTPException(status_code=400, detail="El correo ya está registrado")

    passHash = get_password_hash(userPublicante.contrasena)

    publicante = User.model_validate(userPublicante.model_dump(exclude="contrasena"))
    publicante.contrasena_hash = passHash
   
    querydep.crear_en_db(publicante)
    
    return publicante


@router.post("/CreateEntidad", response_model=ResponseEntidad, tags=["autenticacion"])
async def register_entidad(userEntidad: EntidadCreate, querydep: QueryDep):
    """
    Funcion para registrar un usuario entidad que representaria a cualquier entidad, fundacion o alverge que 
    sepa de animales para dar en adopcion.

    ARGS:
        userEntidad: El usuario entidad que se va a registrar -> EntidadCreate
        querydep: La dependencia del repositorio -> QueryDep
    """
    
    # Verificar si el correo ya existe
    existing_user = querydep.obtener_uno(User, User.correo == userEntidad.correo)
    if existing_user:
        raise HTTPException(status_code=400, detail="El correo ya está registrado")
    
    passHash = get_password_hash(userEntidad.contrasena)    

    entidad = User.model_validate(userEntidad.model_dump(exclude="contrasena"))
    entidad.contrasena_hash = passHash
    
    querydep.crear_en_db(entidad)
    
    return entidad




### Prueba Login###


@router.get("/users/me", tags=["autenticacion"])
async def read_users_me(current_user: depGetCurrentUser):
    return current_user


@router.put("/users/me", response_model=User, tags=["autenticacion"])
async def update_user(user_update: UserUpdate, querydep: QueryDep, current_user: depGetCurrentUser):
    """
    Actualiza los datos del usuario autenticado.
    """
    user_data = user_update.model_dump(exclude_unset=True)
    
    for key, value in user_data.items():
        setattr(current_user, key, value)
        
    querydep.update_object_in_db(current_user)
    
    return current_user





























