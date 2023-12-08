# main.py
from fastapi import FastAPI
from fastapi import FastAPI, Request
from routes.transaction import transaction_router

from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from database.connection import conn

app = FastAPI()

# Mount the templates directory as static files
app.mount("/static", StaticFiles(directory="/home/amd/App/templates"), name="static")


templates = Jinja2Templates(directory="templates")

app.include_router( transaction_router, prefix="/user")

@app.get("/")
def home(request: Request):
	message = "Computelabs payment services"
	return templates.TemplateResponse("index.html", {"request": request, "message": message})

@app.on_event("startup")
def on_startup():
    conn()
