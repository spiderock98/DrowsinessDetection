### Dropbox + full dlib + Qt5 ####

from imutils.video import VideoStream, FPS
from imutils import face_utils
from threading import Thread
import os
import cv2
import time
import imutils
from PyQt5 import QtCore, QtGui, QtWidgets
from scipy.spatial import distance as dist
import numpy as np
import dlib
import subprocess
# import playsound
# import winsound
# from pyfirmata import ArduinoNano, util
import glob
# import serial
# import cameraindex
import dropbox
from pyimagesearch.tempimage import TempImage
import datetime


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(617, 729)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        # self.comboPort = QtWidgets.QComboBox(self.centralwidget)
        # self.comboPort.setGeometry(QtCore.QRect(150, 20, 91, 25))
        # self.comboPort.setObjectName("comboPort")
        # self.lbPort = QtWidgets.QLabel(self.centralwidget)
        # self.lbPort.setGeometry(QtCore.QRect(60, 20, 71, 21))
        # self.lbPort.setObjectName("lbPort")
        self.btnStart = QtWidgets.QPushButton(self.centralwidget)
        self.btnStart.setGeometry(QtCore.QRect(420, 150, 111, 25))
        self.btnStart.setObjectName("btnStart")
        self.progressBar = QtWidgets.QProgressBar(self.centralwidget)
        self.progressBar.setGeometry(QtCore.QRect(10, 190, 591, 41))
        self.progressBar.setProperty("value", 0)
        self.progressBar.setObjectName("progressBar")
        self.spinEye = QtWidgets.QDoubleSpinBox(self.centralwidget)
        self.spinEye.setGeometry(QtCore.QRect(150, 15, 69, 31))
        self.spinEye.setAccelerated(False)
        self.spinEye.setMaximum(0.5)
        self.spinEye.setSingleStep(0.01)
        self.spinEye.setProperty("value", float(settings.value('spinEye')))
        self.spinEye.setObjectName("spinEye")
        self.lbEyeThread = QtWidgets.QLabel(self.centralwidget)
        self.lbsEyeThread.setGeometry(QtCore.QRect(20, 20, 121, 21))
        self.lbEyeThread.setObjectName("lbEyeThread")
        self.lbMouthThread = QtWidgets.QLabel(self.centralwidget)
        self.lbMouthThread.setGeometry(QtCore.QRect(10, 60, 131, 31))
        self.lbMouthThread.setObjectName("lbMouthThread")
        self.spinMouth = QtWidgets.QDoubleSpinBox(self.centralwidget)
        self.spinMouth.setGeometry(QtCore.QRect(150, 60, 69, 31))
        self.spinMouth.setMaximum(0.5)
        self.spinMouth.setSingleStep(0.01)
        self.spinMouth.setProperty("value", 0.27)
        self.spinMouth.setObjectName("spinMouth")
        self.slideEye = QtWidgets.QSlider(self.centralwidget)
        self.slideEye.setGeometry(QtCore.QRect(390, 60, 160, 21))
        self.slideEye.setMaximum(50)
        self.slideEye.setSliderPosition(int(settings.value('lbEyeNum')))
        self.slideEye.setOrientation(QtCore.Qt.Horizontal)
        self.slideEye.setObjectName("slideEye")
        self.lbEyeFrame = QtWidgets.QLabel(self.centralwidget)
        self.lbEyeFrame.setGeometry(QtCore.QRect(260, 60, 121, 17))
        self.lbEyeFrame.setObjectName("lbEyeFrame")
        self.lbMouthFrame = QtWidgets.QLabel(self.centralwidget)
        self.lbMouthFrame.setGeometry(QtCore.QRect(260, 100, 121, 21))
        self.lbMouthFrame.setObjectName("lbMouthFrame")
        self.slideMouth = QtWidgets.QSlider(self.centralwidget)
        self.slideMouth.setGeometry(QtCore.QRect(390, 100, 160, 21))
        self.slideMouth.setMaximum(50)
        self.slideMouth.setSliderPosition(int(settings.value('lbMouthNum')))
        self.slideMouth.setOrientation(QtCore.Qt.Horizontal)
        self.slideMouth.setObjectName("slideMouth")
        self.comboSource = QtWidgets.QComboBox(self.centralwidget)
        self.comboSource.setGeometry(QtCore.QRect(390, 20, 91, 21))
        self.comboSource.setObjectName("comboSource")
        self.lbCam = QtWidgets.QLabel(self.centralwidget)
        self.lbCam.setGeometry(QtCore.QRect(260, 20, 121, 20))
        self.lbCam.setObjectName("lbCam")
        self.checkShow = QtWidgets.QCheckBox(self.centralwidget)
        self.checkShow.setGeometry(QtCore.QRect(20, 160, 171, 21))
        self.checkShow.setLayoutDirection(QtCore.Qt.RightToLeft)
        self.checkShow.setObjectName("checkShow")
        self.lbEyeNum = QtWidgets.QLabel(self.centralwidget)
        self.lbEyeNum.setGeometry(QtCore.QRect(560, 60, 67, 21))
        self.lbEyeNum.setObjectName("lbEyeNum")
        self.lbMouthNum = QtWidgets.QLabel(self.centralwidget)
        self.lbMouthNum.setGeometry(QtCore.QRect(560, 100, 67, 21))
        self.lbMouthNum.setObjectName("lbMouthNum")
        self.spinSize = QtWidgets.QSpinBox(self.centralwidget)
        self.spinSize.setGeometry(QtCore.QRect(220, 150, 48, 21))
        self.spinSize.setMinimum(50)
        self.spinSize.setMaximum(1000)
        self.spinSize.setProperty("value", settings.value('spinSize'))
        self.spinSize.setSingleStep(10)
        self.spinSize.setObjectName("spinSize")
        self.lbSize = QtWidgets.QLabel(self.centralwidget)
        self.lbSize.setGeometry(QtCore.QRect(270, 150, 81, 21))
        self.lbSize.setObjectName("lbSize")
        self.lbStatus = QtWidgets.QLabel(self.centralwidget)
        self.lbStatus.setGeometry(QtCore.QRect(16, 190, 271, 41))
        self.lbStatus.setObjectName("lbStatus")
        self.lbFrameView = QtWidgets.QLabel(self.centralwidget)
        self.lbFrameView.setGeometry(QtCore.QRect(20, 280, 581, 400))
        self.lbFrameView.setObjectName("lbFrameView")
        self.labelInfoEye = QtWidgets.QLabel(self.centralwidget)
        self.labelInfoEye.setGeometry(QtCore.QRect(10, 240, 151, 31))
        self.labelInfoEye.setObjectName("labelInfoEye")
        self.labelInfoEye.setStyleSheet("QLabel {color : red; }")
        self.labelInfoMouth = QtWidgets.QLabel(self.centralwidget)
        self.labelInfoMouth.setGeometry(QtCore.QRect(180, 240, 151, 31))
        self.labelInfoMouth.setObjectName("labelInfoMouth")
        self.labelInfoMouth.setStyleSheet("QLabel {color : blue; }")
        self.lbWarn = QtWidgets.QLabel(self.centralwidget)
        self.lbWarn.setGeometry(QtCore.QRect(360, 240, 241, 31))
        self.lbWarn.setObjectName("lbWarn")
        self.checkDropbox = QtWidgets.QCheckBox(self.centralwidget)
        self.checkDropbox.setGeometry(QtCore.QRect(20, 130, 171, 21))
        self.checkDropbox.setLayoutDirection(QtCore.Qt.RightToLeft)
        self.checkDropbox.setObjectName("checkDropbox")
        self.checkAI = QtWidgets.QCheckBox(self.centralwidget)
        self.checkAI.setGeometry(QtCore.QRect(20, 100, 171, 21))
        self.checkAI.setLayoutDirection(QtCore.Qt.RightToLeft)
        self.checkAI.setObjectName("checkAI")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 605, 22))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        ########### init ###########
        self.spinSize.setEnabled(False)
        self.lbSize.setEnabled(False)
        self.lbEyeNum.setText(settings.value('lbEyeNum'))
        self.lbMouthNum.setText(settings.value('lbMouthNum'))

        ########### custom event listiener ###########
        # self.comboSource.addItems([str(cameraindex.index('HD'))])

        self.slideEye.valueChanged.connect(self.slideChange)
        self.slideMouth.valueChanged.connect(self.slideChange)

        self.progressBar.setTextVisible(True)

        self.btnStart.clicked.connect(self.onClick)

        self.checkShow.stateChanged.connect(self.showChange)

        self.spinSize.valueChanged.connect(self.sizeChange)

    def sizeChange(self):
        settings.setValue('spinSize', self.spinSize.value())

    def showChange(self):
        if (self.checkShow.isChecked()):
            self.spinSize.setEnabled(True)
            self.lbSize.setEnabled(True)
        else:
            self.spinSize.setEnabled(False)
            self.lbSize.setEnabled(False)

    def slideChange(self):
        eyeVal = self.slideEye.value()
        mouthVal = self.slideMouth.value()

        self.lbEyeNum.setText(str(eyeVal))
        self.lbMouthNum.setText(str(mouthVal))
        settings.setValue('lbEyeNum', eyeVal)
        settings.setValue('lbMouthNum', mouthVal)

    def onClick(self):
        def progressValue(stt, current, total=9):
            self.lbStatus.setText(stt)
            self.progressBar.setValue((current/total)*100)

        def sound_alarm():
            # winsound.PlaySound('alarm.wav',winsound.SND_FILENAME)
            # playsound.playsound('alarm.wav')
            subprocess.call(['afplay', 'alarm.wav'])
            # pass

        def sound_focus():
            # winsound.PlaySound('focus.wav',winsound.SND_FILENAME)
            # playsound.playsound('focus.wav')
            subprocess.call(['afplay', 'focus.wav'])
            # pass

        def euclidean_dist(ptA, ptB):
            return np.linalg.norm(ptA - ptB)

        def eye_aspect_ratio(eye):
            return (euclidean_dist(eye[1], eye[5]) + euclidean_dist(eye[2], eye[4])) / (2.0 * euclidean_dist(eye[0], eye[3]))

        def mouth_ratio(mouth):
            return (euclidean_dist(mouth[13], mouth[19])+euclidean_dist(mouth[14], mouth[18])+euclidean_dist(mouth[15], mouth[17]))/(3.0*euclidean_dist(mouth[12], mouth[16]))

        progressValue('Initial Constant Values', 1)

        FOCUS_CONTINOUS_FRAMES = 40

        checkDrop = self.checkDropbox.isChecked()
        EYE_COUNTER = MOUTH_COUNTER = FOCUS_COUNTER = 0
        ratio = []
        avr_eyes = 0.25
        lastUploaded = datetime.datetime.now()
        MOUTH_ALARM_ON = EYE_ALARM_ON = FOCUS_ALARM_ON = EYE_RECORD = MOUTH_RECORD = check_eyes = False
        # FOCUS = True
        STATE = None
        FOCUS = check = True
        fourcc = cv2.VideoWriter_fourcc(*'XVID')
        cv2.namedWindow('frame')

        progressValue('Loading face detector', 2)
        # detector = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
        detector = dlib.get_frontal_face_detector()
        progressValue('Loading facial landmark predictor', 3)
        predictor = dlib.shape_predictor(
            'shape_predictor_68_face_landmarks.dat')

        progressValue('Loading facial coordinates', 4)
        (lStart, lEnd) = face_utils.FACIAL_LANDMARKS_IDXS["left_eye"]
        (rStart, rEnd) = face_utils.FACIAL_LANDMARKS_IDXS["right_eye"]
        (mouthStart, mouthEnd) = face_utils.FACIAL_LANDMARKS_IDXS['mouth']

        progressValue('Starting video stream thread', 5)
        vs = VideoStream(0).start()
        progressValue('Sleep in 1 second', 6)
        time.sleep(1.0)

        progressValue('Linking Dropbox API', 7)
        client = dropbox.Dropbox(
            "unQ5Wyy9mgAAAAAAAAAA1sEqh8yICaR7r0e3F9LL_kXTFYhHoO0cJ3sarfiv8gxx")

        progressValue('FPS sclaler', 8)
        fps = FPS().start()

        progressValue('Done', 9)
        # eyeOUTPUT = 0

        while True:
            frame = vs.read()

            timestamp = datetime.datetime.now()
            ts = timestamp.strftime("%A %d %B %Y %I:%M:%S%p")
            frame = imutils.resize(frame, self.spinSize.value())
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

            if STATE is 1:
                FOCUS_COUNTER += 1
                check_eyes = False
                if (FOCUS_COUNTER == FOCUS_CONTINOUS_FRAMES):
                    FOCUS_COUNTER = 0
                    FOCUS = False
                    tt = Thread(target=sound_focus)
                    tt.setDaemon(True)
                    tt.start()
                    cv2.putText(frame, 'TAP TRUNG', (20, 30),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (50, 255, 100), 2)
                # if not FOCUS:
                #     cv2.putText(frame, 'TAP TRUNG', (20, 30),
                #                 cv2.FONT_HERSHEY_SIMPLEX, 0.7, (50, 255, 100), 2)
            else:
                check_eyes = True
            STATE = 1
            rects = detector(gray, 0)
            # print('check',check_eyes)
            for rect in rects:
                shape = face_utils.shape_to_np(predictor(gray, rect))

                STATE = type(shape)
                if STATE is np.ndarray:
                    # FOCUS = True
                    FOCUS_ALARM_ON = False
                    FOCUS_COUNTER = 0

                leftEye = shape[lStart:lEnd]
                rightEye = shape[rStart:rEnd]
                for item in (leftEye):
                    cv2.circle(frame, tuple(item), 1, (0, 0, 255), -1)
                for item in (rightEye):
                    cv2.circle(frame, tuple(item), 1, (0, 0, 255), -1)
                avr_eyes = (eye_aspect_ratio(leftEye) +
                            eye_aspect_ratio(rightEye)) / 2.0

                self.labelInfoEye.setText(
                    'Eyes Ratio: {:.2f}'.format(avr_eyes))

                if avr_eyes < self.spinEye.value():
                    EYE_COUNTER += 1

                    if EYE_COUNTER >= self.slideEye.value():
                        if not EYE_ALARM_ON:
                            EYE_ALARM_ON = True
                            t = Thread(target=sound_alarm)
                            t.setDaemon(True)
                            t.start()
                        cv2.putText(frame, 'NGU GAT !', (20, 30),
                                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (50, 255, 100), 2)

                    if (checkDrop and not EYE_RECORD):
                        EYE_RECORD = True
                        # init path
                        tt = TempImage('./videos')
                        # create new blank video file
                        eyeOUTPUT = cv2.VideoWriter(
                            tt.path, fourcc, 20.0, (frame.shape[1], frame.shape[0]))
                    # start recording each frame
                    if (checkDrop):
                        eyeOUTPUT.write(frame)

                # chỉ render khi frame trước đó vừa hụ còi >> tránh render chồng chất nhiều frame
                elif (checkDrop and EYE_ALARM_ON):
                    EYE_ALARM_ON = False
                    EYE_COUNTER = 0
                    EYE_RECORD = False
                    eyeOUTPUT.release()
                    # upload lên dropbox
                    if (timestamp - lastUploaded).seconds >= 10:
                        try:
                            path = "/{base_path}/{timestamp}.avi".format(
                                base_path="Drowsiness", timestamp=ts)
                            client.files_upload(
                                open(tt.path, "rb").read(), path)
                            tt.cleanup()
                            # print('[UPLOAD thanh cong]')
                            self.lbWarn.setText('[dropbox] tải lên hoàn tất')
                            lastUploaded = timestamp
                        except:
                            # print('[UPLOAD that bai] Kiem tra ket noi internet')
                            self.lbWarn.setText(
                                '[dropbox] kiểm tra kết nối internet')

                else:
                    EYE_ALARM_ON = False
                    EYE_COUNTER = 0

                mouth = shape[mouthStart:mouthEnd]
                for item in (mouth):
                    cv2.circle(frame, tuple(item), 2, (255, 0, 0), -1)
                avr_mouth = mouth_ratio(mouth)
                self.labelInfoMouth.setText(
                    'Mouth Ratio: {:.2f}'.format(avr_mouth))

                if avr_mouth > self.spinMouth.value():
                    MOUTH_COUNTER += 1

                    if MOUTH_COUNTER >= self.slideMouth.value():
                        if not MOUTH_ALARM_ON:
                            MOUTH_ALARM_ON = True
                            t = Thread(target=sound_alarm)
                            t.setDaemon(True)
                            t.start()
                        cv2.putText(frame, 'NGAP !', (20, 30),
                                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (50, 255, 100), 2)

                    if (checkDrop and not MOUTH_RECORD):
                        MOUTH_RECORD = True
                        tt = TempImage('./videos')
                        mouthOUTPUT = cv2.VideoWriter(
                            tt.path, fourcc, 20.0, (frame.shape[1], frame.shape[0]))
                    # start recording each frame
                    if (checkDrop):
                        mouthOUTPUT.write(frame)

                elif (checkDrop and MOUTH_ALARM_ON):
                    MOUTH_ALARM_ON = False
                    MOUTH_COUNTER = 0
                    # rendering video
                    MOUTH_RECORD = False
                    mouthOUTPUT.release()
                    if (timestamp - lastUploaded).seconds >= 10:
                        try:
                            path = "/{base_path}/{timestamp}.avi".format(
                                base_path="Drowsiness", timestamp=ts)
                            client.files_upload(
                                open(tt.path, "rb").read(), path)
                            tt.cleanup()
                            # print("[UPLOAD thanh cong]")
                            self.lbWarn.setText('[dropbox] tải lên hoàn tất')
                            lastUploaded = timestamp
                        except:
                            # print('[UPLOAD that bai] Kiem tra ket noi internet')
                            self.lbWarn.setText(
                                '[dropbox] kiểm tra kết nối internet')
                else:
                    MOUTH_ALARM_ON = False
                    MOUTH_COUNTER = 0

            self.lbWarn.setText(str(len(ratio)))
            #print('check2 ',check_eyes)
            if (self.checkAI.isChecked()):
                if check_eyes == True:
                    # print('adding')
                    ratio.append(avr_eyes)
                    frameRGB = cv2.circle(
                        frame, (270, 200), 120, (0, 160, 0), 8)
                    cv2.putText(frame, 'Adding !', (20, 40),
                                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
                    cv2.putText(frame, 'Complete: {:.1f}% '.format(
                        (len(ratio))/2.5), (280, 40), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)
                    self.lbFrameView.setPixmap(QtGui.QPixmap.fromImage(QtGui.QImage(
                        frameRGB.data, frameRGB.shape[1], frameRGB.shape[0], frameRGB.shape[1]*3, QtGui.QImage.Format_RGB888)))
                    if (len(ratio) == 250):
                        a = np.average(ratio)
                        self.spinEye.setValue(a)
                        settings.setValue('spinEye', a)
                        self.checkAI.setChecked(False)
                        ratio = []

            if(self.checkShow.isChecked()):
                frameRGB = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                self.lbFrameView.setPixmap(QtGui.QPixmap.fromImage(QtGui.QImage(
                    frameRGB.data, frameRGB.shape[1], frameRGB.shape[0], frameRGB.shape[1]*3, QtGui.QImage.Format_RGB888)))

            if cv2.waitKey(1) == 27:
                break

            fps.update()

        fps.stop()
        print('[INFO] Avr. FPS: {:.2f}'.format(fps.fps()))
        vs.stop()
        cv2.destroyAllWindows()

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "🛣️ Drowsiness 🛵"))
        # self.lbPort.setText(_translate("MainWindow", "Port ⚡"))
        self.btnStart.setText(_translate("MainWindow", "Start"))
        self.lbEyeThread.setText(_translate("MainWindow", "Eyes Threadhold"))
        self.lbMouthThread.setText(_translate(
            "MainWindow", "Mouth Threadhold"))
        self.lbEyeFrame.setText(_translate("MainWindow", "Eyes Frame 🤩"))
        self.lbMouthFrame.setText(_translate("MainWindow", "Mouth Frame 👄"))
        self.lbCam.setText(_translate("MainWindow", "Source 📷"))
        self.checkShow.setText(_translate("MainWindow", "Show Frames"))
        self.lbEyeNum.setText(_translate("MainWindow", "TextLabel"))
        self.lbMouthNum.setText(_translate("MainWindow", "TextLabel"))
        self.lbSize.setText(_translate("MainWindow", "Frame Size"))
        self.checkDropbox.setText(_translate("MainWindow", "Dropbox"))
        self.checkAI.setText(_translate("MainWindow", "AI"))


if __name__ == "__main__":
    import sys
    settings = QtCore.QSettings('./setting.ini', QtCore.QSettings.IniFormat)
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
