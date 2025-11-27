from typing import Annotated
from db import SessionDep
from sqlmodel import select, SQLModel
from typing import Type
from fastapi import Depends 

#Lo Logró. Gracias UNIVERSO :)


class QueryExec():
    """
    Objeto que agrupa toda la logica del crud principalmente 
    para que las rutas solo se preocupan de la lógica de negocio, no de "armar objetos.... y tambien por escrbir menos jaja
    """

    def __init__(self, session: SessionDep):
        """
        REcibe el poder de sqlmodel que es la session uwu
        """
        self.session = session


    def listAll(self, model: Type[SQLModel]):
        return self.session.exec(select(model)).all()


    def getObjectFromTheDatabaseWhitId(self, model: Type[SQLModel], id: int):
        """
        Devuelve un objeto en la base de datos identificado por un id

        ARGS:
            model: El objeto que se pase debe ser una herencia de -> SQLModel
            id: de tipo entero el identificador del objeto que se este devolvioendo
        """
        return self.session.get(model, id) 
        

########ACABAR PRONTO... De momento.. gana el sueño  FALTA IMPLEMENTAR BUENA PARTE DEL CRUD BASICO AUN.

        



def getQueryExec(session: SessionDep):
    """
    Todo_un_insulto_a_los_pythonistas jaja

    se encarga de pasar la session a QueryExec y devolverlo in real time uwu
    
    """ 
    return QueryExec(session)





QueryDep = Annotated[QueryExec, Depends(getQueryExec)] 




