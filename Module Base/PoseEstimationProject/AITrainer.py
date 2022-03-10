import cv2
import mediapipe as mp
import numpy as np
import time
import PoseEstimationModule as pem

from cv2 import waitKey

#######################
count = 0
dir = 0
#######################
cap = cv2.VideoCapture('./PexelsVideos/lift.mp4')  # video
img = cv2.imread('./PexelsVideos/lift.mp4')
detector = pem.poseDetector()
pTime = 0

while True:
    success, img = cap.read()
    detector.findPose(img, False)
    lmList = detector.findPosition(img, draw=False)
    # print(lmList)
    if len(lmList) != 0:
        # Right arm
        angR = detector.findAngle(img, 12, 14, 16)
        perR = np.interp(angR, (30, 195), (100, 0))

        # Left arm
        angL = detector.findAngle(img, 11, 13, 15)
        perL = np.interp(angL, (10, 175), (100, 0))

        if perL == 100 and perR == 100:
            if dir == 0:
                count += 1
                dir = 1
        if perL == 0 and perR == 0:
            if dir == 1:
                dir = 0

        h, w, c = img.shape
        cv2.rectangle(img, (w-150,0 ), (w, 150), (200, 100, 0), 3)
        cv2.putText(img, str(count), (w-100, 100), cv2.FONT_HERSHEY_PLAIN, 5, (255, 0, 100), 5)

    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime

    cv2.putText(img, str(int(fps)), (20, 50), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 0), 3)

    cv2.imshow("Image", img)
    cv2.waitKey(1)
