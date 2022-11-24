import cv2
import mediapipe as mp
from fastapi import WebSocket, WebSocketDisconnect
import asyncio


class Exercise:
    

    def __init__(self, cam):
        self.camera = cam
        self.websocket = None
        self.facial_recognition = False
        self.body_recognition = False
        self.rotate = True
        self.reconhecimento_rosto = mp.solutions.face_detection
        self.draw = mp.solutions.drawing_utils
        self.recognition_face = self.reconhecimento_rosto.FaceDetection()
        self.pose = mp.solutions.pose
        self.Pose = self.pose.Pose(min_tracking_confidence=0.5, min_detection_confidence=0.5)
        self.frame = 0
        

    async def view(self, websocket: WebSocket):
        self.websocket = websocket
        try:
            while True:
                success, frame = self.camera.read()
                self.frame += 1
                if self.frame >= 60:
                    print('recebendo')
                    self.frame = 0
                    await asyncio.sleep(0.01)
               
                frame = cv2.rotate(frame, cv2.ROTATE_180)
                videoRGB = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                results = self.Pose.process(videoRGB)
                points = results.pose_landmarks
                self.draw.draw_landmarks(frame, points, self.pose.POSE_CONNECTIONS)
                
                ret, buffer = cv2.imencode('.jpg', frame,)
                await websocket.send_bytes(buffer.tobytes())
                
                    
        except WebSocketDisconnect:
            print("Client disconnected")
            return False
                
    async def commands(self):
        msg = await self.websocket.receive_text()
        if msg:
            if msg == 'facial':
                if self.facial_recognition:
                    self.facial_recognition = False
                else:
                    self.facial_recognition = True
            if msg == 'rotate':
                if self.rotate:
                    self.rotate = False
                else:
                    self.rotate = True
            elif msg == 'exit':
                await self.websocket.close()
