from fastapi import FastAPI, Request, WebSocket
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from modules.exercise import Exercise
import uvicorn

import time

exercise = Exercise()

app = FastAPI()


app.mount("/static", StaticFiles(directory="view/templates/static"), name="static")
templates = Jinja2Templates(directory="view/templates")

@app.get('/')
def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get('/start/{id}')
def index(request: Request, id: int):
    return templates.TemplateResponse("stream.html", {"request": request, "id": id})



@app.websocket("/cam/{id}")
async def get_stream(websocket: WebSocket, id: int):
    match id:
        case 1:
            await exercise.reconhecimento_facial(websocket)
