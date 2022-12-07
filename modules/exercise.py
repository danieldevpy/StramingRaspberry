import cv2
import mediapipe as mp
from fastapi import WebSocket, WebSocketDisconnect
import asyncio
from threading import Thread


class Exercise:
    

    def __init__(self, cam):
        self.camera = cam
        self.facial_recognition = False
        self.body_recognition = True
        self.rotate = True
        self.reconhecimento_rosto = mp.solutions.face_detection
        self.draw = mp.solutions.drawing_utils
        self.recognition_face = self.reconhecimento_rosto.FaceDetection()
        self.pose = mp.solutions.pose
        self.Pose = self.pose.Pose(min_tracking_confidence=0.5, min_detection_confidence=0.5)
        self.frame = 0


    async def view(self, websocket: WebSocket):
        try:
            while True:
                success, frame = self.camera.read()
                frame = cv2.rotate(frame, cv2.ROTATE_180)
                if self.body_recognition:
                    videoRGB = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                    results = self.Pose.process(videoRGB)
                    points = results.pose_landmarks
                    self.draw.draw_landmarks(frame, points, self.pose.POSE_CONNECTIONS)
                
                ret, buffer = cv2.imencode('.jpg', frame,)
                await websocket.send_bytes(buffer.tobytes())
                # await asyncio.sleep(0)
                
                    
        except WebSocketDisconnect:
            print("Client disconnected")
            return False
                
    async def recieve(self, websocket):
        msg = await websocket.receive_text()
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
