import websockets
import asyncio
import mediapipe as mp
import cv2


class SocketServer:
    def __init__(self):
        self.all_connections = []
        self.camera = cv2.VideoCapture(0)
        self.draw = mp.solutions.drawing_utils
        self.pose = mp.solutions.pose
        self.Pose = self.pose.Pose(min_tracking_confidence=0.5, min_detection_confidence=0.5)

    async def send_all(self):
        print('thread de enviar iniciada')
        while True:
            if self.all_connections:
                success, frame = self.camera.read()
                frame = cv2.rotate(frame, cv2.ROTATE_180)
                # videoRGB = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                results = self.Pose.process(frame)
                # points = results.pose_landmarks
                # self.draw.draw_landmarks(frame, points, self.pose.POSE_CONNECTIONS)
                ret, buffer = cv2.imencode('.jpg', frame, )
                for conn in self.all_connections:
                    await conn.send(buffer.tobytes())
            await asyncio.sleep(0)

    async def new_client_connect(self, client_socket, path):
        print('New client connect!')
        self.all_connections.append(client_socket)
        while True:
            # await client_socket.send('teste')
            message = await client_socket.recv()
            print("Client sent:", message)

    async def start_server(self):
        print('Server started!')
        await websockets.serve(self.new_client_connect, "192.168.1.21", 8000)



if __name__ == "__main__":
    server = SocketServer()
    event_loop = asyncio.get_event_loop()
    event_loop.run_until_complete(server.start_server())
    event_loop.run_until_complete(server.send_all())
    event_loop.run_forever()
