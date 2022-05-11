# cv2 = opencv-python package, mediapipe = mediapipe package both added to the project
import cv2
import mediapipe as mp
import time

mpDraw = mp.solutions.drawing_utils
mpFaceMesh = mp.solutions.face_mesh
faceMesh = mpFaceMesh.FaceMesh(max_num_faces=2)
drawSpec = mpDraw.DrawingSpec(thickness=2, circle_radius=1)
# cap = cv2.VideoCapture('PexelVideo/talk.mp4')  # talk video
# cap = cv2.VideoCapture('PexelVideo/talking.mp4') # talking video
cap = cv2.VideoCapture('PexelVideo/mul_faces.mp4') # talking video
# cap = cv2.VideoCapture(0) # Camputer Camera
pTime = 0


while True:
    success, img = cap.read()
    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = faceMesh.process(imgRGB)

    if results.multi_face_landmarks:
        for faceLMS in results.multi_face_landmarks:
            mpDraw.draw_landmarks(img, faceLMS, mpFaceMesh.FACE_CONNECTIONS, drawSpec, drawSpec)
            for id, lm in enumerate(faceLMS.landmark):
                ih, iw, ic = img.shape
                x, y = int(lm.x * iw), int(lm.y * ih)
                print(id, x, y)

    cTime = time.time()
    fps = 1/(cTime-pTime)
    pTime = cTime

    cv2.putText(img, f'FPS:{int(fps)}', (20, 50), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 150), 3)

    cv2.imshow("Image", img)
    cv2.waitKey(1)