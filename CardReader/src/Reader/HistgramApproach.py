'''
Created on 12.04.2016

@author: Stephan
'''

import cv2
import numpy as np
from matplotlib import pyplot as plt

filename = "08_warp.jpg"
img = cv2.imread(filename)
filename2 = "120.jpg"
img2 = cv2.imread(filename2)
color = ('b','g','r')
for i,col in enumerate(color):
    histr = cv2.calcHist([img],[i],None,[256],[0,256])
    plt.plot(histr,color = col)
    plt.xlim([0,256])
color = ('b--','g--','r--')
for i,col in enumerate(color):
    histr = cv2.calcHist([img],[i],None,[256],[0,256])
    plt.plot(histr,color = col)
    plt.xlim([0,256])

plt.show()
