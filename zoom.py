import cv2
from threading import Thread
import dlib
from imutils import face_utils
import imutils


class Zoom:
    def __init__(self, src):
        self.stream = cv2.VideoCapture(src)
        _, self.frame = self.stream.read()
        self.zoom = imutils.resize(self.frame,100)
        #self.src = src
        self.stopped = False
        print('Loading Facial Landmark ...')
        self.detector = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
        self.predictor = dlib.shape_predictor('shape_predictor_68_face_landmarks.dat')

    def start(self):
        t = Thread(target=self.update, args=())
        t.daemon = True
        t.start()
        return self

    def update(self):
        while True:
            if self.stopped:
                return
            _, self.frame = self.stream.read()
            self.zoom = imutils.resize(self.frame,100)
            self.gray = cv2.cvtColor(self.zoom, cv2.COLOR_BGR2GRAY)
            self.rects = self.detector.detectMultiScale(self.gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30), flags=cv2.CASCADE_SCALE_IMAGE)
            
    def readShape(self):
        for (x, y, w, h) in self.rects:
            self.rect = dlib.rectangle(int(x), int(y), int(x + w), int(y + h))
            self.shape = face_utils.shape_to_np(self.predictor(self.gray, self.rect))
            return self.shape

    def stop(self):
        self.stopped = True
