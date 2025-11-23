from jose import jwt, JWTError
from datetime import datetime, timedelta
from typing import Optional
from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends, HTTPException
from typing import Annotated
from db import SessionDep
from sqlmodel import select
from models import User



oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token") 
tokenDependecy = Annotated[str, Depends(oauth2_scheme)]
SECRET_KEY = "FUTURA_VARIABLE_DE_ENTORNO"
ALGORITHM = "HS256"


def create_access_token(data: dict):
    """
    Crea el token de acceso, Aun trabajo en la funcion requiere Analisis para su correcta implementacion.

    ARGS:
        data: Los datos del usuario -> dict  Ejemplo: {"sub": user.email}}
    """

    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=30)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM) # El Pana JOSE Me firma el TOKEN xd


async def get_current_user(token: tokenDependecy, session: SessionDep):
    """
    Funcion para validar el jwt y la expiracion del mismo.
    
    ARGS:
        token: El token de acceso -> str
        session: La sesion de la base de datos -> SessionDep
    """
    credentials_excep = HTTPException(status_code=401, detail="No entiendo que onda con tus credenciales", headers={"WWW-Authenticate": "Bearer"})   

    try:

        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
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

