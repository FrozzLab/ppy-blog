import requests
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

RESTAPI_URL = "http://127.0.0.1:8000/api"

app = FastAPI()

app.mount("/static", StaticFiles(directory="src/frontend/static"), name="static")

templates = Jinja2Templates(directory="src/frontend/templates")


@app.get("/home-page", response_class=HTMLResponse)
async def get_home_page(req: Request):
    user = requests.get(f'{RESTAPI_URL}/getUser/17')
    return templates.TemplateResponse("index.html", {"request": req, "user": user.json()})