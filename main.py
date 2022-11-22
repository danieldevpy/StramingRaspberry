from fastapi import FastAPI, Request, WebSocket, WebSocketDisconnect
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
import mediapipe as mp
import uvicorn
import cv2
import time



app = FastAPI()
camera = cv2.VideoCapture(0)
reconhecimento_rosto = mp.solutions.face_detection
desenho = mp.solutions.drawing_utils
reconhecedor_rosto = reconhecimento_rosto.FaceDetection()

app.mount("/static", StaticFiles(directory="view/templates/static"), name="static")
templates = Jinja2Templates(directory="view/templates")

@app.get('/')
def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get('/facial')
def index(request: Request):
    return templates.TemplateResponse("stream.html", {"request": request})

@app.websocket("/ws")
async def get_stream(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            success, frame = camera.read()
            frame = cv2.rotate(frame, cv2.ROTATE_180)
            lista_rostos = reconhecedor_rosto.process(frame)
            if lista_rostos.detections:
                for rosto in lista_rostos.detections:
                    desenho.draw_detection(frame, rosto)
            if not success:
                break
            else:
                ret, buffer = cv2.imencode('.jpg', frame)
                await websocket.send_bytes(buffer.tobytes())  

    except WebSocketDisconnect:
        print("Client disconnected")
        
if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000)
 
