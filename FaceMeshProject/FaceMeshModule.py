# cv2 = opencv-python package, mediapipe = mediapipe package both added to the project
import cv2
import mediapipe as mp
import time


class FaceMeshDetector():

    def __init__(self, staticMode = False, maxFaces = 2 ,detectionCon = 0.5, trackCon = 0.5):
        self.StaticMode = staticMode
        self.MaxFaces = maxFaces
        self.detectionCon = detectionCon
        self.trackCon = trackCon

        self.mpDraw = mp.solutions.drawing_utils
        self.mpFaceMesh = mp.solutions.face_mesh
        self.faceMesh = self.mpFaceMesh.FaceMesh(staticMode, maxFaces, detectionCon, trackCon)
        self.drawSpec = self.mpDraw.DrawingSpec(thickness=1, circle_radius=1)

    def findFaceMesh(self, img, draw=True):
        self.imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results = self.faceMesh.process(self.imgRGB)
        faces = []
        if self.results.multi_face_landmarks:

            for faceLMS in self.results.multi_face_landmarks:
                if draw:
                    self.mpDraw.draw_landmarks(img, faceLMS, self.mpFaceMesh.FACE_CONNECTIONS, self.drawSpec, self.drawSpec)
                face = []
                for id, lm in enumerate(faceLMS.landmark):
                    ih, iw, ic = img.shape
                    x, y = int(lm.x * iw), int(lm.y * ih)
                    cv2.putText(img, str(id), (x, y), cv2.FONT_HERSHEY_PLAIN, 0.5, (255, 0, 150), 1)
                    # print(id, x, y)
                    face.append([x, y])
                faces.append(face)
        return img, faces

def main():

    cap = cv2.VideoCapture('PexelVideo/talk.mp4')  # talk video
    # cap = cv2.VideoCapture('PexelVideo/talking.mp4')  # talking video
    # cap = cv2.VideoCapture(0) # Camputer Camera
    pTime = 0
    detector = FaceMeshDetector()
    while True:
        success, img = cap.read()
        img, faces = detector.findFaceMesh(img)
        if len(faces)!= 0:
            print(len(faces[0]))
        cTime = time.time()
        fps = 1/(cTime-pTime)
        pTime = cTime

        cv2.putText(img, f'FPS:{int(fps)}', (20, 50), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 150), 3)

        cv2.imshow("Image", img)
        cv2.waitKey(1)

if __name__ == "__main__":
    main()