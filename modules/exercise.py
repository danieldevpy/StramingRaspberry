import cv2
import mediapipe as mp
from fastapi import WebSocket, WebSocketDisconnect


class Exercise:
    

    def __init__(self):
        self.camera = cv2.VideoCapture(0)


    async def reconhecimento_facial(self, websocket: WebSocket):
        reconhecimento_rosto = mp.solutions.face_detection
        desenho = mp.solutions.drawing_utils
        reconhecedor_rosto = reconhecimento_rosto.FaceDetection()
        await websocket.accept()
        try:
            while True:
                success, frame = self.camera.read()
                # frame = cv2.rotate(frame, cv2.ROTATE_180)
                lista_rostos = reconhecedor_rosto.process(frame)
                if lista_rostos.detections:
                    for rosto in lista_rostos.detections:
                        desenho.draw_detection(frame, rosto)
                if not success:
                    break
                else:
                    ret, buffer = cv2.imencode('.jpg', frame,)
                    await websocket.send_bytes(buffer.tobytes())  

        except WebSocketDisconnect:
                print("Client disconnected")
    
