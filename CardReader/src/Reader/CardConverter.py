'''
Created on 12.04.2016

@author: Stephan
'''
import cv2
import numpy as np

filename ="06_warp.jpg"

im = cv2.imread(filename)

gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)

gauss = cv2.GaussianBlur(gray, (5,5), 2)

thresh = cv2.adaptiveThreshold(gauss, 255, 1, 1, 19, 1)

kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(7,7))

opening = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel)

cv2.imwrite("07_opened.jpg", opening)

dilation = cv2.dilate(opening, kernel,iterations = 3)

cv2.imwrite("08_dilated.jpg", dilation)

print("DONE!")