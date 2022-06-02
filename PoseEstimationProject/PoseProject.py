from sys import argv
import cv2
import time
import PoseEstimationModule as pem
import numpy as np
from datetime import datetime
from djitellopy import Tello

# rescaling frame function for oversized frames - if needed
def rescale_frame(frame, percent=75):
    width = int(frame.shape[1] * percent / 100)
    height = int(frame.shape[0] * percent / 100)
    dim = (width, height)
    return cv2.resize(frame, dim, interpolation=cv2.INTER_AREA)


def hotZones(frame, height, width, maxLength, midPoint, drawLineFlag):
    """:param frame- the frame img , height - the height of the frame, width - the width of the frame,
     maxLength- the max val of the object bbox length, midPoint- the mid point of the object
     :return move- the number of pixels that the camera mast move to keep the object in the frame

    compute the number of pixels to go move the camera to keep the object in the frame
    """
    move = 0
    ratio = maxLength / width
    leftBorder = width * ratio
    moveToLeftBorder = leftBorder + maxLength
    rightBorder = width * (1 - ratio)
    moveToRightBorder = rightBorder - maxLength

    if moveToRightBorder <= moveToLeftBorder:
        moveToLeftBorder = width / 2
        moveToRightBorder = width / 2

    if midPoint[0] < leftBorder:
        move = moveToLeftBorder - midPoint[0]
        if drawLineFlag:
            cv2.arrowedLine(img=frame, pt1=(int(midPoint[0]), int(midPoint[1])),
                            pt2=(int(moveToLeftBorder), int(midPoint[1])), color=(0, 255, 0), thickness=5)
    elif midPoint[0] > rightBorder:
        move = moveToRightBorder - midPoint[0]
        if drawLineFlag:
            cv2.arrowedLine(img=frame, pt1=(int(midPoint[0]), int(midPoint[1])),
                            pt2=(int(moveToRightBorder), int(midPoint[1])), color=(0, 255, 0), thickness=5)

    if drawLineFlag:
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

    return move , [moveToLeftBorder,moveToRightBorder]


def movmentControler(isUp,movmentFlag, fps,h_ratio):
    yaw=0
    front=0
    if h_ratio > 0.4:
        front = -1
    elif h_ratio < 0.2:
        front = 1

    if movmentFlag < 0:
       yaw = 1
    elif movmentFlag > 0:
        yaw=-1

    drone.send_rc_control(0, front*20,  isUp * 5, yaw*15)
    isUp *= -1
    time.sleep(0.05)


def mainPoseDetection(cap, drawLineFlag, droneMode):
    pTime = 0
    adj = 0
    moveto_flag = 0
    detector = pem.poseDetector()
    recordFlag = False
    isUp = 1
    while cv2.waitKey(1) != 27:  # esc
        keyPrass = cv2.waitKey(1) & 0xFF
        if keyPrass == ord('r') or keyPrass == ord('R') and recordFlag == False:
            frame_width = 960
            frame_height =720
            size = (frame_width, frame_height)
            name = datetime.now().strftime("%d.%m.%Y %H-%M-%S")
            result = cv2.VideoWriter(name + ".avi", cv2.VideoWriter_fourcc(*'MJPG'), 24.0, size)
            recordFlag = True

        if droneMode == True:
            img = drone.get_frame_read().frame # capturing frame from drone
        else:
            success, img = cap.read()

        crop_img = np.array(img)  ########## For fully deployment uncomment this row and comment the row below
        adj += 1
        crop_flag = False
        height, width, c = img.shape
        h_ratio = 0.5
        if adj > 51:
            crop_flag = True
            crop_img[:yMinf, :, :] = 0
            crop_img[:, :xMinf, :] = 0
            crop_img[yMaxf:, :, :] = 0
            crop_img[:, xMaxf:, :] = 0

        detector.findPose(crop_img, True)
        lmList = detector.findPosition(crop_img, draw=True)
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
            h_ratio = h / height
            midPoint = (xMin + w / 2, yMin + h / 2)  # mid point of the bbox of the character
            moveTo, yellow_lines = hotZones(img, height, width, maxLength, midPoint, drawLineFlag)
            if moveTo!= 0:
                moveto_flag = moveTo

            if moveto_flag!=0 :
                if midPoint[0]>yellow_lines[0] and midPoint[0] < yellow_lines[1]:
                    moveto_flag = 0

            if drawLineFlag:
                cv2.rectangle(img, (xMax + round(maxLength * 0.25), yMax + round(maxLength * 0.25)),
                              (xMin - round(maxLength * 0.25), yMin - round(maxLength * 0.25)), (139, 34, 104), 2)

        if len(lmList) == 0:
            adj = 30

        if len(lmList) != 0:
            xMaxf = xMax + int(1.4 * w)
            xMinf = xMin - int(1.4 * w)
            yMaxf = yMax + int(1.8 * h)
            yMinf = yMin - int(1.2 * h)

        if drawLineFlag:  # show fps
            cTime = time.time()
            fps = 1 / (cTime - pTime)
            pTime = cTime
            cv2.putText(img, str(int(fps)), (70, 50), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 0), 3)

        if adj > 50 and len(lmList) != 0:
            if not crop_flag:
                img[:yMinf, :, :] = 0
                img[:, :xMinf, :] = 0
                img[yMaxf:, :, :] = 0
                img[:, xMaxf:, :] = 0

        if recordFlag:
            result.write(img)
            img = cv2.circle(img, (25, 25), 10, (0, 0, 255), -1)

        # result.write(img)
        cv2.imshow("Image", img)
        if droneMode == True:
            movmentControler(isUp,moveto_flag, fps,h_ratio)

        if keyPrass == ord('s') or keyPrass == ord('S') and recordFlag == True:
            result.release()
            recordFlag = False

    if recordFlag:
        result.release()
        print("stop recording")
    cv2.destroyAllWindows()


if __name__ == "__main__":
    arg_input = argv[1]  # path input for a video by defalt set to live captun
    drawLines = argv[2]  # draw test lines
    droneMode=False

    if arg_input == '0':
        cap = cv2.VideoCapture(0)  # Camputer Camera
    elif arg_input == '1':
        droneMode=True
    else:
        cap = cv2.VideoCapture(arg_input)  # walking video

    # rescaling resolution for better preformance
    if droneMode == False:
        cap.set(3, 640)
        cap.set(4, 480)

    if drawLines == "True":
        drawLineFlag = True
    elif drawLines == "False":
        drawLineFlag = False
    else:
        print("invalid flag input")

    if droneMode == True:
        drone = Tello()
        drone.connect()
        drone.streamon()  # start camera streaming
        cap  = drone
        drone.takeoff()


    mainPoseDetection(cap, True, droneMode)

    if droneMode==True:
        drone.streamoff()  # start camera streaming
        drone.land()

    cv2.destroyAllWindows()
