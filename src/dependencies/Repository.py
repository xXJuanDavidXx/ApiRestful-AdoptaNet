from typing import Annotated
from ..db import SessionDep
from sqlmodel import select, SQLModel
from typing import Type
from fastapi import Depends 

#NOTA: El uso de Type[Sqlmodel] es porque en las funciones de listar o obtener un objeto de la base de datos, 
# se requiere el mapa de un modelo para consulta de ese tipo. Por lo que se usa Type para indicar que el argumento
# es un modelo de sqlmodel. o el "esquema|

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


    def list_all(self, model: Type[SQLModel]) -> list[SQLModel]: # Nota, cuando se usa Type, Es porque estoy requiriendo el mapa de un modelo para consulta de ese tipo.
        return self.session.exec(select(model)).all()


    def get_object_from_the_database_whit_id(self, model: Type[SQLModel], id: int) -> SQLModel | None:
        """
        Devuelve un objeto en la base de datos identificado por un id

        ARGS:
            model: El objeto que se pase debe ser una herencia de -> SQLModel
            id: de tipo entero el identificador del objeto que se este devolvioendo
        """
        return self.session.get(model, id) 
        
        
    def crear_en_db(self, model: SQLModel) -> SQLModel: # Aprendi que en este caso no uso type para | 
        """
        Se ocupa unicamente de crear un objeto en la base de datos.

        Args:
            model: La herencia de SQLModel que representa el objeto que se va aguradar en db. El objeto debe venir previamente procesado. 
        """
        self.session.add(model)
        self.session.commit()
        self.session.refresh(model)
        return model




    def update_object_in_db(self, model: SQLModel) -> SQLModel:
        """
        Se ocupa unicamente de actualizar un objeto en la base de datos.

        Args:
            model: La herencia de SQLModel que representa el objeto que se va aguradar en db. El objeto debe venir previamente procesado. 
        """
        self.session.add(model)
        self.session.commit()
        self.session.refresh(model)
        return model


    def delete_object_in_db(self, model: SQLModel) -> str:
        """
        Se ocupa unicamente de eliminar un objeto en la base de datos.

        Args:
            model: La herencia de SQLModel que representa el objeto que se va aguradar en db. El objeto debe venir previamente procesado. 
        """

        try:
            self.session.delete(model)
            self.session.commit()
            return "Objeto eliminado correctamente"
        except Exception as e:
            return f"Error al eliminar el objeto: {str(e)}"

    def  obtener_uno(self, model: Type[SQLModel], *args) -> SQLModel | None:
        """
        Obtiene un objeto de la base de datos bajo cualquier condicion que se le pase

        ARGS:
            model: El objeto que se pase debe ser una herencia de -> SQLModel
            *args: Cualquier condicion que se le pase para obtener el objeto
        """
        
        return self.session.exec(select(model).where(*args)).first()

    def obtener_muchos(self, model: Type[SQLModel], *args, skip: int = 0, limit: int = 10000) -> list[SQLModel]:
        """
        Obtiene muchos objetos de la base de datos bajo cualquier condicion que se le pase

        ARGS:
            model: El objeto que se pase debe ser una herencia de -> SQLModel
            *args: Cualquier condicion que se le pase para obtener el objeto
        """
        return self.session.exec(select(model).where(*args).offset(skip).limit(limit)).all()



def getQueryExec(session: SessionDep):
    """
    Todo_un_insulto_a_los_pythonistas jaja

    se encarga de pasar la session a QueryExec y devolverlo in real time uwu
    """
    return Repository(session)







QueryDep = Annotated[Repository, Depends(getQueryExec)] 




