from scipy.spatial import distance as dist
from imutils.video import VideoStream
from imutils.video import FPS
from imutils import face_utils
from threading import Thread
from pyimagesearch.tempimage import TempImage
import numpy as np
import os
import dropbox
import imutils
import dlib
import cv2
#from picamera.array import PiRGBArray
#from picamera import PiCamera
import time
import datetime

def sound_alarm():
	os.system('aplay alarm.wav')
def sound_focus():
	os.system('aplay focus.wav')

def eye_aspect_ratio(eye):
	A = dist.euclidean(eye[1], eye[5])
	B = dist.euclidean(eye[2], eye[4])
	C = dist.euclidean(eye[0], eye[3])
	eye = (A + B) / (2.0 * C)
	return eye
def mouth_ratio(mouth):
	AB = dist.euclidean(mouth[12],mouth[16])
	CD = dist.euclidean(mouth[13],mouth[19])
	EF = dist.euclidean(mouth[14],mouth[18])
	GH = dist.euclidean(mouth[15],mouth[17])
	mouth = (CD+EF+GH)/(3.0*AB)
	return mouth
 
EYE_THRESH = 0.12
EYE_CONTINOUS_FRAMES = 3
MOUTH_THRESH = 0.25
MOUTH_CONTINOUS_FRAMES = 4
FOCUS_CONTINOUS_FRAMES = 4
FREQ = 8

EYE_COUNTER = 0
MOUTH_COUNTER = 0
FOCUS_COUNTER = 0

MOUTH_ALARM_ON = False
EYE_ALARM_ON = False
EYE_RECORD = False
MOUTH_RECORD = False
FOCUS = True
STATE = None
# Define the codec and create VideoWriter object
fourcc = cv2.VideoWriter_fourcc(*'XVID')

client = dropbox.Dropbox("unQ5Wyy9mgAAAAAAAAAACiWorvEgb7ytXApRtaMWb5BNdk1gSVCdv3XGclHnnzC6")
print("[SUCCESS] API Dropbox Signed-in")

print('Loading Facial Landmark ...')
detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor('shape_predictor_68_face_landmarks.dat')

(lStart, lEnd) = face_utils.FACIAL_LANDMARKS_IDXS["left_eye"]
(rStart, rEnd) = face_utils.FACIAL_LANDMARKS_IDXS["right_eye"]
(mouthStart, mouthEnd) = face_utils.FACIAL_LANDMARKS_IDXS['mouth']
 
print("Starting Video Stream Thread ...")
vs = VideoStream(0).start()

time.sleep(1.0)

lastUploaded = datetime.datetime.now()

fps = FPS().start()

while True:
	#frame = image.array
	frame = vs.read()
	frame = imutils.resize(frame, width=400, height=300)
	gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
	rects = detector(gray, 0)

	timestamp = datetime.datetime.now()
	ts = timestamp.strftime("%A %d %B %Y %I:%M:%S%p")
	
	cv2.putText(frame, ts, (5,290), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (0,0,255),2)

	STATE=1
	if STATE is 1:
		FOCUS_COUNTER += 1
		if (FOCUS_COUNTER == FOCUS_CONTINOUS_FRAMES):
			FOCUS_COUNTER = 0
			FOCUS = False
			tt = Thread(target=sound_focus)
			tt.setDaemon(True)
			tt.start()
		if not FOCUS:
			cv2.putText(frame, "Tap Trung!", (300, 20),cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)

	for rect in rects:
		shape = predictor(gray, rect)
		shape = face_utils.shape_to_np(shape)

		STATE = type(shape)
		if STATE is np.ndarray:
			FOCUS = True
			FOCUS_COUNTER = 0

		leftEye = shape[lStart:lEnd]
		rightEye = shape[rStart:rEnd]
		mouth = shape[mouthStart:mouthEnd]
		avr_mouth = mouth_ratio(mouth)

		avr_eye = (eye_aspect_ratio(leftEye) + eye_aspect_ratio(rightEye)) / 2.0
		
		for item in mouth:
			cv2.circle(frame,tuple(item), 1, (0,255,0), 1)
		for item in leftEye:
			cv2.circle(frame,tuple(item), 1, (0,255,0), 1)
		for item in rightEye:
			cv2.circle(frame,tuple(item), 1, (0,255,0), 1)
		
		if avr_eye < EYE_THRESH:
			EYE_COUNTER += 1

			if not EYE_RECORD:
				EYE_RECORD = True
				# init path
				tt = TempImage()
				# create a new blank video file
				eyeOUTPUT = cv2.VideoWriter(tt.path,fourcc,10.0,(400,300))
			# start recording each frame
			eyeOUTPUT.write(frame)

			if EYE_COUNTER >= EYE_CONTINOUS_FRAMES:
				if not EYE_ALARM_ON:
					EYE_ALARM_ON = True
					t = Thread(target=sound_alarm)
					t.setDaemon(True)
					t.start()

				cv2.putText(frame, "Ngu Gat!", (300, 40),
					cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)

		elif EYE_ALARM_ON:
			EYE_ALARM_ON = False
			EYE_COUNTER = 0
			EYE_RECORD = False
			eyeOUTPUT.release()
			if (timestamp - lastUploaded).seconds >= FREQ:
				try:
					path = "/{base_path}/{timestamp}.avi".format(base_path="Drowsiness", timestamp=ts)
					client.files_upload(open(tt.path,"rb").read(), path)
					tt.cleanup()
					print("UPLOAD COMPLETE")
					lastUploaded = timestamp
				except:
					print('Kiem tra ket noi internet')

		else:
			EYE_COUNTER = 0
		
		if avr_mouth > MOUTH_THRESH:
			MOUTH_COUNTER += 1

			if not MOUTH_RECORD:
				MOUTH_RECORD = True
				# init path
				tt = TempImage()
				# create a new blank video file
				mouthOUTPUT = cv2.VideoWriter(tt.path,fourcc,10.0,(400,300))
			# start recording each frame
			mouthOUTPUT.write(frame)

			if MOUTH_COUNTER >= MOUTH_CONTINOUS_FRAMES:
				if not MOUTH_ALARM_ON:
					MOUTH_ALARM_ON = True
					t = Thread(target=sound_alarm)
					t.setDaemon(True)
					t.start()

				cv2.putText(frame, "NGAP!", (300, 60),
					cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)

		elif MOUTH_ALARM_ON:
			MOUTH_ALARM_ON = False
			MOUTH_COUNTER = 0
			MOUTH_RECORD = False
			mouthOUTPUT.release()
			if (timestamp - lastUploaded).seconds >= FREQ:
				try:
					path = "/{base_path}/{timestamp}.avi".format(base_path="Drowsiness", timestamp=ts)
					client.files_upload(open(tt.path,"rb").read(), path)
					tt.cleanup()
					print("UPLOAD thanh cong")
					lastUploaded = timestamp
				except:
					print('Check Your Connection')
					
		else:
			MOUTH_COUNTER = 0

		cv2.putText(frame, "MAT: {:.2f}".format(avr_eye), (10, 40),
			cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
		cv2.putText(frame, "MIENG: {:.2f}".format(avr_mouth), (10, 60),
			cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
	fps.update()
	fps.stop()
	cv2.putText(frame, "FPS: {:.2f}".format(fps.fps()), (10, 20),
			cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
 
	cv2.imshow("Frame", frame)
	key = cv2.waitKey(1) & 0xFF
	
	if key == ord("q"):
		break

cv2.destroyAllWindows()
vs.stop()
