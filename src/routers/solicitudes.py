from fastapi import APIRouter, HTTPException
from dependencies.jwt import depGetCurrentUser
from dependencies.Repository import QueryDep
from models import Solicitud, CrearSolicitud, User, Animal



router = APIRouter()



@router.get("/Solicitudes/{user_id}", tags=["Solicitudes"])
async def listar_solicitudes(querydep: QueryDep, current_user: depGetCurrentUser, skip: int = 0, limit: int = 20): 
    
    animales = querydep.obtener_muchos(Animal, Animal.id_usuario == current_user.id_usuario, skip=0, limit=10000)


    ## SACARA LISTA DE ANIMALES CON ID, 

    animalesIds = [animal.id_animal for animal in animales]


    solicitudes = querydep.obtener_muchos(Solicitud, Solicitud.id_animal.in_(animalesIds), skip=skip, limit=limit)    



    return solicitudes


@router.post("/RegistrarSolicitud", tags=["Solicitudes"])
async def registrarSolicitud(querydep: QueryDep, solicitud: CrearSolicitud):
    """
    registrar la solicitud de adopcion de un animal.


    Args:
        querydep (QueryDep): dependencia de la base de datos.
        solicitud: El esquema de datos para crear una solicitud
    """

    # NOTA, hablar con sebastian sobre el registro de Solicitudes
    #- duda puntual; 1-Como manejaria el registro de solicitudes desde el front


    solicitud_dict = solicitud.model_dump()

    #Validaciones
    user = querydep.obtener_uno(User, User.id_usuario == solicitud_dict.get("id_usuario"))
    
    if not user:
        raise HTTPException(status_code=404, detail={"message":"El usuario no existe"})

    animal = querydep.obtener_uno(Animal, Animal.id_animal == solicitud_dict.get("id_animal"))

    if not animal:
        raise HTTPException(status_code=404, detail={"message": "El animal no existe"})

    
    solicitud_db = Solicitud.model_validate(solicitud_dict)
    
    return querydep.crear_en_db(solicitud_db)

    

    







