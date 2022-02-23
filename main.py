import cvzone
import cv2
from cvzone.FaceMeshModule import FaceMeshDetector
from cvzone.PlotModule import LivePlot

#cap = cv2.VideoCapture("blinking.mp4")
cap = cv2.VideoCapture(0)
detector = FaceMeshDetector(maxFaces=1)
plotY = LivePlot(640, 360, [25, 45], invert=True)

idList = [22, 23, 24, 26, 110, 157, 158, 159, 160, 161, 130, 243]

blinking_num = 0
counter = 0
color = (0, 200, 0)

while True:

    if cap.get(cv2.CAP_PROP_POS_FRAMES) == cap.get(cv2.CAP_PROP_FRAME_COUNT):
        cap.set(cv2.CAP_PROP_POS_FRAMES, 0)

    success, img = cap.read()

    img, faces = detector.findFaceMesh(img, draw=False)

    if faces:
        face = faces[0]
        for id in idList:
            cv2.circle(img, face[id], radius=2, color=color, thickness=cv2.FILLED)
        leftUp = face[159]
        leftDown = face[23]
        leftLeft = face[130]
        leftRight = face[243]
        lengthVertical, _ = detector.findDistance(leftUp, leftDown)
        lengthHorizontal, _ = detector.findDistance(leftLeft, leftRight)

        cv2.line(img, leftUp, leftDown, color=color, thickness=3)
        cv2.line(img, leftLeft, leftRight, color=color, thickness=3)

        ratio = (lengthVertical / lengthHorizontal) * 100
        ImagePlot = plotY.update(ratio, color)
        cv2.imshow('ImagePlot', ImagePlot)

        if ratio < 38 and counter == 0:
            blinking_num += 1
            counter = 1
            color = (0, 0, 200)
        if counter != 0:
            counter += 1
            if counter > 10:
                counter = 0
                color = (0, 200, 0)

        cvzone.putTextRect(img, f"blinking: {blinking_num}", (10, 50), scale=2, colorR=color)

    cv2.imshow('Image', img)
    cv2.waitKey(10)
