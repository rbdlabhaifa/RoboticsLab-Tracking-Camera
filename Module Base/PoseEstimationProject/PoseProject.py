from sys import argv
import cv2
import time
import PoseEstimationModule as pem
import Tello
import numpy as np
from datetime import datetime



# rescaling frame function for oversized frames - if needed
def rescale_frame(frame, percent=75):
    width = int(frame.shape[1] * percent / 100)
    height = int(frame.shape[0] * percent / 100)
    dim = (width, height)
    return cv2.resize(frame, dim, interpolation=cv2.INTER_AREA)




def hotZones(frame, height, width, maxLength, midPoint, drawLineFlag):
    ''':param frame- the frame img , height - the height of the frame, width - the width of the frame,
     maxLength- the max val of the object bbox length, midPoint- the mid point of the object
     :return move- the number of pixels that the camera mast move to keep the object in the frame

    compute the number of pixels to go move the camera to keep the object in the frame
    '''
    move = 0
    ratio = maxLength / width
    leftBorder = width * ratio
    moveToLeftBorder = leftBorder + maxLength
    rightBorder = width * (1 - ratio)
    moveToRightBorder = rightBorder - maxLength
    # print(leftBorder, rightBorder)

    if moveToRightBorder <= moveToLeftBorder:
        moveToLeftBorder = width / 2
        moveToRightBorder = width / 2

    if midPoint[0] < leftBorder:
        move = moveToLeftBorder - midPoint[0]
        if (drawLineFlag == True):
            cv2.arrowedLine(img=frame, pt1=(int(midPoint[0]), int(midPoint[1])),
                        pt2=(int(moveToLeftBorder), int(midPoint[1])), color=(0, 255, 0), thickness=5)
    elif midPoint[0] > rightBorder:
        move = moveToRightBorder - midPoint[0]
        if (drawLineFlag == True):
            cv2.arrowedLine(img=frame, pt1=(int(midPoint[0]), int(midPoint[1])),
                        pt2=(int(moveToRightBorder), int(midPoint[1])), color=(0, 255, 0), thickness=5)

    if(drawLineFlag==True):
        # draw zones
        cv2.line(img=frame, pt1=(int(leftBorder), 0), pt2=(int(leftBorder), height), color=(0, 0, 255), thickness=5,
                 lineType=8, shift=0)
        cv2.line(img=frame, pt1=(int(rightBorder), 0), pt2=(int(rightBorder), height), color=(0, 0, 255), thickness=5,
                 lineType=8, shift=0)

        # draw lines to go to
        cv2.line(img=frame, pt1=(int(moveToLeftBorder), 0), pt2=(int(moveToLeftBorder), height), color=(0, 255, 255),
                 thickness=5, lineType=8, shift=0)
        cv2.line(img=frame, pt1=(int(moveToRightBorder), 0), pt2=(int(moveToRightBorder), height), color=(0, 255, 255),
                 thickness=5, lineType=8, shift=0)

    return move

def movmentControler (movmentFlag):
    if movmentFlag ==0:
        return
    elif movmentFlag<0:
        Tello.move_left()
    elif movmentFlag>0:
        Tello.move_right()

def mainPoseDetection(cap, drawLineFlag):
    # shape = ((int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)), int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)), 3))
    # # print(shape)

    pTime = 0
    adj = 0
    detector = pem.poseDetector()
    recordFlag=False

    while cv2.waitKey(1) != 27: #esc
        keyPrass = cv2.waitKey(1) & 0xFF
        if  keyPrass == ord('r') or keyPrass == ord('R') and recordFlag==False:
            frame_width = int(cap.get(3))
            frame_height = int(cap.get(4))
            size = (frame_width, frame_height)
            name = datetime.now().strftime("%d.%m.%Y %H-%M-%S")
            result = cv2.VideoWriter(name + ".avi", cv2.VideoWriter_fourcc(*'MJPG'), 24.0, size)
            recordFlag=True

        success, img = cap.read()
        if not success or img is None:
            print("No Img")
            break

        crop_img = np.array(img) ########## For fully deployment uncomment this row and comment the row below
        # crop_img = img
        adj += 1
        scalep = 80
        crop_flag = False
        # img = rescale_frame(img, percent=scalep) # Uncomment in order to take place, the percentage is for relative scaling

        height, width, c = img.shape
        # print(adj)
        if adj > 51 and len(lmList) != 0:
            crop_flag = True
            crop_img[:yMinf, :, :] = 0
            crop_img[:, :xMinf, :] = 0
            crop_img[yMaxf:, :, :] = 0
            crop_img[:, xMaxf:, :] = 0

        detector.findPose(crop_img, drawLineFlag)
        lmList = detector.findPosition(crop_img, draw=False)
        if len(lmList) != 0:
            rSholder = lmList[12][1], lmList[12][2]
            lSholder = lmList[11][1], lmList[11][2]
            rHip = lmList[24][1], lmList[24][2]
            lHip = lmList[23][1], lmList[23][2]
            xMax = max(rSholder[0], lSholder[0], rHip[0], lHip[0])
            xMin = min(rSholder[0], lSholder[0], rHip[0], lHip[0])
            yMax = max(rSholder[1], lSholder[1], rHip[1], lHip[1])
            yMin = min(rSholder[1], lSholder[1], rHip[1], lHip[1])
            w, h = (xMax - xMin), (yMax - yMin)
            maxLength = max(h, w)
            midPoint = (xMin + w / 2, yMin + h / 2)  # mid point of the bbox of the character
            moveTo = hotZones(img, height, width, maxLength, midPoint, drawLineFlag)

            movmentControler(moveTo)

            if (drawLineFlag == True):
                cv2.rectangle(img, (xMax+round(maxLength*0.25), yMax+round(maxLength*0.25)), (xMin-round(maxLength*0.25), yMin-round(maxLength*0.25)), (139, 34, 104), 2)

        xMaxf = xMax + int(0.8 * w)
        xMinf = xMin - int(0.8 * w)
        yMaxf = yMax + int(0.8 * h)
        yMinf = yMin - int(0.8 * h)
        if (drawLineFlag == True): #show fps
            cTime = time.time()
            fps = 1 / (cTime - pTime)
            pTime = cTime
            cv2.putText(img, str(int(fps)), (70, 50), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 0), 3)

        if len(lmList) == 0:
            adj=30
        if adj > 50 and len(lmList) != 0:
            if not crop_flag:
                img[:yMinf, :, :] = 0
                img[:, :xMinf, :] = 0
                img[yMaxf:, :, :] = 0
                img[:, xMaxf:, :] = 0
        if recordFlag:
            result.write(img)
            img = cv2.circle(img, (25, 25), 10, (0,0,255), -1)
        cv2.imshow("Image", img)

        if   keyPrass == ord('s') or keyPrass == ord('S') and recordFlag==True  :
            result.release()
            recordFlag=False


    cap.release()
    if recordFlag:
        result.release()
        recordFlag=False
        print("stop recording")
    cv2.destroyAllWindows()



if __name__ == "__main__":
    input = argv[1] # path input for a video by defalt set to live captun
    drawLines = argv[2]  #draw test lines
    # cap = cv2.VideoCapture('Data_Set/PexelsVideos/dancing.mp4')  # dancing video
    # cap = cv2.VideoCapture(r'Data_Set\PexelsVideos\walking.mp4') # walking video
    # cap = cv2.VideoCapture(r'Data_Set/PexelsVideos/dancing_couple.mp4') # lecture video
    # cap = cv2.VideoCapture(r'Data_Set/PedestriansPics/alone.jpg') # walking video
    # cap = cv2.VideoCapture('Data_Set/PedestriansPics/hide2.jpg') # walking video
    # cap = cv2.VideoCapture(r'Data_Set/PedestriansPics/multiple.jpg') # walking video
    # cap = cv2.VideoCapture(r'Data_Set/PexelsVideos/lecture.mp4') # lecture video
    # cap = cv2.VideoCapture(r'Data_Set/PexelsVideos/two_apart.mp4') # two people sitting apart video
    # cap = cv2.VideoCapture('Data_Set/PexelsVideos/stand_apart.mp4')  # two people standing apart video
    # cap = cv2.VideoCapture('Data_Set/@Y_dataset/@Y_braking_shape.mpg') # walking video

    if input=='0':
        cap = cv2.VideoCapture(0) # Camputer Camera
    else:
        cap = cv2.VideoCapture(input) # walking video
    print(input)

    # rescaling resolution for better preformance
    cap.set(3, 640)
    cap.set(4, 480)

    if drawLines == "True":
        drawLineFlag=True
    elif drawLines == "False":
        drawLineFlag = False
    else:
        print("invalid flag input")



    mainPoseDetection(cap, drawLineFlag)

    print("all done!")