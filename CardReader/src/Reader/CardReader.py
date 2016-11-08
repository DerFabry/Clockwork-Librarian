#encoding: utf8
'''
Created on 11.04.2016

@author: Stephan Fabry
'''
import cv2 #cv2 ist das Package für OpenCV
import numpy as np #numpy ist das Package für n-dimensionale Arrays und Matritzenrechnung. Benötogt von OpenCV
#import math #mit math wird gerechnet. Shocker

'''
Da bisher auf einem Externen Rechner ohne Webcam programmiert wurde, wird eine Aufnahme vom
RaspberryPi hier eingeladen. später auf dem Zielgrät durch den Code in Cam.py ersetzen
'''

filename = "01_image.jpg"
cardsizeX = 1000
cardsizeY = 1397
im = cv2.imread(filename)
im2 = cv2.imread(filename)
print("Bild eingelesen")
#Bild in schwarzweiß umwandeln, um aus 3-kanaliger pixelinformation einen kanal zu machen

gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
cv2.imwrite("02_gray.jpg", gray)
print("in Schwarzweiß umgewandelt")
#Gaußscher weichzeichner um bildflimmern zu vermeiden, Gauß und nicht Mean, weil Gauß due bessere Kantenerhaltung hat

blur = cv2.bilateralFilter(gray,9,75,75)

cv2.imwrite("03_blur.jpg", blur)
print("Weichzeichner übertragen")
#Threshholding

thresh = cv2.adaptiveThreshold(blur, 255, 1, 1, 19, 1)
cv2.imwrite("04_thresh.jpg", thresh)
print("Thresholing")
#findContours

kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(7,7))

opening = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel)

cv2.imwrite("05_opened.jpg", opening)

dilation = cv2.dilate(opening, kernel,iterations = 3)

cv2.imwrite("06_dilated.jpg", dilation)


_, contours , hierarchy = cv2.findContours(opening, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
print("konturen gefunden")
#Die Konturen nach ihrer größe Sortieren

contours = sorted(contours, key=cv2.contourArea, reverse= True)
print("konturen sortiert")
#Die größte kontur sollte bei uniformen Hintergrund der Rand der karte sein

cnt = contours[0]

'''
approxPolyDP ist eine funktion die eine Punktmenge (in diesem falle die Kontur in cnt),
einen epsilon-wert, der die maximale abweichung angibt, und die aussage ob es sich um eine Geschlossene oder offene
Kurve handeln soll übergeben bekommt. die funktion wendet den Douglas-Peuker-Algorithmus zur kantenglättung an. bei 50
px erlaubter abweichung sollte ein viereck entstehen
'''

approx = cv2.approxPolyDP(cnt, 25, True)
print("viereck um die Karte gefunden")
#Für spätere rechenoperationen muss das entstandene Array umgewandelt werden

approx32 = np.array(approx, np.float32)

#zur überprüfung werden die Konturen und das errechnete viereck in das ursprungsbild eingefügt
#die Konturen in Schwarz
cv2.drawContours(im2, [cnt], 0, (0,0,0), 2)
#Das errechnete Viereck in weiß
cv2.drawContours(im2, [approx], 0, (255,255,255), 2)

cv2.imwrite('07_contours.jpg', im2)
print("konturen ins buld eingezeichnet")
#es muss ein weiteres Array erstellt werden, in dem das Ergebnis der Perspektivischen Verzerrung zwischengespeichert werden kann

h = np.array([[0,0],[0,cardsizeY],[cardsizeX,cardsizeY], [cardsizeX,0]], np.float32)

#Hier wird die Matrix zur perspektivischen verzerrung errechnet

transform = cv2.getPerspectiveTransform(approx32, h)
print("transform-matrix erzeugt")
print(transform)
#hier wird die Perspektivische Verzerrung Durchzogen. das bild ist in allen Dimensionen um einen Pixel größer, da 

warp = cv2.warpPerspective(im, transform, (cardsizeX,cardsizeY))
warpDilation = cv2.warpPerspective(dilation, transform, (cardsizeX,cardsizeY))
cv2.imwrite('08_warp.jpg', warp)
cv2.imwrite("09_openwarp.jpg", warpDilation)
print('DONE!')