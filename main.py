from fastapi import FastAPI, Request, WebSocket
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from modules.exercise import Exercise
from config import config
import uvicorn
import cv2


camera = cv2.VideoCapture(config['port_cam'])

app = FastAPI()
exercise = Exercise(cam=camera)
all_con = 0

app.mount("/static", StaticFiles(directory="view/templates/static"), name="static")
templates = Jinja2Templates(directory="view/templates")

@app.get('/')
def index(request: Request):
    return templates.TemplateResponse(
        "index.html", {"request": request, "conexoes": all_con})

@app.get('/start/{id}')
def start(request: Request, id: int):
    new_config = config
    new_config['id'] = id
    new_config["request"] = request
    return templates.TemplateResponse("stream.html", new_config)


@app.websocket("/cam")
async def get_stream(websocket: WebSocket):
    global all_con
    await websocket.accept()

    r = await exercise.view(websocket)