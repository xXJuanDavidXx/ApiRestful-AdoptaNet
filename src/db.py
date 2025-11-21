from sqlmodel import Session, create_engine, SQLModel
from typing import Annotated
from fastapi import Depends, FastAPI



engine = create_engine("mysql+pymysql://admin:password@localhost:3306/adoptanet")


def create_tables(app: FastAPI):
	SQLModel.metadata.create_all(engine)
	yield # Con esto decimos que el control de la funcionalidad a FastAPi

def get_session():
	with Session(engine) as session:
		yield session # 



SessionDep = Annotated[Session, Depends(get_session)]

