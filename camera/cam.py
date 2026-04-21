import cv2


"""
cap = cv2.VideoCapture(192.168.0.1) # change this based on ip address of camera feed (ie. 0 for local webcam, or for rpi cam feed, use the ip address of the rpi followed by the port number)

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
"""


class Camera:
    def __init__(self, source):
        self.cap = cv2.VideoCapture(source)
    
    def release(self):
        self.cap.release()
        cv2.destroyAllWindows()

    def get_frame(self):
        ret, frame = self.cap.read()
        if not ret:
            print("Can't receive frame (stream end?). Exiting ...")
            return 
        
        cv2.imshow('ROV CAM FEED', frame)
        

    def release(self):
        self.cap.release()
        cv2.destroyAllWindows()

cam = Camera(0)

while True:
    
    cam.get_frame
    
    if cv2.waitKey(1) == ord('q'):
        cam.release()



