import cv2
import mediapipe as mp
import time

# VideoCapture(input) input = 0 and not 1 as it apears on the guide
# import pTime as pTime

cap = cv2.VideoCapture(0)

mpHands = mp.solutions.hands
hands = mpHands.Hands()     # LCtrl & click on Hands() func to see the implementation
mpDraw = mp.solutions.drawing_utils
pTime = 0   # previous timestamp
cTime = 0   # current timestamp

while True:
    success, img = cap.read()
    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = hands.process(imgRGB)
    # print(results.multi_hand_landmarks) - this allow to see detection down the run box

    if results.multi_hand_landmarks:
        # LMS = landmarks
        for handLMS in results.multi_hand_landmarks:
            for id, lm in enumerate(handLMS.landmark):
                # print(id, lm)
                h, w, c = img.shape
                cx, cy = int(lm.x*w), int(lm.y*h)
                # print(id, cx, cy)
                if id == 0 or id == 4:     # 0 is the lm of the palm root as shown in purple bold circle
                    cv2.circle(img, (cx, cy), 15, (255, 0, 255), cv2.FILLED)


            mpDraw.draw_landmarks(img, handLMS, mpHands.HAND_CONNECTIONS)

    cTime = time.time()
    fps = 1/(cTime-pTime)
    pTime = cTime

    cv2.putText(img, str(int(fps)), (10, 70), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 255), 3)

    cv2.imshow("Image", img)
    cv2.waitKey(1)