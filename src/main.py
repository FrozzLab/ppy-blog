import datetime

from sqlalchemy import create_engine, inspect, select
from sqlalchemy.orm import sessionmaker

from myPackage import myModule
from modelsPackage import modelsModule as mm

DB_URL = "sqlite:///D:\\blog.db"

engine = create_engine(DB_URL, connect_args={"check_same_thread": False})
connection = engine.connect()
metadata = mm.get_metadata()

metadata.create_all(bind=engine)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
session = SessionLocal()

if __name__ == '__main__':
    print(dir(myModule))
    myModule.say_hi("Kuba")
    myModule.my_age(21)
    print(list(inspect(mm.User).columns))

    user = mm.User(first_name="Anton", last_name="Krotkevich", profile_name="Flor", email="albio@gmail.com",
                   password="1111", country="Ukraine", signup_date=datetime.datetime.now())
    session.add(user)
    session.commit()
    session.refresh(user)

    rows = session.execute(select(mm.User)).fetchall()

    for row in rows:
        print(row)
