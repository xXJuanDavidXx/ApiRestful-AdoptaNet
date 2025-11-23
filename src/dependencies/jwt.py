from jose import jwt, JWTError
from datetime import datetime, timedelta
from typing import Optional




SECRET_KEY = "FUTURA_VARIABLE_DE_ENTORNO"
ALGORITHM = "HS256"


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    """
    Crea el token de acceso, Aun trabajo en la funcion requiere Analisis para su correcta implementacion.

    ARGS:
        data: Los datos del usuario -> dict  Ejemplo: {"sub": user.email}}
        expires_delta: La duracion del token -> timedelta
    """

    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM) # El Pana JOSE Me firma el TOKEN xd



