import datetime

from sqlalchemy import create_engine, inspect, select
from sqlalchemy.orm import sessionmaker

from fastapi import FastAPI

from services import service

from schemasPackage import schemasModule

from myPackage import myModule
from modelsPackage import modelsModule as mm

DB_URL = "sqlite:///C:\\Users\\jakub\\Downloads\\blog.db"

engine = create_engine(DB_URL, connect_args={"check_same_thread": False})
connection = engine.connect()
metadata = mm.get_metadata()

metadata.create_all(bind=engine)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
session = SessionLocal()

app = FastAPI()

@app.get("/getUser/{index}")
def getUserById(index: int) -> schemasModule.UserSchema:
    return service.getUserById(session, index)


@app.post("/addUser/{index}")
def getUserById(index: int) -> schemasModule.UserSchema:
    return service.getUserById(session, index)


if __name__ == '__main__':
    print(list(inspect(mm.User).columns))

    user = mm.User(first_name="Anton", last_name="Krotkevich", profile_name="Flor", email="albio@gmail.com",
                   password="1111", country="Ukraine", signup_date=datetime.datetime.now())
    session.add(user)
    session.commit()
    session.refresh(user)

    rows = session.execute(select(mm.User)).fetchall()

    for row in rows:
        print(row)
