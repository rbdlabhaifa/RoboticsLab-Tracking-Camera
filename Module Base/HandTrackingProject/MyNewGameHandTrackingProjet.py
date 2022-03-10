import cv2
import mediapipe as mp
import time
import HandTrackingModule as htm


pTime = 0  # previous timestamp
cTime = 0  # current timestamp
# VideoCapture(input) input = 0 and not 1 as it apears on the guide
# import pTime as pTime
cap = cv2.VideoCapture(0)
detector = htm.handDetector()

while True:
    success, img = cap.read()
    img = detector.findHands(img, draw = True) # False for not drawing
    lmList = detector.findPosition(img, draw = True) # False for not drawing
    if len(lmList) != 0:
        print(lmList[4])

    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime

    cv2.putText(img, str(int(fps)), (10, 70), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 255), 3)

    cv2.imshow("Image", img)
    cv2.waitKey(1)
