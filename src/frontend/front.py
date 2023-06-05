from typing import Annotated

import requests
from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

RESTAPI_URL = "http://127.0.0.1:8000/api"

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")


@app.get("/blog/home", response_class=HTMLResponse)
async def get_home_page(req: Request):
    blogs = requests.get(f'{RESTAPI_URL}/getNMostPopularBlogs?amount_to_display=10').json()
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
    return templates.TemplateResponse("operationResult.html", {"request": req, "result": result})


@app.get("/blog/register-page", response_class=HTMLResponse)
async def get_register_page(req: Request):
    return templates.TemplateResponse("register.html", {"request": req})


# Long as hell, but works, will leave it for now
@app.post("/blog/register-user", response_class=HTMLResponse)
async def register_user(req: Request, first_name: Annotated[str, Form()], last_name: Annotated[str, Form()], user_name: Annotated[str, Form()], email: Annotated[str, Form()], country: Annotated[str, Form()], password: Annotated[str, Form()]):
    user_to_registry = {"first_name": first_name, "last_name": last_name, "profile_name": user_name, "email": email, "country": country, "password": password}
    x = requests.post(f'{RESTAPI_URL}/createUser', json=user_to_registry)
    if x.status_code != 200:
        result = {"title": "Register Failed", "body": x}
        return templates.TemplateResponse("operationResult.html", {"request": req, "result": result})
    result = {"title": "Successful Registration", "body": x}
    return templates.TemplateResponse("operationResult.html", {"request": req, "result": result})


@app.get("/blog/blog-page/{blog_id}", response_class=HTMLResponse)
async def get_blog_page(req: Request, blog_id: int):
    blog = requests.get(f'{RESTAPI_URL}/getBlog/{blog_id}')
    posts = requests.get(f'{RESTAPI_URL}/getBlogPosts/{blog_id}')
    return templates.TemplateResponse("blog.html", {"request": req, "blog": blog.json(), "posts": posts.json()})
