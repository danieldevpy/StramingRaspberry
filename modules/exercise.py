import cv2
import mediapipe as mp
from fastapi import WebSocket, WebSocketDisconnect


class Exercise:
    

    def __init__(self):
        self.camera = cv2.VideoCapture(0)
        
    async def normal_cam(self, websocket: WebSocket):
        await websocket.accept()
        try:
            while True:
                success, frame = self.camera.read()
                if not success:
                    break
                else:
                    frame = cv2.rotate(frame, cv2.ROTATE_180)
                    ret, buffer = cv2.imencode('.jpg', frame,)
                    await websocket.send_bytes(buffer.tobytes())
                    msg = await websocket.receive_text()
                    if msg:
                        print(msg)
                        if msg == 'exit':
                            await websocket.close()

                    
        except WebSocketDisconnect:
            print("Client disconnected")

    async def reconhecimento_facial(self, websocket: WebSocket):
        await websocket.accept()
        reconhecimento_rosto = mp.solutions.face_detection
        desenho = mp.solutions.drawing_utils
        reconhecedor_rosto = reconhecimento_rosto.FaceDetection()
        try:
            while True:
                success, frame = self.camera.read()
                if not success:
                    break
                else:
                    frame = cv2.rotate(frame, cv2.ROTATE_180)
                    lista_rostos = reconhecedor_rosto.process(frame)
                    if lista_rostos.detections:
                        for rosto in lista_rostos.detections:
                            desenho.draw_detection(frame, rosto)
                    ret, buffer = cv2.imencode('.jpg', frame,)
                    await websocket.send_bytes(buffer.tobytes())
                    msg = await websocket.receive_text()
                    if msg:
                        print(websocket, msg)
                        if msg == 'exit':
                            await websocket.close()


        except WebSocketDisconnect:
                print("Client disconnected")
    
