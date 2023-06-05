from typing import Annotated

import requests
from fastapi import FastAPI, Request, Form, Cookie
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

RESTAPI_URL = "http://127.0.0.1:8000/api"

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")


@app.get("/blog/home", response_class=HTMLResponse)
async def get_home_page(req: Request, cookie_id: int = Cookie(None)):
    blogs = requests.get(f'{RESTAPI_URL}/getNMostPopularBlogs?amount_to_display=10').json()
    if cookie_id is not None:
        get_user = requests.get(f'{RESTAPI_URL}/getUser/{cookie_id}')
        if get_user.status_code == 200:
            return templates.TemplateResponse("userPages/index.html", {"request": req, "blogs": blogs, "user": get_user.json()})
    return templates.TemplateResponse("index.html", {"request": req, "blogs": blogs})


@app.get("/blog/login-page", response_class=HTMLResponse)
async def get_login_page(req: Request):
    return templates.TemplateResponse("login.html", {"request": req})


@app.post("/blog/login-user")
async def login_user(req: Request, user_name: Annotated[str, Form()], password: Annotated[str, Form()]):
    user = requests.get(f'{RESTAPI_URL}/getUserByLogin?user_profile_name={user_name}&user_password={password}')
    if user.status_code != 200:
        result = {"title": "Login Failed", "body": user}
        return templates.TemplateResponse("operationResult.html", {"request": req, "result": result})
    result = {"title": "Login Successful", "body": user}
    response = templates.TemplateResponse("operationResult.html", {"request": req, "result": result})
    u = user.json()
    response.set_cookie(key="cookie_id", value=u['id'])
    return response


@app.get("/blog/logout")
async def logout_user(req:Request):
    result = {"title": "Logout Successful"}
    response = templates.TemplateResponse("operationResult.html", {"request": req, "result": result})
    response.delete_cookie(key="cookie_id")
    return response


@app.get("/blog/register-page", response_class=HTMLResponse)
async def get_register_page(req: Request):
    return templates.TemplateResponse("register.html", {"request": req})


# Long as hell, but works, will leave it for now
@app.post("/blog/register-user", response_class=HTMLResponse)
async def register_user(req: Request, first_name: Annotated[str, Form()], last_name: Annotated[str, Form()], user_name: Annotated[str, Form()], email: Annotated[str, Form()], country: Annotated[str, Form()], password: Annotated[str, Form()]):
    user_to_registry = {"first_name": first_name, "last_name": last_name, "profile_name": user_name, "email": email, "country": country, "password": password}
    x = requests.post(f'{RESTAPI_URL}/createUser', json=user_to_registry)
    if x.status_code != 201:
        result = {"title": "Register Failed", "body": x}
        return templates.TemplateResponse("operationResult.html", {"request": req, "result": result})
    result = {"title": "Successful Registration, You can now login", "body": x}
    return templates.TemplateResponse("operationResult.html", {"request": req, "result": result})


@app.get("/blog/blog-page/{blog_id}", response_class=HTMLResponse)
async def get_blog_page(req: Request, blog_id: int):
    blog = requests.get(f'{RESTAPI_URL}/getBlog/{blog_id}')
    posts = requests.get(f'{RESTAPI_URL}/getBlogPosts/{blog_id}')
    if posts.status_code == 404:
        information = [{"title": "This blog has no posts yet"}]
        return templates.TemplateResponse("blog.html", {"request": req, "blog": blog.json(), "posts": information})
    return templates.TemplateResponse("blog.html", {"request": req, "blog": blog.json(), "posts": posts.json()})


@app.get("/blog/post-comments/{post_id}", response_class=HTMLResponse)
async def get_post_comments(req: Request, post_id: int):
    post = requests.get(f'{RESTAPI_URL}/getPost/{post_id}')
    comments = requests.get(f'{RESTAPI_URL}/getPostComments/{post_id}')
    if comments.status_code == 404:
        information = [{"body": "This post has no comments yet"}]
        return templates.TemplateResponse("postsComments.html", {"request": req, "post": post.json(), "comments": information})
    return templates.TemplateResponse("postsComments.html", {"request": req, "post": post.json(), "comments": comments.json()})


@app.get("/blog/user-page/{user_id}", response_class=HTMLResponse)
async def get_home_page(req: Request, user_id: int, cookie_id: int = Cookie(None)):
    user = requests.get(f'{RESTAPI_URL}/getUser/{user_id}').json()
    blogs = requests.get(f'{RESTAPI_URL}/getUserBlogs/{user_id}').json()
    current_user = requests.get(f'{RESTAPI_URL}/getUser/{cookie_id}')
    if current_user.status_code != 200:
        return templates.TemplateResponse("user.html", {"request": req, "user": user.json(), "blogs": blogs})
    if user['id'] == cookie_id:
        return templates.TemplateResponse("userPages/selfUser.html", {"request": req, "user": user, "blogs": blogs})
    else:
        return templates.TemplateResponse("userPages/user.html", {"request": req, "user": user, "blogs": blogs, "current_user": current_user.json()})


@app.get("/blog/create-blog-page", response_class=HTMLResponse)
async def get_create_blog_page(req: Request):
    return templates.TemplateResponse("userPages/createBlog.html", {"request": req})


@app.post("/blog/create-blog")
async def create_blog(req: Request, title: Annotated[str, Form()], description: Annotated[str, Form()], cookie_id: int = Cookie(None)):
    blog_to_create = {"title": title, "description": description}
    x = requests.post(f'{RESTAPI_URL}/createBlog?user_id={cookie_id}', json=blog_to_create)
    if x.status_code != 201:
        result = {"title": "Creation Failed", "body": x}
        return templates.TemplateResponse("operationResult.html", {"request": req, "result": result})
    result = {"title": "Blog has been successfully created", "body": x}
    return templates.TemplateResponse("operationResult.html", {"request": req, "result": result})
