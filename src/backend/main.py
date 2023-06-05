from datetime import datetime

from fastapi import FastAPI, HTTPException
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from src.backend.models import models
from src.backend.schemas import schemas
from src.backend.services import crud

# DB_URL = "sqlite:///D:\\blog.db"
DB_URL = "sqlite:///C:\\Users\\jakub\\Desktop\\studia\\semestr4\\PPY\\py_project\\blog.db"

engine = create_engine(DB_URL, connect_args={"check_same_thread": False})
connection = engine.connect()

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
session = SessionLocal()

metadata = models.get_metadata()
metadata.create_all(bind=engine)

tags_metadata = [
    {
        "name": "user",
        "description": "Operations related to users.",
    },
    {
        "name": "blog",
        "description": "Operations related to blogs.",
    },
    {
        "name": "post",
        "description": "Operations related to posts.",
    },
    {
        "name": "comment",
        "description": "Operations related to comments.",
    },
    {
        "name": "like",
        "description": "Operations related to likes.",
    },
    {
        "name": "save",
        "description": "Operations related to saves.",
    }
]

app = FastAPI(openapi_tags=tags_metadata)


@app.post("/api/createUser", status_code=201, response_model=schemas.UserGetSchema, tags=["user"])
def create_user(new_user: schemas.UserCreateSchema):
    new_user_model = models.User(**new_user.dict(), signup_date=datetime.utcnow())
    crud.create_user(session, new_user_model)
    return new_user_model


@app.post("/api/createBlog", status_code=201, response_model=schemas.BlogGetSchema, tags=["blog"])
def create_blog(new_blog: schemas.BlogCreateSchema, user_id: int):
    return crud.create_blog(session, new_blog, user_id)


@app.post("/api/createPost", status_code=201, response_model=schemas.PostGetSchema, tags=["post"])
def create_post(new_post: schemas.PostCreateSchema):
    return crud.create_post(session, new_post)


@app.post("/api/createComment", status_code=201, response_model=schemas.CommentGetSchema, tags=["comment"])
def create_comment(new_comment_schema: schemas.CommentCreateSchema):
    return crud.create_comment(session, new_comment_schema)


@app.post("/api/createBlogLike", status_code=201, response_model=schemas.BlogLikeGetSchema, tags=["like"])
def create_blog_like(new_blog_like_schema: schemas.BlogLikeCreateSchema):
    return crud.create_blog_like(session, new_blog_like_schema)


@app.post("/api/createPostLike", status_code=201, response_model=schemas.PostLikeGetSchema, tags=["like"])
def create_post_like(new_post_like_schema: schemas.PostLikeCreateSchema):
    return crud.create_post_like(session, new_post_like_schema)


@app.post("/api/createCommentLike", status_code=201, response_model=schemas.CommentLikeGetSchema, tags=["like"])
def create_comment_like(new_comment_like_schema: schemas.CommentLikeCreateSchema):
    return crud.create_comment_like(session, new_comment_like_schema)


@app.post("/api/createBlogSave", status_code=201, response_model=schemas.BlogSaveGetSchema, tags=["save"])
def create_blog_save(new_blog_save_schema: schemas.BlogSaveCreateSchema):
    return crud.create_blog_save(session, new_blog_save_schema)


@app.post("/api/createPostSave", status_code=201, response_model=schemas.PostSaveGetSchema, tags=["save"])
def create_post_save(new_post_save_schema: schemas.PostSaveCreateSchema):
    return crud.create_post_save(session, new_post_save_schema)


@app.post("/api/createCommentSave", status_code=201, response_model=schemas.CommentSaveGetSchema, tags=["save"])
def create_comment_save(new_comment_save_schema: schemas.CommentSaveCreateSchema):
    return crud.create_comment_save(session, new_comment_save_schema)


@app.get("/api/getUser/{user_id}", response_model=schemas.UserGetSchema, tags=["user"])
def get_user_by_id(user_id: int):
    user = crud.get_user_by_id(session, user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user


# Bad solution since the password is shown in plaintext in uri, will fix later
@app.get("/api/getUserByLogin", response_model=schemas.UserGetSchema, tags=["user"])
def get_user_by_name_and_password(user_profile_name: str, user_password: str):
    user = crud.get_user_by_name_and_password(session, user_profile_name, user_password)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@app.get("/api/getUsersByBlog/{blog_id}", response_model=list[schemas.UserGetSchema], tags=["user"])
def get_users_by_blog(blog_id: int):
    users = crud.get_users_by_blog(session, blog_id)
    if not users:
        raise HTTPException(status_code=404, detail="Users not found")
    return users


@app.get("/api/getBlog/{blog_id}", response_model=schemas.BlogGetSchema, tags=["blog"])
def get_blog_by_id(blog_id: int):
    blog = crud.get_blog_by_id(session, blog_id)
    if blog is None:
        raise HTTPException(status_code=404, detail="Blog not found")
    return blog


@app.get("/api/getBlog/{blog_title}", response_model=schemas.BlogGetSchema, tags=["blog"])
def get_blog_by_title(blog_title: str):
    blog = crud.get_blog_by_title(session, blog_title)
    if blog is None:
        raise HTTPException(status_code=404, detail="Blog not found")
    return blog


@app.get("/api/getPost/{post_id}", response_model=schemas.PostGetSchema, tags=["post"])
def get_post_by_id(post_id: int):
    post = crud.get_post_by_id(session, post_id)
    if post is None:
        raise HTTPException(status_code=404, detail="Post not found")
    return post


@app.get("/api/getComment/{comment_id}", response_model=schemas.CommentGetSchema, tags=["comment"])
def get_comment_by_id(comment_id: int):
    comment = crud.get_comment_by_id(session, comment_id)
    if comment is None:
        raise HTTPException(status_code=404, detail="Comment not found")
    return comment


@app.get("/api/getUserBlogs/{user_id}", response_model=list[schemas.BlogGetSchema], tags=["blog"])
def get_user_blogs(user_id: int):
    user_blogs = crud.get_user_blogs(session, user_id)
    if not user_blogs:
        raise HTTPException(status_code=404, detail="No blogs belonging to given user found")
    return user_blogs


@app.get("/api/getBlogPosts/{blog_id}", response_model=list[schemas.PostGetSchema], tags=["post"])
def get_blog_posts(blog_id: int):
    blog_posts = crud.get_blog_posts(session, blog_id)
    if not blog_posts:
        raise HTTPException(status_code=404, detail="No posts belonging to given blog found")
    return blog_posts


@app.get("/api/getPostComments/{post_id}", response_model=list[schemas.CommentGetSchema], tags=["comment"])
def get_post_comments(post_id: int):
    post_comments = crud.get_post_comments(session, post_id)
    if not post_comments:
        raise HTTPException(status_code=404, detail="No comments belonging to given post found")
    return post_comments


@app.get("/api/getUserComments/{user_id}", response_model=list[schemas.CommentGetSchema], tags=["comment"])
def get_user_comments(user_id: int):
    user_comments = crud.get_user_comments(session, user_id)
    if not user_comments:
        raise HTTPException(status_code=404, detail="No comments belonging to given user found")
    return user_comments


@app.get("/api/getUserFollowers/{user_id}", response_model=list[schemas.UserGetSchema], tags=["user"])
def get_user_followers(user_id: int):
    user_followers = crud.get_user_followers(session, user_id)
    if not user_followers:
        raise HTTPException(status_code=404, detail="The user does not exist or has no followers")
    return user_followers


@app.get("/api/getUserFollows/{user_id}", response_model=list[schemas.UserGetSchema], tags=["user"])
def get_user_follows(user_id: int):
    user_follows = crud.get_user_follows(session, user_id)
    if not user_follows:
        raise HTTPException(status_code=404, detail="The user does not exist or does not follow anyone")
    return user_follows


@app.get("/api/getAllUsers", response_model=list[schemas.UserGetSchema], tags=["user"])
def get_all_users():
    users = crud.get_all_users(session)
    if not users:
        raise HTTPException(status_code=404, detail="No users in database")
    return users


@app.get("/api/getAllBlogs", response_model=list[schemas.BlogGetSchema], tags=["blog"])
def get_all_blogs():
    blogs = crud.get_all_blogs(session)
    if not blogs:
        raise HTTPException(status_code=404, detail="No blogs in database")
    return blogs


@app.get("/api/getNMostPopularBlogs", response_model=list[schemas.BlogGetSchema], tags=["blog"])
def get_n_most_popular_blogs(amount_to_display: int):
    blogs = crud.get_n_most_popular_blogs(session, amount_to_display)
    if not blogs:
        raise HTTPException(status_code=404, detail="No blogs in database")
    return blogs


@app.get("/api/getAllPosts", response_model=list[schemas.PostGetSchema], tags=["post"])
def get_all_posts():
    posts = crud.get_all_posts(session)
    if not posts:
        raise HTTPException(status_code=404, detail="No posts in database")
    return posts


@app.get("/api/getAllComments", response_model=list[schemas.CommentGetSchema], tags=["comment"])
def get_all_comments():
    comments = crud.get_all_comments(session)
    if not comments:
        raise HTTPException(status_code=404, detail="No comments in database")
    return comments


@app.put("/api/updateUser/{user_id}", response_model=schemas.UserGetSchema, tags=["user"])
def update_user_by_id(user_update_data: schemas.UserUpdateSchema, user_id: int):
    return crud.update_user_by_id(session, user_update_data, user_id)


@app.put("/api/updateBlog/{blog_id}", response_model=schemas.BlogGetSchema, tags=["blog"])
def update_blog_by_id(blog_update_data: schemas.BlogUpdateSchema, blog_id: int):
    return crud.update_blog_by_id(session, blog_update_data, blog_id)


@app.put("/api/updatePost/{post_id}", response_model=schemas.PostGetSchema, tags=["post"])
def update_post_by_id(post_update_data: schemas.PostUpdateSchema, post_id: int):
    return crud.update_post_by_id(session, post_update_data, post_id)


@app.put("/api/updateComment/{comment_id}", response_model=schemas.CommentGetSchema, tags=["comment"])
def update_comment_by_id(comment_update_data: schemas.CommentUpdateSchema, comment_id: int):
    return crud.update_comment_by_id(session, comment_update_data, comment_id)


@app.delete("/api/deleteUser/{user_id}", status_code=204, tags=["user"])
def delete_user_by_id(user_id: int):
    crud.delete_user_by_id(session, user_id)


@app.delete("/api/deleteBlog/{blog_id}", status_code=204, tags=["blog"])
def delete_blog_by_id(blog_id: int):
    crud.delete_blog_by_id(session, blog_id)


@app.delete("/api/deletePost/{post_id}", status_code=204, tags=["post"])
def delete_post_by_id(post_id: int):
    crud.delete_post_by_id(session, post_id)


@app.delete("/api/deleteComment/{comment_id}", status_code=204, tags=["comment"])
def delete_comment_by_id(comment_id: int):
    crud.delete_comment_by_id(session, comment_id)


@app.delete("/api/deleteBlogLike/{user_id}/{blog_id}", status_code=204, tags=["like"])
def delete_blog_like_by_id(user_id: int, blog_id: int):
    crud.delete_blog_like_by_id(session, user_id, blog_id)


@app.delete("/api/deletePostLike/{user_id}/{post_id}", status_code=204, tags=["like"])
def delete_post_like_by_id(user_id: int, post_id: int):
    crud.delete_post_like_by_id(session, user_id, post_id)


@app.delete("/api/deleteCommentLike/{user_id}/{comment_id}", status_code=204, tags=["like"])
def delete_comment_like_by_id(user_id: int, comment_id: int):
    crud.delete_comment_like_by_id(session, user_id, comment_id)


@app.delete("/api/deleteBlogSave/{user_id}/{blog_id}", status_code=204, tags=["save"])
def delete_blog_save_by_id(user_id: int, blog_id: int):
    crud.delete_blog_save_by_id(session, user_id, blog_id)


@app.delete("/api/deletePostSave/{user_id}/{post_id}", status_code=204, tags=["save"])
def delete_post_save_by_id(user_id: int, post_id: int):
    crud.delete_post_save_by_id(session, user_id, post_id)


@app.delete("/api/deleteCommentSave/{user_id}/{comment_id}", status_code=204, tags=["save"])
def delete_comment_save_by_id(user_id: int, comment_id: int):
    crud.delete_comment_save_by_id(session, user_id, comment_id)
