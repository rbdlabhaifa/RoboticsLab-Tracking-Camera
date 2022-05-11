import cv2
import time
import PoseEstimationModule as pem
import numpy as np


# cap = cv2.VideoCapture('Data_Set/PexelsVideos/dancing.mp4')  # dancing video
# cap = cv2.VideoCapture(r'Data_Set\PexelsVideos\walking.mp4') # walking video
# cap = cv2.VideoCapture(0) # Camputer Camera
# cap = cv2.VideoCapture(r'Data_Set/PexelsVideos/dancing_couple.mp4') # lecture video
# cap = cv2.VideoCapture(r'Data_Set/PedestriansPics/alone.jpg') # walking video
# cap = cv2.VideoCapture(r'Data_Set/PedestriansPics/hide2.jpg') # walking video
# cap = cv2.VideoCapture(r'Data_Set/PedestriansPics/multiple.jpg') # walking video
# cap = cv2.VideoCapture(r'Data_Set/PexelsVideos/lecture.mp4') # lecture video
# cap = cv2.VideoCapture(r'Data_Set/PexelsVideos/two_apart.mp4') # two people sitting apart video
cap = cv2.VideoCapture(r'Data_Set/PexelsVideos/stand_apart.mp4') # two people standing apart video
# cap = cv2.VideoCapture('Data_Set/@Y_dataset/@Y_braking_shape.mpg') # walking video


# creating zero frame
shape = ((int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)),int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)),3))
print(shape)
frame1 = np.zeros(shape)
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

    return move

pTime = 0
adj = 0
detector = pem.poseDetector()

while True:
    success, img = cap.read()
    adj=adj+1
    scalep = 80
    # img = rescale_frame(img, percent=scalep) # Uncomment in order to take place, the percentage is for relative scaling
    # frame = rescale_frame(frame, percent=scalep) # Uncomment in order to take place, the percentage is for relative scaling

    # img = cv2.imread('C:\Code\GitHub\RoboticsLab\PedestriansPics\\alone.jpg')
    # # img=cv2.flip(img,1)
    # cv2.namedWindow('ObjectDetection_Checker', cv2.WINDOW_NORMAL)
    # cv2.resizeWindow('ObjectDetection_Checker', 1280, 720)

    # cv2.imshow('Image', img)

    height, width , c = img.shape
    print(adj)

    detector.findPose(img, True)
    lmList = detector.findPosition(img, draw = False)
    if len(lmList)!=0:
        rSholder = lmList[12][1],lmList[12][2]
        lSholder = lmList[11][1],lmList[11][2]
        rHip = lmList[24][1],lmList[24][2]
        lHip = lmList[23][1],lmList[23][2]
        xMax = max(rSholder[0], lSholder[0], rHip[0], lHip[0])+20
        xMin = min(rSholder[0], lSholder[0], rHip[0], lHip[0])-20
        yMax = max(rSholder[1], lSholder[1], rHip[1], lHip[1])+20
        yMin = min(rSholder[1], lSholder[1], rHip[1], lHip[1])-20
        w,h = (xMax-xMin), (yMax-yMin)
        maxLength=max(h,w)
        midPoint=(xMin+w/2, yMin+h/2) # mid point of the bbox of the character
        moveTo=hotZones(img, height, width, maxLength, midPoint)
        # cv2.rectangle(img, (x+30, y+30), (x1-30,y1-30), (139, 34, 104), 2)
        cv2.rectangle(img, (xMax, yMax), (xMin,yMin), (139, 34, 104), 2)

        rEye = lmList[5][1],lmList[5][2]
        lEye = lmList[2][1],lmList[2][2]
        rFoot = lmList[32][1],lmList[32][2]
        lFoot = lmList[31][1],lmList[31][2]
        xMaxf = max(rEye[0], lEye[0], rFoot[0], lFoot[0])+30
        xMinf = min(rEye[0], lEye[0], rFoot[0], lFoot[0])-30
        yMaxf = max(rEye[1], lEye[1], rFoot[1], lFoot[1])+30
        yMinf = min(rEye[1], lEye[1], rFoot[1], lFoot[1])-30

        # inserting crop image into zero frame
        # frame1 = np.zeros(shape)
        # crop = img[xMin:xMax, yMin:yMax,:]
        # crop = np.array(crop)
        # offset = np.array((xMin, yMin,0))
        # frame1[offset[0]:offset[0] + crop.shape[0], offset[1]:offset[1] + crop.shape[1],offset[2]:offset[2] + crop.shape[2]] = crop



    cTime = time.time()
    fps = 1/(cTime-pTime)
    pTime = cTime

    cv2.putText(img, str(int(fps)), (70, 50), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 0), 3)
    if adj < 50 or len(lmList)==0:
        cv2.imshow("Image", img)
    else:
        if(adj==100):
            cv2.destroyAllWindows()
        frame1 = np.zeros(shape)
        frame1[yMinf:yMaxf,xMinf:xMaxf,:] = img[yMinf:yMaxf,xMinf:xMaxf,:]
        cv2.imshow("Frame1", img)
    # cv2.imshow("test", background)
    cv2.waitKey(1)
    # cv2.waitKey(6000)
if __name__ == "__main__":
    main()