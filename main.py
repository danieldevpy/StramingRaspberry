from socketify import App, AppOptions, OpCode, CompressOptions
from threading import Thread
import time
import mediapipe as mp
import cv2

all_conn = []


camera = cv2.VideoCapture(0)
draw = mp.solutions.drawing_utils
pose = mp.solutions.pose
Pose = pose.Pose(min_tracking_confidence=0.5, min_detection_confidence=0.5)

def send_all():
    while True:
        if all_conn:
            sucess, img = camera.read()
            ret, buffer = cv2.imencode('.jpg', img, )
            for ws in all_conn:
                ws.send(buffer.tobytes())
        else:
            time.sleep(3)

def ws_open(ws):
    print("A WebSocket got connected!")
    all_conn.append(ws)

def recieve(ws):
    while True:
        ws.recv()

def ws_message(ws, message, opcode):
    print(message, opcode)
    # Ok is false if backpressure was built up, wait for drain
    # ok = ws.send(message, opcode)


app = App()
app.ws(
    "/*",
    {
        "compression": CompressOptions.SHARED_COMPRESSOR,
        "max_payload_length": 16 * 1024 * 1024,
        "idle_timeout": 100000,
        "open": ws_open,
        "message": ws_message,
        "drain": lambda ws: print(
            "WebSocket backpressure: %s", ws.get_buffered_amount()
        ),
        "close": lambda ws, code, message: print("WebSocket closed"),
    },
)
app.any("/", lambda res, req: res.end("Nothing to see here!'"))
app.listen(
    3000,
    lambda config: print("Listening on port http://localhost:%d now\n" % (config.port)),
)

Thread(target=send_all).start()
app.run()
