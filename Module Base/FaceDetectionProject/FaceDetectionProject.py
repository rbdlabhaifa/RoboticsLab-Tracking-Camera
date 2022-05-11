# cv2 = opencv-python package, mediapipe = mediapipe package both added to the project
import cv2
import mediapipe as mp
import time

mpDraw = mp.solutions.drawing_utils
mpFaceDetection = mp.solutions.face_detection
faceDetection = mpFaceDetection.FaceDetection()

#cap = cv2.VideoCapture('PexelVideo/face.mp4')  # face video
# cap = cv2.VideoCapture('PexelVideo/hiddenface.mp4')  # hiddenface video
cap = cv2.VideoCapture('PexelVideo/multiface.mp4') # multi-face video
# cap = cv2.VideoCapture(0) # Camputer Camera
pTime = 0

while True:
    success, img = cap.read()
    # img  = cv2.resize(img, (480,840)) - for 'PexelVideo/face.mp4'
    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = faceDetection.process(imgRGB)
    # print(results) # .faceDetection_landmarks
    if results.detections:

        for id, detection in enumerate(results.detections):
            # mpDraw.draw_detection(img, detection)
            print(id, detection)
            # print(id, detection.score)
            # print(detection.location_data.relative_bounding_box)
            bboxC = detection.location_data.relative_bounding_box
            ih, iw, ic = img.shape
            bbox = int(bboxC.xmin * iw), int(bboxC.ymin * ih), \
                   int(bboxC.width * iw), int(bboxC.height * ih)
            cv2.rectangle(img, bbox, (255, 0, 150), 2)
            cv2.putText(img, f'{int(detection.score[0]*100)}%', (bbox[0]+10, bbox[1]+30), cv2.FONT_HERSHEY_PLAIN, 2, (255, 0, 150), 3)

    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime
    cv2.putText(img, f'FPS: {int(fps)}', (20, 40), cv2.FONT_HERSHEY_PLAIN, 2, (255, 0, 150), 3)

    cv2.imshow("Image", img)
    cv2.waitKey(1)
