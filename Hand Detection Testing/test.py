import cv2
from cvzone.HandTrackingModule import HandDetector
from cvzone.ClassificationModule import Classifier
import numpy as np
import math
from gtts import gTTS
import pygame
import tempfile

def speak(text, language='en'):
    tts = gTTS(text, lang=language)
    temp_mp3_file = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3")
    temp_mp3_file.close()
    tts.save(temp_mp3_file.name)
    print(temp_mp3_file.name)
    return temp_mp3_file.name

cap = cv2.VideoCapture(0)
detector = HandDetector(maxHands=1)
classifier = Classifier("Model/keras_model.h5", "Model/labels.txt")

offset = 20
imgSize = 300

folder = "Data/C"
counter = 0

labels = ["0", "1", "2", "3", "4", "5", "A", "B", "C", "G", "H", "L", "O", "P", "Q", "Y"]

while True:
    success, img = cap.read()
    imgOutput = img.copy()
    hands, img = detector.findHands(img)
    if hands:
        hand = hands[0]
        x, y, w, h = hand['bbox']

        imgWhite = np.ones((imgSize, imgSize, 3), np.uint8) * 255
        imgCrop = img[y - offset:y + h + offset, x - offset:x + w + offset]

        try:
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
            else:
                k = imgSize / w
                hCal = math.ceil(k * h)
                imgResize = cv2.resize(imgCrop, (imgSize, hCal))
                imgResizeShape = imgResize.shape
                hGap = math.ceil((imgSize - hCal) / 2)
                imgWhite[hGap:hCal + hGap, :] = imgResize
                prediction, index = classifier.getPrediction(imgWhite, draw=False)

            cv2.rectangle(imgOutput, (x - offset, y - offset-50),
                          (x - offset+90, y - offset-50+50), (255, 0, 255), cv2.FILLED)
            cv2.putText(imgOutput, labels[index], (x, y - 26), cv2.FONT_HERSHEY_COMPLEX, 1.7, (255, 255, 255), 2)

            if cv2.waitKey(1) == ord("s"):
                pygame.init()
                pygame.mixer.init()
                sound = speak(str(labels[index]))
                pygame.mixer.music.load(sound, 'mp3')
                pygame.mixer.music.play()
        except Exception as e:
            print("Hand is out of detection range !!!")

    cv2.imshow("Image", imgOutput)

    if cv2.waitKey(1) == ord('q'):
        break

# Release the PiCamera and close all OpenCV windows
cap.release()
cv2.destroyAllWindows()
