from sqlalchemy import select

from fastapi import FastAPI
from schemasPackage import schemasModule

app = FastAPI()

def getUserById(session, index: int) -> schemasModule.UserSchema:
    return session.execute(select(schemasModule.UserSchema).where(schemasModule.UserSchema.user_id == index).limit(1))