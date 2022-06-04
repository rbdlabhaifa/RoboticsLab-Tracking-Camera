# cv2 = opencv-python package, mediapipe = mediapipe package both added to the project
import cv2
import mediapipe as mp
import time
import math

class poseDetector():

    def __init__(self, mode=False, complex=1, smooth=True, detectionCon=0.5, trackCon=0.5, min_detection_confidence=0.5,
    min_tracking_confidence=0.5):

        self.mode = mode
        self.complex = complex
        self.smooth = smooth
        self.detectionCon = detectionCon
        self.trackCon = trackCon

        self.mpDraw = mp.solutions.drawing_utils
        self.mpPose = mp.solutions.pose
        self.pose = self.mpPose.Pose()

    def findPose(self, img, draw=True):

        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results = self.pose.process(imgRGB)

        if self.results.pose_landmarks:
            if draw:# false insteed of draw for new way
                self.mpDraw.draw_landmarks(img, self.results.pose_landmarks, self.mpPose.POSE_CONNECTIONS)
        return img

    def findPosition(self, img, draw=True):
        self.lmList = []
        if self.results.pose_landmarks:
            for id, lm in enumerate(self.results.pose_landmarks.landmark):
                h, w, c = img.shape
                cx, cy = int(lm.x * w), int(lm.y * h)
                self.lmList.append([id, cx, cy])
                if draw:
                    cv2.circle(img, (cx, cy), 7, (255, 0, 150), cv2.FILLED)

        return self.lmList


