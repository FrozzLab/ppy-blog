from fastapi import FastAPI, HTTPException
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from uuid import UUID

from src.backend.models.models import get_metadata
from src.backend.schemas.create_schemas import UserCreateSchema, BlogCreateSchema, PostCreateSchema, \
    CommentCreateSchema, BlogLikeCreateSchema, PostLikeCreateSchema, CommentLikeCreateSchema, BlogSaveCreateSchema, \
    PostSaveCreateSchema, CommentSaveCreateSchema
from src.backend.schemas.get_schemas import UserGetSchema, BlogGetSchema, PostGetSchema, CommentGetSchema, \
    BlogLikeGetSchema, PostLikeGetSchema, CommentLikeGetSchema, CommentSaveGetSchema, PostSaveGetSchema, \
    BlogSaveGetSchema
from src.backend.schemas.update_schemas import PostUpdateSchema, BlogUpdateSchema, CommentUpdateSchema, UserUpdateSchema
from src.backend.services import create, delete, get, update

DB_URL = "sqlite:///D:\\blog.db"

engine = create_engine(DB_URL, connect_args={"check_same_thread": False}, echo=True)
connection = engine.connect()

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
session = SessionLocal()

metadata = get_metadata()
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


@app.post("/api/createUser", status_code=200, response_model=UserGetSchema, tags=["user"])
def create_user(new_user_schema: UserCreateSchema):
    return create.create_user(session, new_user_schema)


@app.post("/api/createBlog", status_code=200, response_model=BlogGetSchema, tags=["blog"])
def create_blog(new_blog_schema: BlogCreateSchema):
    return create.create_blog(session, new_blog_schema)


@app.post("/api/createPost", status_code=200, response_model=PostGetSchema, tags=["post"])
def create_post(new_post_schema: PostCreateSchema):
    return create.create_post(session, new_post_schema)


@app.post("/api/createComment", status_code=200, response_model=CommentGetSchema, tags=["comment"])
def create_comment(new_comment_schema: CommentCreateSchema):
    return create.create_comment(session, new_comment_schema)


@app.post("/api/createBlogLike", status_code=200, response_model=BlogLikeGetSchema, tags=["like"])
def create_blog_like(new_blog_like_schema: BlogLikeCreateSchema):
    return create.create_blog_like(session, new_blog_like_schema)


@app.post("/api/createPostLike", status_code=200, response_model=PostLikeGetSchema, tags=["like"])
def create_post_like(new_post_like_schema: PostLikeCreateSchema):
    return create.create_post_like(session, new_post_like_schema)


@app.post("/api/createCommentLike", status_code=200, response_model=CommentLikeGetSchema, tags=["like"])
def create_comment_like(new_comment_like_schema: CommentLikeCreateSchema):
    return create.create_comment_like(session, new_comment_like_schema)


@app.post("/api/createBlogSave", status_code=200, response_model=BlogSaveGetSchema, tags=["save"])
def create_blog_save(new_blog_save_schema: BlogSaveCreateSchema):
    return create.create_blog_save(session, new_blog_save_schema)


@app.post("/api/createPostSave", status_code=200, response_model=PostSaveGetSchema, tags=["save"])
def create_post_save(new_post_save_schema: PostSaveCreateSchema):
    return create.create_post_save(session, new_post_save_schema)


@app.post("/api/createCommentSave", status_code=200, response_model=CommentSaveGetSchema, tags=["save"])
def create_comment_save(new_comment_save_schema: CommentSaveCreateSchema):
    return create.create_comment_save(session, new_comment_save_schema)


@app.get("/api/getUser/{user_uuid}", response_model=UserGetSchema, tags=["user"])
def get_user_by_uuid(user_uuid: UUID):
    user = get.get_user_by_uuid(session, user_uuid)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user


# Bad solution since the password is shown in plaintext in url, will fix later
# TODO: fix get_user_by_name_and_password to not expose user password
@app.get("/api/getUserByLogin", response_model=UserGetSchema, tags=["user"])
def get_user_by_name_and_password(user_profile_name: str, user_password: str):
    user = get.get_user_by_username_and_password(session, user_profile_name, user_password)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@app.get("/api/getUsersByBlog/{blog_uuid}", response_model=list[UserGetSchema], tags=["user"])
def get_users_by_blog(blog_uuid: UUID):
    users = get.get_users_by_blog(session, blog_uuid)
    if not users:
        raise HTTPException(status_code=404, detail="Users not found")
    return users


@app.get("/api/getBlog/{blog_uuid}", response_model=BlogGetSchema, tags=["blog"])
def get_blog_by_uuid(blog_uuid: UUID):
    blog = get.get_blog_by_uuid(session, blog_uuid)
    if blog is None:
        raise HTTPException(status_code=404, detail="Blog not found")
    return blog


@app.get("/api/getBlog/{blog_title}", response_model=BlogGetSchema, tags=["blog"])
def get_blog_by_title(blog_title: str):
    blog = get.get_blog_by_title(session, blog_title)
    if blog is None:
        raise HTTPException(status_code=404, detail="Blog not found")
    return blog


@app.get("/api/getPost/{post_uuid}", response_model=PostGetSchema, tags=["post"])
def get_post_by_uuid(post_uuid: UUID):
    post = get.get_post_by_uuid(session, post_uuid)
    if post is None:
        raise HTTPException(status_code=404, detail="Post not found")
    return post


@app.get("/api/getComment/{comment_uuid}", response_model=CommentGetSchema, tags=["comment"])
def get_comment_by_uuid(comment_uuid: UUID):
    comment = get.get_comment_by_uuid(session, comment_uuid)
    if comment is None:
        raise HTTPException(status_code=404, detail="Comment not found")
    return comment


@app.get("/api/getUserBlogs/{user_uuid}", response_model=list[BlogGetSchema], tags=["blog"])
def get_user_blogs_by_uuid(user_uuid: UUID):
    user_blogs = get.get_user_blogs_by_uuid(session, user_uuid)
    if not user_blogs:
        raise HTTPException(status_code=404, detail="No blogs belonging to given user found")
    return user_blogs


@app.get("/api/getBlogPosts/{blog_uuid}", response_model=list[PostGetSchema], tags=["post"])
def get_blog_posts_by_uuid(blog_uuid: UUID):
    blog_posts = get.get_blog_posts_by_uuid(session, blog_uuid)
    if not blog_posts:
        raise HTTPException(status_code=404, detail="No posts belonging to given blog found")
    return blog_posts


@app.get("/api/getPostComments/{post_uuid}", response_model=list[CommentGetSchema], tags=["comment"])
def get_post_comments_by_uuid(post_uuid: UUID):
    post_comments = get.get_post_comments_by_uuid(session, post_uuid)
    if not post_comments:
        raise HTTPException(status_code=404, detail="No comments belonging to given post found")
    return post_comments


@app.get("/api/getUserComments/{user_uuid}", response_model=list[CommentGetSchema], tags=["comment"])
def get_user_comments_by_uuid(user_uuid: UUID):
    user_comments = get.get_user_comments_by_uuid(session, user_uuid)
    if not user_comments:
        raise HTTPException(status_code=404, detail="No comments belonging to given user found")
    return user_comments


@app.get("/api/getUserFollowers/{user_uuid}", response_model=list[UserGetSchema], tags=["user"])
def get_user_followers_by_uuid(user_uuid: UUID):
    user_followers = get.get_user_followers_by_uuid(session, user_uuid)
    if not user_followers:
        raise HTTPException(status_code=404, detail="The user does not exist or has no followers")
    return user_followers


@app.get("/api/getUserFollows/{user_uuid}", response_model=list[UserGetSchema], tags=["user"])
def get_user_follows_by_uuid(user_uuid: UUID):
    user_follows = get.get_user_follows_by_uuid(session, user_uuid)
    if not user_follows:
        raise HTTPException(status_code=404, detail="The user does not exist or does not follow anyone")
    return user_follows


@app.get("/api/getAllUsers", response_model=list[UserGetSchema], tags=["user"])
def get_all_users():
    users = get.get_all_users(session)
    if not users:
        raise HTTPException(status_code=404, detail="No users in database")
    return users


@app.get("/api/getAllBlogs", response_model=list[BlogGetSchema], tags=["blog"])
def get_all_blogs():
    blogs = get.get_all_blogs(session)
    if not blogs:
        raise HTTPException(status_code=404, detail="No blogs in database")
    return blogs


@app.get("/api/getNMostPopularBlogs", response_model=list[BlogGetSchema], tags=["blog"])
def get_n_most_popular_blogs(amount_to_display: int):
    blogs = get.get_n_most_popular_blogs(session, amount_to_display)
    if not blogs:
        raise HTTPException(status_code=404, detail="No blogs in database")
    return blogs


@app.get("/api/getAllPosts", response_model=list[PostGetSchema], tags=["post"])
def get_all_posts():
    posts = get.get_all_posts(session)
    if not posts:
        raise HTTPException(status_code=404, detail="No posts in database")
    return posts


@app.get("/api/getAllComments", response_model=list[CommentGetSchema], tags=["comment"])
def get_all_comments():
    comments = get.get_all_comments(session)
    if not comments:
        raise HTTPException(status_code=404, detail="No comments in database")
    return comments


@app.put("/api/updateUser/{user_uuid}", response_model=UserGetSchema, tags=["user"])
def update_user_by_uuid(user_update_data: UserUpdateSchema, user_uuid: UUID):
    return update.update_user_by_uuid(session, user_update_data, user_uuid)


@app.put("/api/updateBlog/{blog_uuid}", response_model=BlogGetSchema, tags=["blog"])
def update_blog_by_uuid(blog_update_data: BlogUpdateSchema, blog_id: UUID):
    return update.update_blog_by_uuid(session, blog_update_data, blog_id)


@app.put("/api/updatePost/{post_uuid}", response_model=PostGetSchema, tags=["post"])
def update_post_by_uuid(post_update_data: PostUpdateSchema, post_id: UUID):
    return update.update_post_by_uuid(session, post_update_data, post_id)


@app.put("/api/updateComment/{comment_uuid}", response_model=CommentGetSchema, tags=["comment"])
def update_comment_by_uuid(comment_update_data: CommentUpdateSchema, comment_id: UUID):
    return update.update_comment_by_uuid(session, comment_update_data, comment_id)


@app.delete("/api/deleteUser/{user_uuid}", status_code=204, tags=["user"])
def delete_user_by_uuid(user_uuid: UUID):
    delete.delete_user_by_uuid(session, user_uuid)


@app.delete("/api/deleteBlog/{blog_uuid}", status_code=204, tags=["blog"])
def delete_blog_by_uuid(blog_uuid: UUID):
    delete.delete_blog_by_uuid(session, blog_uuid)


@app.delete("/api/deletePost/{post_uuid}", status_code=204, tags=["post"])
def delete_post_by_uuid(post_uuid: UUID):
    delete.delete_post_by_uuid(session, post_uuid)


@app.delete("/api/deleteComment/{comment_uuid}", status_code=204, tags=["comment"])
def delete_comment_by_uuid(comment_uuid: UUID):
    delete.delete_comment_by_uuid(session, comment_uuid)


@app.delete("/api/deleteBlogLike/{user_uuid}/{blog_uuid}", status_code=204, tags=["like"])
def delete_blog_like_by_uuid(user_uuid: UUID, blog_uuid: UUID):
    delete.delete_blog_like_by_uuid(session, user_uuid, blog_uuid)


@app.delete("/api/deletePostLike/{user_uuid}/{post_uuid}", status_code=204, tags=["like"])
def delete_post_like_by_uuid(user_uuid: UUID, post_uuid: UUID):
    delete.delete_post_like_by_uuid(session, user_uuid, post_uuid)


@app.delete("/api/deleteCommentLike/{user_uuid}/{comment_uuid}", status_code=204, tags=["like"])
def delete_comment_like_by_uuid(user_uuid: UUID, comment_uuid: UUID):
    delete.delete_comment_like_by_uuid(session, user_uuid, comment_uuid)


@app.delete("/api/deleteBlogSave/{user_uuid}/{blog_uuid}", status_code=204, tags=["save"])
def delete_blog_save_by_uuid(user_uuid: UUID, blog_uuid: UUID):
    delete.delete_blog_save_by_uuid(session, user_uuid, blog_uuid)


@app.delete("/api/deletePostSave/{user_uuid}/{post_uuid}", status_code=204, tags=["save"])
def delete_post_save_by_uuid(user_uuid: UUID, post_uuid: UUID):
    delete.delete_post_save_by_uuid(session, user_uuid, post_uuid)


@app.delete("/api/deleteCommentSave/{user_uuid}/{comment_uuid}", status_code=204, tags=["save"])
def delete_comment_save_by_uuid(user_uuid: UUID, comment_uuid: UUID):
    delete.delete_comment_save_by_uuid(session, user_uuid, comment_uuid)
