import cv2
import time
import PoseEstimationModule as pem


# cap = cv2.VideoCapture('Data_Set/PexelsVideos/dancing.mp4')  # dancing video
# cap = cv2.VideoCapture(r'Data_Set\PexelsVideos\walking.mp4') # walking video
# cap = cv2.VideoCapture(0) # Camputer Camera
# cap = cv2.VideoCapture(r'Data_Set/PexelsVideos/dancing_couple.mp4') # lecture video
# cap = cv2.VideoCapture(r'Data_Set/PedestriansPics/alone.jpg') # walking video
# cap = cv2.VideoCapture(r'Data_Set/PedestriansPics/hide2.jpg') # walking video
# cap = cv2.VideoCapture(r'Data_Set/PedestriansPics/multiple.jpg') # walking video
cap = cv2.VideoCapture(r'Data_Set/PexelsVideos/lecture.mp4') # lecture video
# cap = cv2.VideoCapture('Data_Set/@Y_dataset/@Y_HZ_levels.mpg') # walking video

# rescaling resolution for better preformance
cap.set(3, 640)
cap.set(4, 480)


# rescaling frame function for oversized frames - if needed
def rescale_frame(frame, percent=75):
    width = int(frame.shape[1] * percent/ 100)
    height = int(frame.shape[0] * percent/ 100)
    dim = (width, height)
    return cv2.resize(frame, dim, interpolation =cv2.INTER_AREA)

def hotZones(frame, height, width, maxLength, midPoint):
    ''':param frame- the frame img , height - the height of the frame, width - the width of the frame,
     maxLength- the max val of the object bbox length, midPoint- the mid point of the object
     :return move- the number of pixels that the camera mast move to keep the object in the frame

    compute the number of pixels to go move the camera to keep the object in the frame
    '''
    move=0
    ratio=maxLength/width
    leftBorder=width*ratio
    moveToLeftBorder=leftBorder+maxLength
    rightBorder = width * (1-ratio)
    moveToRightBorder=rightBorder-maxLength
    # print(leftBorder, rightBorder)

    if moveToRightBorder<=moveToLeftBorder:
        moveToLeftBorder=width/2
        moveToRightBorder=width/2

    if midPoint[0]<leftBorder:
        move=moveToLeftBorder-midPoint[0]
        cv2.arrowedLine(img=frame, pt1=(int(midPoint[0]),int(midPoint[1])), pt2=(int(moveToLeftBorder), int(midPoint[1])), color=(0, 255, 0), thickness=5)
    elif midPoint[0]>rightBorder:
        move=moveToRightBorder-midPoint[0]
        cv2.arrowedLine(img=frame, pt1=(int(midPoint[0]),int(midPoint[1])), pt2=(int(moveToRightBorder), int(midPoint[1])), color=(0, 255, 0), thickness=5)

    #draw zones
    cv2.line(img=frame, pt1=(int(leftBorder), 0), pt2=(int(leftBorder), height), color=(0, 0, 255), thickness=5, lineType=8, shift=0)
    cv2.line(img=frame, pt1=(int(rightBorder), 0), pt2=(int(rightBorder), height), color=(0, 0, 255), thickness=5, lineType=8, shift=0)

    # draw lines to go to
    cv2.line(img=frame, pt1=(int(moveToLeftBorder), 0), pt2=(int(moveToLeftBorder), height), color=(0, 255, 255), thickness=5, lineType=8, shift=0)
    cv2.line(img=frame, pt1=(int(moveToRightBorder), 0), pt2=(int(moveToRightBorder), height), color=(0, 255, 255), thickness=5, lineType=8, shift=0)

    print(move)
    return move

pTime = 0

img = detector = pem.poseDetector()

while True:
    success, img = cap.read()

    # img = rescale_frame(img, percent=60) # Uncomment in order to take place, the percentage is for relative scaling
    # img = cv2.imread('C:\Code\GitHub\RoboticsLab\PedestriansPics\\alone.jpg')
    # # img=cv2.flip(img,1)
    # cv2.namedWindow('ObjectDetection_Checker', cv2.WINDOW_NORMAL)
    # cv2.resizeWindow('ObjectDetection_Checker', 1280, 720)

    # cv2.imshow('Image', img)

    height, width , c = img.shape

    detector.findPose(img, True)
    lmList = detector.findPosition(img, draw = False)
    if len(lmList)!=0:
        # print(lmList[12]) # right shoulder
        # print(lmList[11]) # left shoulder
        # print(lmList[24]) # right hip
        # print(lmList[23]) # left hip
        # x1,y1,x4,y4 = lmList[12][1],lmList[12][2],lmList[23][1],lmList[23][2]
        rSholder = lmList[12][1],lmList[12][2]
        lSholder = lmList[11][1],lmList[11][2]
        rHip = lmList[24][1],lmList[24][2]
        lHip = lmList[23][1],lmList[23][2]
        xMax = max(rSholder[0], lSholder[0], rHip[0], lHip[0])
        xMin = min(rSholder[0], lSholder[0], rHip[0], lHip[0])
        yMax = max(rSholder[1], lSholder[1], rHip[1], lHip[1])
        yMin = min(rSholder[1], lSholder[1], rHip[1], lHip[1])
        w,h = (xMax-xMin), (yMax-yMin)
        maxLength=max(h,w)
        midPoint=(xMin+w/2, yMin+h/2) # mid point of the bbox of the character
        moveTo=hotZones(img, height, width, maxLength, midPoint)
        # x,y = x4,y4
        # w,h = abs(x1-x4),abs(y1-y4)
        # cv2.rectangle(img, (x+30, y+30), (x1-30,y1-30), (139, 34, 104), 2)
        cv2.rectangle(img, (xMax, yMax), (xMin,yMin), (139, 34, 104), 2)
        # cv2.circle(img, (lmList[14][1], lmList[14][2]), 5, (255, 0, 150), cv2.FILLED)

    cTime = time.time()
    fps = 1/(cTime-pTime)
    pTime = cTime

    cv2.putText(img, str(int(fps)), (70, 50), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 0), 3)

    cv2.imshow("Image", img)
    cv2.waitKey(1)
    # cv2.waitKey(6000)
if __name__ == "__main__":
    main()