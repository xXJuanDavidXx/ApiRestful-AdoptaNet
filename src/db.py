from sqlmodel import Session, create_engine, SQLModel
from typing import Annotated
from fastapi import Depends, FastAPI
from .config import settings



engine = create_engine(settings.DATABASE_URL)


def create_tables(app: FastAPI):
	SQLModel.metadata.create_all(engine)
	yield # Con esto decimos que el control de la funcionalidad a FastAPi

def get_session():
	with Session(engine) as session:
		yield session # 



SessionDep = Annotated[Session, Depends(get_session)]

