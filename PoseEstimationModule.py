# cv2 = opencv-python package, mediapipe = mediapipe package both added to the project
import cv2
import mediapipe as mp
import time
import math
# Edited library component:
# D:\GitHub\RoboticsLabProject\RoboticsLab\venv\Lib\site-packages\mediapipe\python\solutions\drawing_utils.py
# commented error ValueError(f'Landmark index is out of range. Invalid connection 'f'from landmark #{start_idx} to landmark #{end_idx}.')
# at line 161


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
        # self.pose = self.mpPose.Pose(self.mode, self.smooth, self.detectionCon, self.trackCon)
        # self.pose = self.mpPose.Pose(self.mode, self.smooth, self.detectionCon, self.trackCon,min_detection_confidence,min_tracking_confidence)
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





# def main():
#     cap = cv2.VideoCapture('PexelsVideos/dancing.mp4')  # dancing video
#     cap = cv2.VideoCapture('PexelsVideos/walking.mp4') # walking video
#     cap = cv2.VideoCapture('PexelsVideos/lecture.mp4') # lecture video
#     cap = cv2.VideoCapture(0) # Camputer Camera
#     pTime = 0
#     img = detector = poseDetector()
#
#     while True:
#
#         success, img = cap.read()
#         detector.findPose(img)
#         # detector.findPosition(img)
#         lmList = detector.findPosition(img, draw=False)
#         if len(lmList) != 0:
#             print(lmList[14])
#             cv2.circle(img, (lmList[14][1], lmList[14][2]), 3, (0, 0, 255), cv2.FILLED)
#
#
#         cTime = time.time()
#         fps = 1 / (cTime - pTime)
#         pTime = cTime
#
#         cv2.putText(img, str(int(fps)), (70, 50), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 0), 3)
#
#
#         cv2.imshow("Image", img)
#         cv2.waitKey(1)
#
#
# if __name__ == "__main__":
#     main()