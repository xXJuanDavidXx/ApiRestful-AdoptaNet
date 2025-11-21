from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from passlib.context import CryptContext
from db import Session
from models import User


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


def autenticated_user(session: Session, user: str, password: str):
    user_db = session.get(User, user)
    if not user_db:
        return False
    if not verify_password(password, user_db.hashed_password):
        return False
    return user_db



# https://chatgpt.com/c/691ff335-1b50-8328-ad61-79f19550510a
