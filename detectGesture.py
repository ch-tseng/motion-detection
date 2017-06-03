#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
import numpy as np
import cv2

from libraryCH.device.camera import PICamera
from libraryCH.device.lcd import ILI9341

debugDisplay = 2

# construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required=True, help="Path to the input image")
args = vars(ap.parse_args())

lcd = ILI9341(LCD_size_w=240, LCD_size_h=320, LCD_Rotate=180)


def wait():
    raw_input('Press Enter')

image = cv2.imread(args["image"])

gray = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
blur=cv2.GaussianBlur(gray,(5,5),0)

ret , th = cv2.threshold(blur,0,255,cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU)
th = cv2.erode(th, None, iterations=3)
th = cv2.dilate(th, None, iterations=3)
lcd.displayImg(th)
wait()

(contours, hierarchy) = cv2.findContours(th, cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
areas = [cv2.contourArea(temp) for temp in contours]
max_index = np.argmax(areas)
largest_contour=contours[max_index]
cv2.drawContours(image, largest_contour, -1, (0,255,0), 2)
lcd.displayImg(th)
wait()

image2=image
approx=cv2.approxPolyDP(largest_contour,0.01*cv2.arcLength(largest_contour,True),True)
cv2.putText( image2,'Number of approx: ' + str (len(approx)),
       (10,30),cv2.FONT_HERSHEY_COMPLEX_SMALL,1,(255,0,0))
lcd.displayImg(image2)
wait()

image_hull = image
hull = cv2.convexHull(approx,returnPoints=True)
hull2 = cv2.convexHull(approx,returnPoints=False)
defect = cv2.convexityDefects(approx,hull2)
#cv2.drawContours(image_hull,[hull],0,(0,0,255),1)

#draw the points for the hull 
for i in range ( len ( hull ) ):
   [x , y]= hull[i][0].flatten()
   cv2.circle(image_hull,(int(x),int(y)),2,(0,255,0),-1)
   cv2.circle(image_hull,(int(x),int(y)),5,(255,255,0),1)
   cv2.circle(image_hull,(int(x),int(y)),8,(255,0,0),1)

#draw the points for the defect
for i in range(defect.shape[0]):
    s,e,f,d = defect[i,0]
    start = tuple(approx[s][0])
    end = tuple(approx[e][0])
    far = tuple(approx[f][0])
    cv2.line(image_hull,start,end,[0,255,0],2)
    cv2.circle(image_hull,far,5,[0,0,255],-1)

cv2.putText( image_hull,"Fingers by convex hull & defect: " + str ( (len(hull)-2) ) + "," + str(len(defect)),
       (10,30),cv2.FONT_HERSHEY_COMPLEX_SMALL,1,(255,0,0))
print ("Number of Fingers by convex hull: " + str ( (len(hull)-2) ))
print ("Number of Fingers by convex defect: " + str ( len(defect) ))

lcd.displayImg(image_hull)


wait()
