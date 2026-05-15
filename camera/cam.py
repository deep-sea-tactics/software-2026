'''
USE X11 Forwarding in case this fails
- Open and run Xming server w/ Xlaunch
- Enable X11 forwarding in the SSH client (Putty) settings
- Run rpicam-hello -t 0 on the RPI; window pops up on local machine
rpi-vid is also usuable IF this is the Linux native laptop
'''

''' This is ran on the RPI!!! '''

import io
import cv2
# These two directories should be donwnloaded on the RPI, but are not necessary for the local machine
import picamera2
from flask import Flask, Response

app = Flask(__name__)

@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

def generate_frames():
    # Implementation for generating video frames
    camera = picamera2.Picamera2()
    camera.resolution = (640, 480)
    camera.framerate = 24
    stream = io.BytesIO()

    for _ in camera.capture_continuous(stream, format='jpeg', use_video_port=True):
        stream.seek(0)
        frame = stream.read()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
        stream.seek(0)
        stream.truncate()

# Endpoint: http://192.168.0.2:5000/video_feed

'''''''''''''''
cap = cv2.VideoCapture(0) # change this based on ip address of camera feed (ie. 0 for local webcam, or for rpi cam feed, use the ip address of the rpi followed by the port number)

if not cap.isOpened():
    print("Cannot open camera")
    exit()

while True:
    ret, frame = cap.read()

    if not ret:
        print("Can't receive frame (stream end?). Exiting ...")
        break

    cv2.imshow('ROV CAM FEED', frame)
    if cv2.waitKey(1) == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()

class Camera:
    def __init__(self, source):
        self.cap = cv2.VideoCapture(source)
    

    def get_frame(self):
        ret, frame = self.cap.read()

        if not ret:
            print("Can't receive frame (stream end?). Exiting ...")
            return None
        
        cv2.imshow('ROV CAM FEED', frame)
        

    def release(self):
        self.cap.release()
        cv2.destroyAllWindows()


if __name__ == "__main__":
    cam = Camera(0)
    while True:
        
        cam.get_frame()
        
        if cv2.waitKey(1) == ord('q'):
            cam.release()
            break
'''''''''







