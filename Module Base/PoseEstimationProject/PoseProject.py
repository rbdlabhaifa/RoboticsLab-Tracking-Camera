import cv2
import time
import PoseEstimationModule as pem


# cap = cv2.VideoCapture('PexelsVideos/dancing.mp4')  # dancing video
cap = cv2.VideoCapture(r'D:\GitHub\RoboticsLabProject\RoboticsLab\Module Base\PoseEstimationProject\PexelsVideos\walking.mp4') # walking video
# cap = cv2.VideoCapture(0) # Camputer Camera
# cap = cv2.VideoCapture('Module Base/PoseEstimationProject/PexelsVideos/lecture.mp4') # lecture video
# cap = cv2.VideoCapture('PedestriansPics/alone.jpg') # walking video
# cap = cv2.VideoCapture('PedestriansPics/hide1.jpg') # walking video
# cap = cv2.VideoCapture('PedestriansPics/multiple.jpg') # walking video


pTime = 0
img = detector = pem.poseDetector()

while True:
    success, img = cap.read()
    detector.findPose(img)
    lmList = detector.findPosition(img, draw = False)
    if len(lmList)!=0:
        print(lmList[12]) # right shoulder
        # print(lmList[11]) # left shoulder
        # print(lmList[24]) # right hip
        print(lmList[23]) # left hip
        x1,y1,x4,y4 = lmList[12][1],lmList[12][2],lmList[23][1],lmList[23][2]
        x,y = x4,y4
        w,h = abs(x1-x4),abs(y1-y4)
        cv2.rectangle(img, (x+30, y+30), (x1-30,y1-30), (139, 34, 104), 2)
        # cv2.circle(img, (lmList[14][1], lmList[14][2]), 5, (255, 0, 150), cv2.FILLED)

    cTime = time.time()
    fps = 1/(cTime-pTime)
    pTime = cTime

    cv2.putText(img, str(int(fps)), (70, 50), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 0), 3)

    cv2.imshow("Image", img)
    cv2.waitKey(1)


if __name__ == "__main__":
    main()