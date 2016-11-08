"""
"""
import sys
import cv2
import math
import numpy as np

"""cv2.imwrite('cardsgrey.jpg', im)
thresh = 100	
(thresh1, im1) = cv2.threshold(im,thresh,255,cv2.THRESH_BINARY)
(thresh2, im2) = cv2.threshold(im,thresh,255,cv2.THRESH_BINARY_INV)
(thresh3, im3) = cv2.threshold(im,thresh,255,cv2.THRESH_TRUNC)
(thresh4, im4) = cv2.threshold(im,thresh,255,cv2.THRESH_TOZERO)
(thresh5, im5) = cv2.threshold(im,thresh,255,cv2.THRESH_TOZERO_INV)


cv2.imwrite('bin.jpg', im1)
cv2.imwrite('bininv.jpg', im2)
cv2.imwrite('trunc.jpg', im3)
cv2.imwrite('tozero.jpg', im4)
cv2.imwrite('tozeroinv.jpg', im5)

Funktioniert ansatzweise

"""


def preprocess(img):
	gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
	cv2.imwrite("02_gray.jpg",gray)
	blur = cv2.GaussianBlur(gray,(5,5),2 )
	cv2.imwrite("03_blur.jpg", blur)
	thresh = cv2.adaptiveThreshold(blur, 255, 1, 1, 19, 1)
	cv2.imwrite("04_thresh.jpg", thresh)
	return thresh
"""	contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        contours = sorted(contours, key=cv2.contourArea, reverse= True)[:numcards]

        for card in contours:
                #peri = cv2.arcLength(card,True)
                #approx = rectify(cv2.approxPolyDP(card,0.02*peri,True))

                #box = np.int0(approx)
		box = contours[card]
                cv2.drawContours(im,[box], 0, (255,255,0),6)
        
"""


sys.path.insert(0,"usr/local/lib/python2.7/sitepackages/")



filename = "01_image.jpg"
im = cv2.imread(filename)
gray = cv2.cvtColor(im,cv2.COLOR_BGR2GRAY)
thresh = preprocess(im)
im2, contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
contours = sorted(contours, key=cv2.contourArea, reverse= True)#[:numcards]                         
cnt = contours[0]
approx = cv2.approxPolyDP(cnt, 50, True)
approx32 = np.array(approx , np.float32)
print approx
rect = cv2.minAreaRect(cnt)
print rect[2]
#box = cv2.cv.BoxPoints(rect)
#box = np.int0(box)
#cv2.drawContours(im, [box], 0, (0,0,255), 5)
cv2.drawContours(im, [approx], 0, (255,0,0), 5)
cv2.drawContours(im, [cnt], 0, (0,255,0), 5)

length = 300
xa = 1000
ya = 1000
angleRad = math.fabs(rect[2]) * math.pi / 180.0
print angleRad
xb = int(xa+(length*math.sin(angleRad)))
yb = int(ya+(length*math.cos(angleRad)))

cv2.line(im, (xa,ya), (xb,yb), (0,0,0), 7, 8, 0)
cv2.circle(im, (xa,ya),20, (0,0,0))
cv2.imwrite("05_contours.jpg", im)
if(rect[2]<0):
        h = np.array([[0,0],[0,1397],[1000,1397],[1000,0]],np.float32)
else:
        h = np.array([[0,0],[0,1000],[1397,1000],[1397,0]],np.float32)
transform = cv2.getPerspectiveTransform(approx32, h)
print transform

if(rect[2]<0):
        warp = cv2.warpPerspective(gray, transform, (1001,1398))
else:
        warp = cv2.warpPerspective(gray, transform, (1398,1001))



cv2.imwrite("06_warp.jpg", warp)
crop_warp = warp[80:130, 70:760]
crop_warp_blur =  cv2.GaussianBlur(crop_warp,(3,3),2 )
thresh_crop_wrap = cv2.adaptiveThreshold(crop_warp, 255, 1, 1, 301, 1)
thresh_crop_wrap_inv = (255 - thresh_crop_wrap)
cv2.imwrite("07_croppedTitle.jpg", thresh_crop_wrap_inv)

print "DONE!"
