import websockets
import asyncio
import mediapipe as mp
import cv2
import math

class SocketServer:
    def __init__(self):
        self.all_connections = []
        self.camera = cv2.VideoCapture(0)
        self.draw = mp.solutions.drawing_utils
        self.pose = mp.solutions.pose
        self.Pose = self.pose.Pose(min_tracking_confidence=0.5, min_detection_confidence=0.5)

    async def send_all(self):
        check = True
        contador = 0
        print('thread de enviar iniciada')
        while True:
            if self.all_connections:
                sucess, img = self.camera.read()
                img = cv2.rotate(img, cv2.ROTATE_180)
                videoRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
                results = self.Pose.process(videoRGB)
                points = results.pose_landmarks
                self.draw.draw_landmarks(img, points, self.pose.POSE_CONNECTIONS)

                h, w, y = img.shape
                # print(f'h: {h}, w: {w}, y:{y}')
                if points:
                    # mão direita
                    
                    x_mao_direita = int(points.landmark[self.pose.PoseLandmark.RIGHT_INDEX].x * w)
                    y_mao_direita = int(points.landmark[self.pose.PoseLandmark.RIGHT_INDEX].y * h)
                    # mão esquerda
                    x_mao_esquerda = int(points.landmark[self.pose.PoseLandmark.LEFT_INDEX].x * w)
                    y_mao_esquerda = int(points.landmark[self.pose.PoseLandmark.LEFT_INDEX].y * h)
                    # pé direito
                    x_pe_direito = int(points.landmark[self.pose.PoseLandmark.RIGHT_FOOT_INDEX].x * w)
                    y_pe_direito = int(points.landmark[self.pose.PoseLandmark.RIGHT_FOOT_INDEX].y * h)
                    # pé esquerdo
                    x_pe_esquerdo = int(points.landmark[self.pose.PoseLandmark.LEFT_FOOT_INDEX].x * w)
                    y_pe_esquerdo = int(points.landmark[self.pose.PoseLandmark.LEFT_FOOT_INDEX].y * h)

                    distancia_maos = math.hypot(x_mao_direita - x_mao_esquerda, y_mao_direita - y_mao_esquerda)
                    distancia_pes = math.hypot(x_pe_direito - x_pe_esquerdo, y_pe_direito - y_pe_esquerdo)
                    cv2.putText(img, f'QNTD: {contador}', (20, 100), cv2.FONT_HERSHEY_SIMPLEX, 2, (255,0,0), 2)
                    # print(f'Distancia das mãos: {distancia_maos}')
                    # print(f'Distancia dos pés: {distancia_pes}')
                    if check and distancia_maos <= 50 and distancia_pes >= 120:
                        contador += 1
                        check = False
                    if not check and distancia_maos > 50 and distancia_pes < 120:
                        check = True
                ret, buffer = cv2.imencode('.jpg', img, )
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
        await websockets.serve(self.new_client_connect, "192.168.1.21", 8080)



if __name__ == "__main__":
    server = SocketServer()
    event_loop = asyncio.get_event_loop()
    event_loop.run_until_complete(server.start_server())
    event_loop.run_until_complete(server.send_all())
    event_loop.run_forever()
                # success, frame = self.camera.read()
                # frame = cv2.rotate(frame, cv2.ROTATE_180)
                # videoRGB = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                # results = self.Pose.process(videoRGB)
                # points = results.pose_landmarks
                # self.draw.draw_landmarks(frame, points, self.pose.POSE_CONNECTIONS)