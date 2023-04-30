from fastapi import FastAPI, HTTPException
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from models import models as ml
from schemas import schemas as sm
from services import crud

DB_URL = "sqlite:///D:\\blog.db"

engine = create_engine(DB_URL, connect_args={"check_same_thread": False})
connection = engine.connect()

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
session = SessionLocal()

metadata = ml.get_metadata()
metadata.create_all(bind=engine)

app = FastAPI()


@app.get("/getUser/{user_id}", response_model=sm.UserSchema)
def get_user_by_id(user_id: int):
    user = crud.get_user_by_id(session, user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@app.get("/getBlog/{blog_id}", response_model=sm.BlogSchema)
def get_blog_by_id(blog_id: int):
    blog = crud.get_blog_by_id(session, blog_id)
    if blog is None:
        raise HTTPException(status_code=404, detail="Blog not found")
    return blog


@app.get("/getPost/{post_id}", response_model=sm.PostSchema)
def get_post_by_id(post_id: int):
    post = crud.get_post_by_id(session, post_id)
    if post is None:
        raise HTTPException(status_code=404, detail="Post not found")
    return post


@app.get("/getComment/{comment_id}", response_model=sm.CommentSchema)
def get_comment_by_id(comment_id: int):
    comment = crud.get_comment_by_id(session, comment_id)
    if comment is None:
        raise HTTPException(status_code=404, detail="Comment not found")
    return comment
