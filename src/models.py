from sqlmodel import SQLModel, Field, Relationship
from typing import Optional
from pydantic import EmailStr, BaseModel, field_validator

#### AUTENTICACION Y USUARIOS ####

class UserBase(SQLModel):
    # Campos comunes
    nombre: str
    correo: EmailStr = Field(unique=True)  
    telefono: str
    direccion: str
    
    
    # Campo Discriminador
    rol: str = Field(index=True)
    
    # Campos específicos del Publicante (Permitir NULL en la DB)
    cc: str | None = Field(default=None, nullable=True) 
    
    # Campos específicos de la Organización (Permitir NULL en la DB)
    nit: str | None = Field(default=None, nullable=True)  # Permitir NULL en la DBNone
    tipo_organizacion: Optional[str] = None
    descripcion: str | None = Field(default=None, nullable=True)  # Permitir NULL en la DBNone


class UserUpdate(SQLModel):
    nombre: str | None = None
    telefono: str | None = None
    direccion: str | None = None
    
    # Campos específicos to update (optional)
    cc: str | None = None
    nit: str | None = None
    tipo_organizacion: str | None = None
    descripcion: str | None = None



# Modelo de la Tabla DB
class User(UserBase, table=True):
    id_usuario: Optional[int] = Field(default=None, primary_key=True)
    contrasena_hash: str | None = Field(default=None, nullable=True)  # Permitir NULL en la DBNone  
    animales_publicados: list["Animal"] = Relationship(back_populates="usuario") 
    solicitudes: list["Solicitud"] = Relationship(back_populates="usuario") ##REcordar que asi se hace una relacion, en este caso un usuario puede tener muchas solicitudes.


class EntidadCreate(UserBase):
    rol:str = "organizacion"
    nit: str | None = Field(default=None, nullable=True)  # Permitir NULL en la DBNone
    tipo_organizacion: Optional[str] = None
    descripcion: str | None = Field(default=None, nullable=True)
    contrasena: str # Para recibir y convertir en hash y pasarlo a la DB


class PublicanteCreate(UserBase):
    rol:str = "publicante"
    cc: str | None = Field(default=None, nullable=True) 
    contrasena: str # Para recibir y convertir en contrasena_hash
    # 2. Sobrescribir los campos de la organización a None
    # Esto le indica a Pydantic que estos campos siempre son nulos para este modelo
    nit: str |  None = Field(default=None)  # Permitir NULL en la DBNone
    tipo_organizacion:str | None = Field(default=None)  # Permitir NULL en la DBNone
    descripcion:str | None = Field(default=None)
 
# Creo las respuestas porque tengo que mostrar unos datos u otros en funcion del rol 
class ResponsePublicante(SQLModel):
    id_usuario: int
    nombre: str
    correo: EmailStr
    telefono: str
    direccion: str
    rol: str
    cc: str | None


class ResponseEntidad(SQLModel):
    id_usuario: int
    nombre: str
    correo: EmailStr
    telefono: str
    direccion: str
    rol: str
    nit: str | None
    tipo_organizacion: str | None
    descripcion: str | None




############## ANIMALES ##################


class AnimalBase(SQLModel):
    nombre: str
    especie: str
    raza: str
    edad: int | None = Field(default=None, nullable=True)
    sexo: str
    descripcion: str | None = Field(default=None, nullable=True)
    imagen: str
    adoptado: bool = False 


class Animal(AnimalBase, table=True):
    id_animal: int | None = Field(default=None, primary_key=True)
    id_user: int | None = Field(default=None, foreign_key="user.id_usuario")    
    usuario : User = Relationship(back_populates="animales_publicados")  # La funcion de backpopulatrs es mantener sincronizadas las dos tablas el usuario que se relaciona a el animal y arriba en animales una lista de usuarios.
    animal_solicitado: list["Solicitud"] = Relationship(back_populates="animal")

class AnimalCreate(BaseModel):
    """
    Este seria unicamente para la creacion de animales, lo centro unicamente en los datos que si le permito para la creacion 

    """
    nombre: str
    especie: str
    raza: str
    edad: int | None = Field(default=None, nullable=True)
    sexo: str
    descripcion: str | None = Field(default=None, nullable=True)
    imagen: str
    id_user: int | None = Field(default=None) 




###### SOLICITUDES de Adopcion #######


class SolicitudBase(SQLModel):
    nombre_completo: str
    correo: EmailStr
    telefono: str


class Solicitud(SolicitudBase, table=True):
    id_solicitud: int | None = Field(default=None, primary_key=True)
    id_animal: int = Field(foreign_key="animal.id_animal")
    id_usuario: int = Field(foreign_key="user.id_usuario")
    animal : Animal = Relationship(back_populates="animal_solicitado") ## RECORDAR QUE ES MUCHOS A UNO
    usuario : User = Relationship(back_populates="solicitudes")

#Los nombres en back_populates deben coincidir exactamente con el nombre del atributo en la OTRA clase. ###TENER PRESENTE


class CrearSolicitud(BaseModel):
    """
       Esquema de creacion de una solicitud. 

    """
    id_animal: int  
    id_usuario: int 
    nombre_completo: str
    correo: EmailStr
    telefono: str



# Filter Params




















