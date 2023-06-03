import requests
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

RESTAPI_URL = "http://127.0.0.1:8000/api"

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")


@app.get("/blog/home", response_class=HTMLResponse)
async def get_home_page(req: Request):
    blogs = requests.get(f'{RESTAPI_URL}/getNMostPopularBlogs?amount_to_display=10')
    return templates.TemplateResponse("index.html", {"request": req, "blogs": blogs.json()})


@app.get("/blog/blog-page/{blog_id}", response_class=HTMLResponse)
async def get_blog_page(req: Request, blog_id: int):
    blog = requests.get(f'{RESTAPI_URL}/getBlog/{blog_id}')
    posts = requests.get(f'{RESTAPI_URL}/getBlogPosts/{blog_id}')
    return templates.TemplateResponse("blog.html", {"request": req, "blog": blog.json(), "posts": posts.json()})
