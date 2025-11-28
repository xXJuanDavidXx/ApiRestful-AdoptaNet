from typing import Annotated
from db import SessionDep
from sqlmodel import select, SQLModel
from typing import Type
from fastapi import Depends 
from typing import List

#Lo Logró. Gracias UNIVERSO :)


class Repository():
    """
    Objeto que agrupa toda la logica del crud principalmente 
    para que las rutas solo se preocupan de la lógica de negocio, no de "armar objetos.... y tambien por escrbir menos jaja
    """

    def __init__(self, session: SessionDep):
        """
        REcibe el poder de sqlmodel que es la session uwu
        """
        self.session = session


    def listAll(self, model: Type[SQLModel]) -> List[Type[SQLModel]]: # Nota, cuando se usa Type, Es porque estoy requiriendo el mapa de un modelo para consulta de ese tipo.
        return self.session.exec(select(model)).all()


    def getObjectFromTheDatabaseWhitId(self, model: Type[SQLModel], id: int) -> Type[SQLModel]:
        """
        Devuelve un objeto en la base de datos identificado por un id

        ARGS:
            model: El objeto que se pase debe ser una herencia de -> SQLModel
            id: de tipo entero el identificador del objeto que se este devolvioendo
        """
        return self.session.get(model, id) 
        
        
    def crearEnDB(self, model: SQLModel) -> Type[SQLModel]: # Aprendi que en este caso no uso type para | 
        """
        Se ocupa unicamente de crear un objeto en la base de datos.

        Args:
            model: La herencia de SQLModel que representa el objeto que se va aguradar en db. El objeto debe venir previamente procesado. 
        """
        self.session.add(model)
        self.session.commit()
        self.session.refresh(model)
        return model


    ### PENSAR EN COMO HACER EL UPDATE Y EL DELETE.


    def updatObjectenDB(self, model: SQLModel) -> Type[SQLModel]:
        """
        Se ocupa unicamente de actualizar un objeto en la base de datos.

        Args:
            model: La herencia de SQLModel que representa el objeto que se va aguradar en db. El objeto debe venir previamente procesado. 
        """
        self.session.add(model)
        self.session.commit()
        self.session.refresh(model)
        return model


    def delete_objecte(self, model: SQLModel) -> Type[SQLModel]:
        """
        Se ocupa unicamente de eliminar un objeto en la base de datos.

        Args:
            model: La herencia de SQLModel que representa el objeto que se va aguradar en db. El objeto debe venir previamente procesado. 
        """
        self.session.delete(model)
        self.session.commit()
        return model

    def obtener_uno(self, model: Type[SQLModel], *args) -> SQLModel | None:
        """
        Obtiene un objeto de la base de datos bajo cualquier condicion que se le pase

        ARGS:
            model: El objeto que se pase debe ser una herencia de -> SQLModel
            *args: Cualquier condicion que se le pase para obtener el objeto
        """
        
        return self.session.exec(select(model).where(*args)).first()

    def filtrar(self):
        """
        Proximo desarrollo uwu
        """
        pass


def getQueryExec(session: SessionDep):
    """
    Todo_un_insulto_a_los_pythonistas jaja

    se encarga de pasar la session a QueryExec y devolverlo in real time uwu
    """
    return Repository(session)







QueryDep = Annotated[Repository, Depends(getQueryExec)] 




