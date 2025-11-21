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
    
    contrasena_hash: str | None = Field(default=None, nullable=True)  # Permitir NULL en la DBNone  
    
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
    # animales_publicados: list["Animal"] = Relationship(back_populates="usuario") 
    # solicitudes_hechas: list["Solicitud"] = Relationship(back_populates="usuario_solicitante")


class EntidadCreate(UserBase):
    rol = "organizacion"
    nit: str | None = Field(default=None, nullable=True)  # Permitir NULL en la DBNone
    tipo_organizacion: Optional[str] = None
    descripcion: str | None = Field(default=None, nullable=True)
    contrasena: str # Para recibir y convertir en hash y pasarlo a la DB


class PublicanteCreate(UserBase):
    rol = "publicante"
    cc: str | None = Field(default=None, nullable=True) 
    contrasena: str # Para recibir y convertir en hash   
 
    
class ReadUser(SQLModel):
    id_usuario: int
    nombre: str
    correo: EmailStr
    telefono: str
    direccion: str
    rol: str
    cc: str | None
    nit: str | None
    tipo_organizacion: Optional[str]
    descripcion: str | None

## ANIMALES ###
