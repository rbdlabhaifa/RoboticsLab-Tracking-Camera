import cv2
import mediapipe as mp
import time
import os
import HandTrackingModule as htm
import math

##########
wCam, hCam = 640, 480
pTime = 0
sumOfFingers = 0
##########

cap = cv2.VideoCapture(0)
cap.set(3, wCam)
cap.set(4, hCam)

folderPath = './FingerImg'  # "FingerImg"
myList = os.listdir(folderPath)
# print(myList)
overlayList = []
for imPath in myList:
    image = cv2.imread(f'{folderPath}/{imPath}')
    # print(image)
    overlayList.append(image)

detector = htm.handDetector(detectionCon=.7)

tipIds = [8, 12, 16, 20]


while True:
    success, img = cap.read()
    img = detector.findHands(img)
    lmList = detector.findPosition(img, draw=False)

    if len(lmList) != 0:
        fingers = []
        # solving the thumb unique properties by degrees between the joints
        x1, y1 = lmList[4][1], lmList[4][2]     # thumb tip
        x2, y2 = lmList[3][1], lmList[3][2]     # thumb mid
        x3, y3 = lmList[2][1], lmList[2][2]     # thumb bottom
        v1 = [(x2-x1), (y2-y1)]
        v2 = [(x3-x2), (y3-y2)]
        ang = math.degrees(math.atan2(v1[0], v1[1]) - math.atan2(v2[0], v2[1]))
        # print(ang)

        if(abs(ang)<26):
            fingers.append(1)
        else:
            fingers.append(0)

        for id in range(0, 4):

            if lmList[tipIds[id]][2] < lmList[tipIds[id]-2][2]:
                fingers.append(1)
            else:
                fingers.append(0)

        sumOfFingers = fingers.count(1)
        print(sumOfFingers)

    h, w, c = overlayList[sumOfFingers].shape
    img[0:h, 0:w] = overlayList[sumOfFingers] # location of the overlaying image in the window

    cTime = time.time()
    fps = 1/(cTime - pTime)
    pTime = cTime

    cv2.putText(img, str(int(fps)), (10, 460), cv2.FONT_HERSHEY_PLAIN, 2, (255, 0, 150), 2)
    cv2.imshow("Image", img)
    cv2.waitKey(1)

