from fastapi import APIRouter, HTTPException
from dependencies.jwt import depGetCurrentUser
from dependencies.Repository import QueryDep



router = APIRouter()


@router.post("/RegistrarSolicitud", tags=["Solicitudes"])
async def registrarSolicitud(querydep: QueryDep, current_user: depGetCurrentUser):
    """
    registrar la solicitud de adopcion de un animal.


    Args:
        querydep (QueryDep): dependencia de la base de datos.
        current_user (depGetCurrentUser): dependencia del usuario actual.        
    """







