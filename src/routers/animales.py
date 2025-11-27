from fastapi import APIRouter, HTTPException
from models import Animal, User, AnimalCreate
from db import SessionDep

router = APIRouter()




###  Registrar animales ####
@router.post("/RegistrarAnimal", response_model=Animal, tags=["animales"])
async def register_animal(animal: AnimalCreate, session: SessionDep):
    """
    La logica de registro de animales, espera el modelo AnimalCreate que defini en models

    """
    dict_animal = animal.model_dump()
    user = session.get(User, User.id_usuario == dict_animal.get("id_user"))

    if not user:
        raise HTTPException(status_code=404, detail={"Message": "Eso no existe.. ;-;"},)


    animalito: Animal =  Animal.model_validate(dict_animal) 

    session.add(animalito)
    session.commit()
    session.refresh(animalito)

    return animalito


#### Listar animales ####

@router.get("/ListarAnimales", tags=["animales"])
async def listarAnimales(session: SessionDep):
    """
    Lista Todo el catalogo de animales.

    es evidente por si misma.. no necesita argumentos ....kibalion
    """

    return session.exec(select(Animal)).all()








