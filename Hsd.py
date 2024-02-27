import cv2, openpyxl
from time import sleep

import pyautogui
from cvzone.HandTrackingModule import HandDetector
from cvzone.ClassificationModule import Classifier
import pyautogui as pa
import mysql.connector as sql
import numpy as np
import math


con = sql.connect(host="localhost",user="root",password="",database="feedback")
cursor=con.cursor()

cap = cv2.VideoCapture(0)
detector = HandDetector(maxHands=1, minTrackCon=0.7)
classifier = Classifier("Model/keras_model.h5", "Model/labels.txt")

offset = 20
imgSize = 300

timer = 0
sr = False
sg = False


# ex = openpyxl.Workbook()
# sheet = ex.active
# sheet.title = "Feedback List"
# sheet.append(['Feedback'])

labels = ["Good", "Bad", "Ok", "Submit"]
fingers = 0




while True:
    success, img = cap.read()
    imgOutput = img.copy()
    hands, img = detector.findHands(img)


    # if sg:
    #
    #     if sr is False:
    #         timer = time.time() - initialTime
    #         cv2.putText(imgOutput, str(int(timer)), (10, 90), cv2.FONT_HERSHEY_PLAIN, 6, (255, 0, 255), 4)



    if hands:
        hand = hands[0]
        x, y, w, h = hand['bbox']
        hand = hands[0]
        fingers = detector.fingersUp(hand)
        # print(fingers)

        imgWhite = np.ones((imgSize, imgSize, 3), np.uint8) * 255
        imgCrop = img[y - offset:y + h + offset, x - offset:x + w + offset]

        imgCropShape = imgCrop.shape

        aspectRatio = h / w

        if aspectRatio > 1:
            k = imgSize / h
            wCal = math.ceil(k * w)
            imgResize = cv2.resize(imgCrop, (wCal, imgSize))
            imgResizeShape = imgResize.shape
            wGap = math.ceil((imgSize - wCal) / 2)
            imgWhite[:, wGap:wCal + wGap] = imgResize
            prediction, index = classifier.getPrediction(imgWhite, draw=False)
            # if timer>3:
            #     sr = True
            #     timer = 0
            Feedback = (labels[index])
            print(Feedback)
            # if Feedback == "Good":
            #     pa.moveTo(470,562)
            #     pa.click(470,562)
            #     sleep(2)
            # if Feedback == "Bad":
            #     pa.moveTo(765, 516)
            #     pa.click(765, 516)
            #     sleep(2)

            # sub = pa.locateCenterOnScreen("Submit.png")
            # pa.moveTo(sub)
            # pa.click()

            # con = sql.connect(host="localhost", user="root", password="", database="feedback")
            # cursor = con.cursor()
            # cursor.execute("insert into feedback values('"  "', '" + Feedback + "')")
            # cursor.execute("commit")
            # con.close()

        else:
            k = imgSize / w
            hCal = math.ceil(k * h)
            imgResize = cv2.resize(imgCrop, (imgSize, hCal))
            imgResizeShape = imgResize.shape
            hGap = math.ceil((imgSize - hCal) / 2)
            imgWhite[hGap:hCal + hGap, :] = imgResize
            prediction, index = classifier.getPrediction(imgWhite, draw=False)

        cv2.rectangle(imgOutput, (x - offset, y - offset - 50),
                  (x - offset + 90, y - offset - 50 + 50), (255, 0, 255), cv2.FILLED)
        cv2.putText(imgOutput, labels[index], (x, y - 26), cv2.FONT_HERSHEY_COMPLEX, 1.7, (255, 255, 255), 2)

        cv2.rectangle(imgOutput, (x - offset, y - offset),
                  (x + w + offset, y + h + offset), (255, 0, 255), 4)
    #
    #
    #
    cv2.imshow("Image", imgOutput)
    key = cv2.waitKey(1)
    #
    #
    # if key == ord('s'):
    #     sg = True
    #     initialTime = time.time()
    #     sr = False
    # if key == ord("q"):
    #     break
    # ex.save("feedback.xlsx")




