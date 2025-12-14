from jose import jwt, JWTError
from datetime import datetime, timedelta, timezone
from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends, HTTPException
from typing import Annotated
from ..db import SessionDep
from sqlmodel import select
from ..models import User
from ..config import settings



oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token") 
tokenDependecy = Annotated[str, Depends(oauth2_scheme)]


def create_access_token(data: dict):
    """

    ARGS:
        data: Los datos del usuario -> dict  Ejemplo: {"sub": user.email}}
    """

    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM) # El Pana JOSE Me firma el TOKEN xd


async def get_current_user(token: tokenDependecy, session: SessionDep):
    """
    Funcion para validar el jwt y la expiracion del mismo.
    
    ARGS:
        token: El token de acceso -> str
        session: La sesion de la base de datos -> SessionDep
    """
    credentials_excep = HTTPException(status_code=401, detail="O estas desautenticado o el token es invalido o estas husmeando por ahí", headers={"WWW-Authenticate": "Bearer"})   

    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]) #se decodifica y se verifica el token
        correo = payload.get("sub")
        if correo is None:
            raise credentials_excep
    except JWTError: ## Esta excepcion se lanza cuando el token es invalido o expirado
        raise credentials_excep
        
    user = session.exec(select(User).where(User.correo == correo)).first()
    if user is None:
        raise credentials_excep
    return user        


depGetCurrentUser = Annotated[User, Depends(get_current_user)]

