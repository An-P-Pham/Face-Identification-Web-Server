from pyimagesearch.facedetector import FaceDetector
import cv2
import os, time

# construct the face detector
fd = FaceDetector('cascades/haarcascade_frontalface_default.xml')
#load the cascade file
face_cascade = cv2.CascadeClassifier('cascades/haarcascade_frontalface_default.xml')

#instructions
status = "Please take photo when box is green"
stop = False

class WebCam(object):
    def __init__(self):
        self.video = cv2.VideoCapture(0)

    def __del__(self):
        self.video.release()

    def get_frame(self):
        while True:
            #grab the current frame
            (success, image) = self.video.read()
            if not success:
                global stop
                stop = True
                break

            image = cv2.resize(image, None, fx=0.6, fy=0.6, interpolation=cv2.INTER_AREA)
            gray =cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            face_rects = face_cascade.detectMultiScale(gray,1.3,5)
            for (x, y, w, h) in face_rects:
                cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)
                break
            cv2.putText(image, status, (20, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.5,
                        (0, 0, 0), 2)
            ret, jpeg = cv2.imencode('.jpg', image)
            return jpeg.tobytes()

    def save_photo(self):
        (grabbed, frame) = self.video.read()
        BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        unknown_faces_dir = os.path.join(BASE_DIR, "unknown")  # unknown faces directory
        os.chdir(unknown_faces_dir)
        cv2.imwrite("unidentified_person.jpg", frame)
        time.sleep(2)

