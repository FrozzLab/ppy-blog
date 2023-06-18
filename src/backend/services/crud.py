from typing import Type

from fastapi import HTTPException
from sqlalchemy import desc, func
from sqlalchemy.orm import Session
from uuid import uuid4

from src.backend.models import *
from src.backend.schemas import *


def create_user(session: Session, new_user_schema: UserCreateSchema) -> User:
    existing_user_model = get_user_by_username(session, new_user_schema.profile_name)

    if existing_user_model is not None:
        raise HTTPException(status_code=400, detail="User with given profile name already exists")

    new_user_model = User(**new_user_schema.dict(), created_at=datetime.utcnow())
    new_user_model.uuid = uuid4()

    session.add(new_user_model)
    session.commit()
    session.refresh(new_user_model)

    return new_user_model


def create_blog(session: Session, new_blog_schema: BlogCreateSchema) -> Blog:
    user_creator_model = get_user_by_id(session, new_blog_schema.user_id)

    if user_creator_model is None:
        raise HTTPException(status_code=404, detail="Blog creator does not exist")

    existing_blog_model = get_blog_by_title(session, new_blog_schema.title)

    if existing_blog_model is not None:
        raise HTTPException(status_code=400, detail="Blog with given title already exists")

    new_blog_dict = new_blog_schema.dict()
    del new_blog_dict["user_id"]

    new_blog_model = Blog(**new_blog_dict, created_at=datetime.utcnow())
    new_blog_model.uuid = uuid4()
    new_blog_model.owners.append(user_creator_model)

    session.add(new_blog_model)
    session.commit()
    session.refresh(new_blog_model)

    return new_blog_model


def create_post(session: Session, new_post_schema: PostCreateSchema) -> Post:
    parent_blog_model = get_blog_by_id(session, new_post_schema.blog_id)

    if parent_blog_model is None:
        raise HTTPException(status_code=404, detail="Parent blog does not exist")

    user_creator_model = get_user_by_id(session, new_post_schema.user_id)

    if user_creator_model is None:
        raise HTTPException(status_code=404, detail="Post creator does not exist")

    creator_blogs = get_user_blogs(session, user_creator_model.id)

    if parent_blog_model not in creator_blogs:
        raise HTTPException(status_code=400, detail="User does not own blog")

    existing_post_model = get_post_by_title(session, new_post_schema.title, new_post_schema.blog_id)

    if existing_post_model is not None:
        raise HTTPException(status_code=400, detail="Post with given title already exists in given blog")

    new_post_model = Post(**new_post_schema.dict(), created_at=datetime.utcnow())
    new_post_model.uuid = uuid4()
    new_post_model.user = user_creator_model
    new_post_model.blog = parent_blog_model

    session.add(new_post_model)
    session.commit()
    session.refresh(new_post_model)

    return new_post_model


def create_comment(session: Session, new_comment_schema: CommentCreateSchema) -> Comment:
    parent_post_model = get_post_by_id(session, new_comment_schema.post_id)

    if parent_post_model is None:
        raise HTTPException(status_code=404, detail="Parent post does not exist")

    user_creator_model = get_user_by_id(session, new_comment_schema.user_id)

    if user_creator_model is None:
        raise HTTPException(status_code=404, detail="Comment creator does not exist")

    new_comment_model = Comment(**new_comment_schema.dict(), created_at=datetime.utcnow())
    new_comment_model.uuid = uuid4()
    new_comment_model.user = user_creator_model
    new_comment_model.post = parent_post_model

    session.add(new_comment_model)
    session.commit()
    session.refresh(new_comment_model)

    return new_comment_model


def create_blog_like(session: Session, new_like_schema: BlogLikeCreateSchema) -> BlogLike:
    liking_user_model = get_user_by_id(session, new_like_schema.user_id)

    if liking_user_model is None:
        raise HTTPException(status_code=404, detail="Liking user does not exist")

    liked_blog_model = get_blog_by_id(session, new_like_schema.blog_id)

    if liked_blog_model is None:
        raise HTTPException(status_code=404, detail="Liked blog does not exist")

    existing_blog_like_model = get_blog_like_by_id(session, new_like_schema.user_id, new_like_schema.blog_id)

    if existing_blog_like_model is not None:
        raise HTTPException(status_code=400, detail="Blog has already been liked")

    new_like_model = BlogLike(**new_like_schema.dict(), liked_at=datetime.utcnow())
    new_like_model.user = liking_user_model
    new_like_model.blog = liked_blog_model

    session.add(new_like_model)
    session.commit()
    session.refresh(new_like_model)

    return new_like_model


def create_post_like(session: Session, new_like_schema: PostLikeCreateSchema) -> PostLike:
    liking_user_model = get_user_by_id(session, new_like_schema.user_id)

    if liking_user_model is None:
        raise HTTPException(status_code=404, detail="Liking user does not exist")

    liked_post_model = get_post_by_id(session, new_like_schema.post_id)

    if liked_post_model is None:
        raise HTTPException(status_code=404, detail="Liked post does not exist")

    existing_post_like_model = get_post_like_by_id(session, new_like_schema.user_id, new_like_schema.post_id)

    if existing_post_like_model is not None:
        raise HTTPException(status_code=400, detail="Post has already been liked")

    new_like_model = PostLike(**new_like_schema.dict(), liked_at=datetime.utcnow())
    new_like_model.user = liking_user_model
    new_like_model.post = liked_post_model

    session.add(new_like_model)
    session.commit()
    session.refresh(new_like_model)

    return new_like_model


def create_comment_like(session: Session, new_like_schema: CommentLikeCreateSchema) -> CommentLike:
    liking_user_model = get_user_by_id(session, new_like_schema.user_id)

    if liking_user_model is None:
        raise HTTPException(status_code=404, detail="Liking user does not exist")

    liked_comment_model = get_comment_by_id(session, new_like_schema.comment_id)

    if liked_comment_model is None:
        raise HTTPException(status_code=404, detail="Liked comment does not exist")

    existing_comment_like_model = get_comment_like_by_id(session, new_like_schema.user_id, new_like_schema.comment_id)

    if existing_comment_like_model is not None:
        raise HTTPException(status_code=400, detail="Comment has already been liked")

    new_like_model = CommentLike(**new_like_schema.dict(), liked_at=datetime.utcnow())
    new_like_model.user = liking_user_model
    new_like_model.comment = liked_comment_model

    session.add(new_like_model)
    session.commit()
    session.refresh(new_like_model)

    return new_like_model


def create_blog_save(session: Session, new_save_schema: BlogSaveCreateSchema) -> BlogSave:
    saving_user_model = get_user_by_id(session, new_save_schema.user_id)

    if saving_user_model is None:
        raise HTTPException(status_code=404, detail="Saving user does not exist")

    saving_blog_model = get_blog_by_id(session, new_save_schema.blog_id)

    if saving_blog_model is None:
        raise HTTPException(status_code=404, detail="Saved blog does not exist")

    existing_blog_save_model = get_blog_save_by_id(session, new_save_schema.user_id, new_save_schema.blog_id)

    if existing_blog_save_model is not None:
        raise HTTPException(status_code=400, detail="Blog has already been saved")

    new_save_model = BlogSave(**new_save_schema.dict(), saved_at=datetime.utcnow())
    new_save_model.user = saving_user_model
    new_save_model.blog = saving_blog_model

    session.add(new_save_model)
    session.commit()
    session.refresh(new_save_model)

    return new_save_model


def create_post_save(session: Session, new_save_schema: PostSaveCreateSchema) -> PostSave:
    saving_user_model = get_user_by_id(session, new_save_schema.user_id)

    if saving_user_model is None:
        raise HTTPException(status_code=404, detail="Saving user does not exist")

    saved_post_model = get_post_by_id(session, new_save_schema.post_id)

    if saved_post_model is None:
        raise HTTPException(status_code=404, detail="Saved post does not exist")

    existing_post_save_model = get_post_save_by_id(session, new_save_schema.user_id, new_save_schema.post_id)

    if existing_post_save_model is not None:
        raise HTTPException(status_code=400, detail="Post has already been saved")

    new_save_model = PostSave(**new_save_schema.dict(), saved_at=datetime.utcnow())
    new_save_model.user = saving_user_model
    new_save_model.post = saved_post_model

    session.add(new_save_model)
    session.commit()
    session.refresh(new_save_model)

    return new_save_model


def create_comment_save(session: Session, new_save_schema: CommentSaveCreateSchema) -> CommentSave:
    saving_user_model = get_user_by_id(session, new_save_schema.user_id)

    if saving_user_model is None:
        raise HTTPException(status_code=404, detail="Saving user does not exist")

    saved_comment_model = get_comment_by_id(session, new_save_schema.comment_id)

    if saved_comment_model is None:
        raise HTTPException(status_code=404, detail="Saved comment does not exist")

    existing_comment_save_model = get_comment_save_by_id(session, new_save_schema.user_id, new_save_schema.comment_id)

    if existing_comment_save_model is not None:
        raise HTTPException(status_code=400, detail="Comment has already been saved")

    new_save_model = CommentSave(**new_save_schema.dict(), saved_at=datetime.utcnow())
    new_save_model.user = saving_user_model
    new_save_model.comment = saved_comment_model

    session.add(new_save_model)
    session.commit()
    session.refresh(new_save_model)

    return new_save_model


def get_user_by_id(session: Session, user_id: int) -> Type[User] | None:
    return session.query(User).filter(User.id == user_id).first()


def get_user_by_uuid(session: Session, user_uuid: UUID) -> Type[User] | None:
    return session.query(User).filter(User.uuid == user_uuid).first()


def get_user_by_username(session: Session, user_profile_name: str) -> Type[User] | None:
    return session.query(User).filter(User.profile_name == user_profile_name).first()


def get_user_by_username_and_password(session: Session, 
                                      user_profile_name: str, 
                                      user_password: str) -> Type[User] | None:
    return session.query(User). \
        filter(User.profile_name == user_profile_name 
               and User.password == user_password). \
        first()


def get_users_by_blog(session: Session, blog_id: int) -> list[Type[User]]:
    return session.query(User). \
        join(UserBlog, UserBlog.user_id == User.id). \
        filter(UserBlog.blog_id == blog_id). \
        all()


def get_blog_by_id(session: Session, blog_id: int) -> Type[Blog] | None:
    return session.query(Blog).filter(Blog.id == blog_id).first()


def get_blog_by_uuid(session: Session, blog_uuid: UUID) -> Type[Blog] | None:
    return session.query(Blog).filter(Blog.uuid == blog_uuid).first()


def get_blog_by_title(session: Session, blog_title: str) -> Type[Blog] | None:
    return session.query(Blog).filter(Blog.title == blog_title).first()


def get_post_by_id(session: Session, post_id: int) -> Type[Post] | None:
    return session.query(Post).filter(Post.id == post_id).first()


def get_post_by_uuid(session: Session, post_uuid: UUID) -> Type[Post] | None:
    return session.query(Post).filter(Post.uuid == post_uuid).first()


# Requires a relevant blog ID to be passed as the website allows for
# posts with the same name to appear across multiple blogs
def get_post_by_title(session: Session, post_title: str, blog_id: int) -> Type[Post] | None:
    return session.query(Post).filter(Post.title == post_title and Post.blog.id == blog_id).first()


def get_comment_by_id(session: Session, comment_id: int) -> Type[Comment] | None:
    return session.query(Comment).filter(Comment.id == comment_id).first()


def get_user_blogs(session: Session, user_id: int) -> list[Type[Blog]]:
    return session.query(Blog). \
        join(UserBlog, UserBlog.blog_id == Blog.id). \
        filter(UserBlog.user_id == user_id). \
        all()


def get_blog_posts(session: Session, blog_id: int) -> list[Type[Post]]:
    return session.query(Post).filter(Post.blog_id == blog_id).all()


def get_post_comments(session: Session, post_id: int) -> list[Type[Comment]]:
    return session.query(Comment).filter(Comment.post_id == post_id).all()


def get_user_comments(session: Session, user_id: int) -> list[Type[Comment]]:
    return session.query(Comment).filter(Comment.user_id == user_id).all()


def get_user_followers(session: Session, user_uuid: str) -> list[Type[User]]:
    user = session.query(User).filter(User.uuid == user_uuid).first()
    follower_associations = user.follower_associations if user else []
    followers = []

    for follower_association in follower_associations:
        followers.append(follower_association.follower)

    return followers


def get_user_follows(session: Session, user_uuid: str) -> list[Type[User]]:
    user = session.query(User).filter(User.uuid == user_uuid).first()
    follow_associations = user.follow_associations if user else []
    follows = []

    for follow_association in follow_associations:
        follows.append(follow_association.user)

    return follows


def get_all_users(session: Session) -> list[Type[User]]:
    return session.query(User).all()


def get_all_blogs(session: Session) -> list[Type[Blog]]:
    return session.query(Blog).all()


def get_n_most_popular_blogs(session: Session, amount_to_display: int) -> list[Type[Blog]]:
    return session.query(Blog). \
        outerjoin(BlogLike, BlogLike.blog_id == Blog.id). \
        order_by(desc(func.count(BlogLike.user_id))). \
        group_by(Blog.id). \
        limit(amount_to_display).all()


def get_all_posts(session: Session) -> list[Type[Post]]:
    return session.query(Post).all()


def get_all_comments(session: Session) -> list[Type[Comment]]:
    return session.query(Comment).all()


def get_blog_like_by_id(session: Session, user_id: int, blog_id: int) -> Type[BlogLike] | None:
    return session.query(BlogLike).\
        filter(BlogLike.user_id == user_id
               and BlogLike.blog_id == blog_id).\
        first()


def get_blog_save_by_id(session: Session, user_id: int, blog_id: int) -> Type[BlogSave] | None:
    return session.query(BlogSave).\
        filter(BlogSave.user_id == user_id
               and BlogSave.blog_id == blog_id).\
        first()


def get_post_like_by_id(session: Session, user_id: int, post_id: int) -> Type[PostLike] | None:
    return session.query(PostLike).\
        filter(PostLike.user_id == user_id
               and PostLike.post_id == post_id).\
        first()


def get_post_save_by_id(session: Session, user_id: int, post_id: int) -> Type[PostSave] | None:
    return session.query(PostSave).\
        filter(PostSave.user_id == user_id
               and PostSave.post_id == post_id).\
        first()


def get_comment_like_by_id(session: Session, user_id: int, comment_id: int) -> Type[CommentLike] | None:
    return session.query(CommentLike).\
        filter(CommentLike.user_id == user_id
               and CommentLike.comment_id == comment_id).\
        first()


def get_comment_save_by_id(session: Session, user_id: int, comment_id: int) -> Type[CommentSave] | None:
    return session.query(CommentSave).\
        filter(CommentSave.user_id == user_id
               and CommentSave.comment_id == comment_id).\
        first()


def update_user_by_uuid(session: Session, user_update_data: UserUpdateSchema, user_uuid: str) -> Type[User]:
    given_user_model = get_user_by_uuid(session, user_uuid)

    if given_user_model is None:
        raise HTTPException(status_code=404, detail="User queued for update does not exist")

    for var, value in vars(user_update_data).items():
        setattr(given_user_model, var, value) if value else None

    session.add(given_user_model)
    session.commit()
    session.refresh(given_user_model)

    return given_user_model


def update_blog_by_id(session: Session, blog_update_data: BlogUpdateSchema, blog_id: int) -> Type[Blog]:
    given_blog_model = get_blog_by_uuid(session, blog_id)

    if given_blog_model is None:
        raise HTTPException(status_code=404, detail="Blog queued for update does not exist")

    for var, value in vars(blog_update_data).items():
        setattr(given_blog_model, var, value) if value else None

    session.add(given_blog_model)
    session.commit()
    session.refresh(given_blog_model)

    return given_blog_model


def update_post_by_id(session: Session, post_update_data: PostUpdateSchema, post_id: int) -> Type[Post]:
    given_post_model = get_post_by_uuid(session, post_id)

    if given_post_model is None:
        raise HTTPException(status_code=404, detail="Post queued for update does not exist")

    for var, value in vars(post_update_data).items():
        setattr(given_post_model, var, value) if value else None

    session.add(given_post_model)
    session.commit()
    session.refresh(given_post_model)

    return given_post_model


def update_comment_by_id(session: Session, 
                         comment_update_data: CommentUpdateSchema, 
                         comment_id: int) -> Type[Comment]:
    given_comment_model = get_comment_by_id(session, comment_id)

    if given_comment_model is None:
        raise HTTPException(status_code=404, detail="Comment queued for update does not exist")

    for var, value in vars(comment_update_data).items():
        setattr(given_comment_model, var, value) if value else None

    session.add(given_comment_model)
    session.commit()
    session.refresh(given_comment_model)

    return given_comment_model


def delete_user_by_id(session: Session, user_id: int) -> None:
    session.query(User).filter(User.id == user_id).delete()
    session.commit()


def delete_blog_by_id(session: Session, blog_id: int) -> None:
    session.query(Blog).filter(Blog.id == blog_id).delete()
    session.commit()


def delete_post_by_id(session: Session, post_id: int) -> None:
    session.query(Post).filter(Post.id == post_id).delete()
    session.commit()


def delete_comment_by_id(session: Session, comment_id: int) -> None:
    session.query(Comment).filter(Comment.id == comment_id).delete()
    session.commit()


def delete_blog_like_by_id(session: Session, user_id: int, blog_id: int) -> None:
    session.query(BlogLike). \
        filter(BlogLike.user_id == user_id,
               BlogLike.blog_id == blog_id). \
        delete()

    session.commit()


def delete_post_like_by_id(session: Session, user_id: int, post_id: int) -> None:
    session.query(PostLike). \
        filter(PostLike.user_id == user_id,
               PostLike.post_id == post_id). \
        delete()

    session.commit()


def delete_comment_like_by_id(session: Session, user_id: int, comment_id: int) -> None:
    session.query(CommentLike). \
        filter(CommentLike.user_id == user_id,
               CommentLike.comment_id == comment_id). \
        delete()

    session.commit()


def delete_blog_save_by_id(session: Session, user_id: int, blog_id: int) -> None:
    session.query(BlogSave). \
        filter(BlogSave.user_id == user_id,
               BlogSave.blog_id == blog_id). \
        delete()

    session.commit()


def delete_post_save_by_id(session: Session, user_id: int, post_id: int) -> None:
    session.query(PostSave). \
        filter(PostSave.user_id == user_id,
               PostSave.post_id == post_id). \
        delete()

    session.commit()


def delete_comment_save_by_id(session: Session, user_id: int, comment_id: int) -> None:
    session.query(CommentSave). \
        filter(CommentSave.user_id == user_id,
               CommentSave.comment_id == comment_id). \
        delete()

    session.commit()
