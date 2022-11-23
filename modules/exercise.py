import cv2
import mediapipe as mp
from fastapi import WebSocket, WebSocketDisconnect


class Exercise:
    

    def __init__(self, cam):
        self.camera = cam
        self.websocket = None
        self.facial_recognition = False
        self.body_recognition = False
        self.recieve = True
        self.rotate = True
        self.reconhecimento_rosto = mp.solutions.face_detection
        self.desenho = mp.solutions.drawing_utils
        self.reconhecedor_rosto = self.reconhecimento_rosto.FaceDetection()

    async def start(self, websocket: WebSocket):
        self.websocket = websocket
        try:
            while True:
                success, frame = self.camera.read()
                if not success:
                    break
                else:
                    if self.rotate:
                        frame = cv2.rotate(frame, cv2.ROTATE_180)
                    if self.facial_recognition:
                        lista_rostos = self.reconhecedor_rosto.process(frame)
                        if lista_rostos.detections:
                            for rosto in lista_rostos.detections:
                                self.desenho.draw_detection(frame, rosto)
                       
                    ret, buffer = cv2.imencode('.jpg', frame,)
                    await websocket.send_bytes(buffer.tobytes())
                    if self.recieve:
                        self.commands();

        except WebSocketDisconnect:
            print("Client disconnected")
                
    async def commands(self):
        msg = self.websocket.receive_text()
        if msg == 'exit':
            await self.websocket.close()