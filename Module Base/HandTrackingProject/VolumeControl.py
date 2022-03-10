# cv2 = opencv-python package, mediapipe = mediapipe package both added to the project
import cv2
import mediapipe as mp
import time

import numpy as np

import HandTrackingModule as htm
import math
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

#############################
wCam, hCam = 1280, 720
vol = 0
volb = 400
volp = 0
#############################

cap = cv2.VideoCapture(0)
cap.set(3, wCam)
cap.set(4, hCam)
# mpHands = mp.solutions.hands
# hands = mpHands.Hands()     # LCtrl & click on Hands() func to see the implementation
# mpDraw = mp.solutions.drawing_utils
pTime = 0   # previous timestamp
detector = htm.handDetector(detectionCon=.7)


devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(
    IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))
# volume.GetMute()
# volume.GetMasterVolumeLevel()
volRange = volume.GetVolumeRange()

minVol = volRange[0]
maxVol = volRange[1]



while True:
    success, img = cap.read()
    img = detector.findHands(img)
    lmList = detector.findPosition(img, draw=False)
    if len(lmList)!=0:
        # print(lmList[4], lmList[8])

        x1, y1 = lmList[4][1], lmList[4][2]
        x2, y2 = lmList[8][1], lmList[8][2]
        cx, cy = (x1+x2)//2, (y1+y2)//2

        cv2.circle(img, (x1, y1), 15, (255,0,150), cv2.FILLED)
        cv2.circle(img, (x2, y2), 15, (255,0,150), cv2.FILLED)
        cv2.line(img, (x1, y1), (x2, y2), (255, 0, 150), 3)
        cv2.circle(img, (cx, cy), 10, (255, 0, 150), cv2.FILLED)

        length = math.hypot(x2-x1, y2-y1)
        # print(length)
        # Finger range is [50,300]
        # Volume range is [-64,0]
        vol = np.interp(length,[50,300],[minVol,maxVol])
        volb = np.interp(length, [50, 300], [400, 150])
        volp = np.interp(length, [50, 300], [0, 100])
        print(vol)
        volume.SetMasterVolumeLevel(vol, None)

        if length <50:
            cv2.circle(img, (cx, cy), 10, (0, 255, 0), 3, cv2.FILLED)

    cv2.rectangle(img, (50, 150),(85,400),(255,0,150),3)
    cv2.rectangle(img, (50, int(volb)), (85,400), (255, 0, 150), cv2.FILLED)
    cTime = time.time()
    fps = 1/(cTime-pTime)
    pTime = cTime
    cv2.putText(img, f'{int(volp)}%', (40, 130), cv2.FONT_HERSHEY_PLAIN, 2, (255, 0, 150), 2)
    cv2.putText(img, str(int(fps)), (10, 30), cv2.FONT_HERSHEY_PLAIN, 2, (255, 0, 150), 2)

    cv2.imshow("Image", img)
    cv2.waitKey(1)