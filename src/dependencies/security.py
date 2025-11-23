from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from passlib.context import CryptContext # Este es un gestor de contraseñas que permite el cifrado y verificar contraseñas
from db import SessionDep
from models import User
from sqlmodel import select
from datetime import datetime, timedelta
from typing import Optional



gestor_contraseñas = CryptContext(schemes=["sha256_crypt"], deprecated="auto") ## aLGORIRTMO PARA CIFRAR LA CONTRASEÑA
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token") 



def get_password_hash(password: str) -> str:
    """
    Genera la contraseña cifrada

    ARGS:
        password: La contraseña que ingresa el usuario en el registro -> str

    """
    return gestor_contraseñas.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verifica la Contraseña del usuario

    ARGS:
        plain_password: La contraseña que ingresa el usuario -> str
        hashed_password: La contraseñ cifrada del usuario -> str

    """
    return gestor_contraseñas.verify(plain_password, hashed_password)




def autenticated_user(session: SessionDep, emailUser: str, password: str):
    """
    Maneja la logica para ver si un usuario esta autenticado
   
    En caso de estarlo devuelvo el usuario

    ARGS:
        session: La sesion de la base de datos -> Session
        EmailUser: El correo del usuario -> str
        password: La contraseña del usuario -> str
    """
    user_db = session.exec(select(User).where(User.correo == emailUser)).first() 
    if not user_db:
      return False

    if user_db.contrasena_hash is None:
      return False

    if not verify_password(password, user_db.contrasena_hash): ### Verifica si la contraseña es correcta
      return False
    return user_db




# https://chatgpt.com/c/691ff335-1b50-8328-ad61-79f19550510a
