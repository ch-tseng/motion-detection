#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import numpy as np
import cv2
import os
from libraryCH.device.lcd import ILI9341

#----- Your configuration ------------------------
displayDevice = 2  # 1--> LCD monitor  2--> ILI9341 TFT

lcd = ILI9341(LCD_size_w=240, LCD_size_h=320, LCD_Rotate=270)

dislpayType = 2  #1--> Contour  2--> Image
markType = 3  #1--> Draw edge  2-->Box selection  3--> Draw & Box

numInput = raw_input("Please keyin your gesture number (Enter to skip): ")

lcd = ILI9341(LCD_size_w=240, LCD_size_h=320, LCD_Rotate=270)

def wait():
    raw_input('Press Enter')

def createFolder(pathFolder):
    if(not os.path.exists(pathFolder)):
        os.makedirs(pathFolder)

def writeImage(num, img):
    global imgFolder
    imgFile = ("G{}.png".format(num))
    cv2.imwrite(imgFolder + imgFile, img)

imgFolder = ("imgGesture/{}/".format(numInput))
print ("Images will save to: {}".format(imgFolder))
if(not numInput==""):  createFolder(imgFolder)

cap = cv2.VideoCapture(0)

#k=np.ones((3,3),np.uint8)

t0 = cap.read()[1]
t1 = cap.read()[1]

i = 0
while(True):
    grey1 = cv2.cvtColor(t0, cv2.COLOR_BGR2GRAY)
    grey2 = cv2.cvtColor(t1, cv2.COLOR_BGR2GRAY)

    blur1 = cv2.GaussianBlur(grey1,(7,7),0)
    blur2 = cv2.GaussianBlur(grey2,(5,5),0)

    d = cv2.absdiff(blur1, blur2)

    ret, th = cv2.threshold( d, 10, 255, cv2.THRESH_BINARY )

    dilated=cv2.dilate(th, None, iterations=1)


    contours, hierarchy = cv2.findContours(dilated,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
    areas = [cv2.contourArea(c) for c in contours]

    if(dislpayType==1):
        layer = np.zeros(t0.shape[:2], dtype = "uint8")
        markColor = 255
    elif(dislpayType==2):
        layer = t0
        markColor = (0,255,0)

    if(len(areas)>0):
        max_index = np.argmax(areas)
        cnt=contours[max_index]
        x,y,w,h = cv2.boundingRect(cnt)
       # print("area={}, w*h={}".format(areas[max_index], w*h))
        if(areas[max_index]>5000):
            if(markType==1 or markType==3):
                cv2.drawContours(layer, cnt, -1, markColor, 2)
            if(markType==2 or markType==3):
                cv2.rectangle(layer,(x,y),(x+w,y+h), markColor,2)

    lcd.displayImg(layer)
    print(i)

    if(not numInput==""): 
        Cutted = t0[y:y + h, x:x + w]
        layer = layer[y:y + h, x:x + w]
        cv2.imwrite(imgFolder + "color-"+str(i)+".png", Cutted)
        writeImage(i, layer)
    #print("dilated.shape={}".format(dilated.shape))

    t0=t1
    t1=cap.read()[1]    

    if cv2.waitKey(5) == 27 :
        break

    i = i + 1

cap.release()
