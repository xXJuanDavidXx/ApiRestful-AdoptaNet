from sqlmodel import SQLModel, Field, Relationship
from typing import Optional
from pydantic import EmailStr, field_validator

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



# Modelo de la Tabla DB
class User(UserBase, table=True):
    id_usuario: Optional[int] = Field(default=None, primary_key=True)
    contrasena_hash: str | None = Field(default=None, nullable=True)  # Permitir NULL en la DBNone  
    # animales_publicados: list["Animal"] = Relationship(back_populates="usuario") 
    # solicitudes_hechas: list["Solicitud"] = Relationship(back_populates="usuario_solicitante")


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




## ANIMALES ###


class AnimalBase(SQLModel):
    nombre: str
    especie: str
    raza: str
    edad: int | None = Field(default=None, nullable=True)
    sexo: str
    descripcion: str | None = Field(default=None, nullable=True)
    imagen: str

    # PEnsar si el base deberia tener de una vez la relacion con el usuario



# Mirar como hacer relacion
























