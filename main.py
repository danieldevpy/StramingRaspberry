from fastapi import FastAPI, Request, WebSocket
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from modules.exercise import Exercise
import uvicorn
import asyncio
import cv2


import time

app = FastAPI()

all_con = 0
camera = cv2.VideoCapture(0)

app.mount("/static", StaticFiles(directory="view/templates/static"), name="static")
templates = Jinja2Templates(directory="view/templates")

@app.get('/')
def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request, "con": all_con})

@app.get('/start/{id}')
def start(request: Request, id: int):
    return templates.TemplateResponse("stream.html", {"request": request, "id": id})


@app.websocket("/cam")
async def get_stream(websocket: WebSocket):
    global all_con
    await websocket.accept()
    e = Exercise(cam=camera)
    all_con += 1
    r = await e.view(websocket)
    if r:
        pass
    else:
        all_con -= 1
        