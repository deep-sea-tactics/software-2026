'''
USE X11 Forwarding in case this fails
- Open and run Xming server w/ Xlaunch
- Enable X11 forwarding in the SSH client (Putty) settings
- Run rpicam-hello -t 0 on the RPI; window pops up on local machine

rpi-vid is also viable
- On the RPI:
    - rpicam-vid -t 0 -n --inline --listen -o tcp://0.0.0.0:<port>
- On the local machine, will require both ffplay (FFmpeg) and vlc to be installed:
    - ffplay tcp://192.168.0.2:<port> -vf "setpts=N/30" -fflags nobuffer -flags low_delay -framedrop
    - vlc tcp://192.168.0.2:<port>

The following uses a Flask solution to stream the video feed from the RPI to the local machine.
It requires the least setup up on the local machine as all the libraries are installed on the RPI
This file is ran on the RPI to establish the Flask server
'''
import io
import cv2

cap = cv2.VideoCapture(0) # change this based on ip address of camera feed (ie. 0 for local webcam, or for rpi cam feed, use the ip address of the rpi followed by the port number)

class Camera:
    '''Controls general camera functions'''
    def __init__(self, source):
        self.cap = cv2.VideoCapture(source)

    def get_frame(self):
        '''Get and display a video frame'''
        ret, frame = self.cap.read()

        if not ret:
            print("Can't receive frame (stream end?). Exiting ...")
            return None
        
        cv2.imshow('ROV CAM FEED', frame)

    def release(self):
        '''Close windows'''
        self.cap.release()
        cv2.destroyAllWindows()


if __name__ == "__main__":
    cam = Camera(0)
    while True:
        key = cv2.waitKey(1)
        ret, frame = cam.cap.read()

        cam.get_frame()
        
        if key == ord('s'):
            # Save to file
            cv2.imwrite('frozen_pic.jpg', frame)
            # Show in a separate window to "freeze" it on screen
            cv2.imshow('Frozen Frame', frame)
            print("Frame captured and frozen!")

        if key == ord('q'):
            cam.release()
            break
        

''' 
Unused Flask Solution
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

if __name__ == "__main__":
    app.run(host='192.168.0.2', port=5001)

# Endpoint: http://192.168.0.2:5001/video_feed
'''






