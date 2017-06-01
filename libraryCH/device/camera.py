#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import picamera
import time

class PICamera:
    def __init__(self):
        self.camera = picamera.PiCamera()

    def CameraConfig(self, sharpness=0, contrast=0, brightness=50, saturation=0, 
                           iso=0, video_stabilization=False,exposure_compensation=0, 
                           exposure_mode='auto', meter_mode='average', awb_mode='auto',
                           image_effect='none', color_effects=None, rotation=0, hflip=False,
                           vflip=False, crop=(0.0, 0.0, 1.0, 1.0), preview=False):
        self.camera.sharpness = sharpness
        self.camera.contrast = contrast
        self.camera.brightness = brightness
        self.camera.saturation = saturation
        self.camera.iso = iso
        self.camera.video_stabilization = video_stabilization
        self.camera.exposure_compensation = exposure_compensation
        self.camera.exposure_mode = exposure_mode
        self.camera.meter_mode = meter_mode
        self.camera.awb_mode = awb_mode
        self.camera.image_effect = image_effect
        self.camera.color_effects = color_effects
        self.camera.rotation = rotation
        self.camera.hflip = hflip
        self.camera.vflip = vflip
        self.camera.crop = crop
        self.preview = preview

    def cameraResolution(self, resolution=(1280, 720)):
        self.camera.resolution = resolution

    def cameraBrightness(self, brightness=None):
        if(brightness>100): brightness = 100
        if(brightness<0): brightness = 0
        self.camera.brightness = brightness

    def cameraContrast(self, contrast=0):
        if(contrast<-100): contrast=-100
        if(contrast>100): contrast=100
        self.camera.contrast = contrast

    def cameraDynamicRange(self, drc_strength='off'):
        self.camera.drc_strength = drc_strength   #'off', 'low', 'medium', 'high'

    def cameraShutter(self,shutter_speed=0):
        self.camera.shutter_speed = shutter_speed

    def cameraISO(self,shutter_iso=0):
        self.camera.iso = iso

    def cameraExpoCompensation(self,exposure_compensation=0):
        if(exposure_compensation<-25): exposure_compensation=-25
        if(exposure_compensation>25): exposure_compensation=25
        self.camera.exposure_compensation = exposure_compensation

    def cameraExMode(self,exposure_mode='auto'):
        #'off','auto','night','nightpreview','backlight','spotlight','sports','snow','beach','verylong','fixedfps','antishake','fireworks'
        self.camera.exposure_mode = exposure_mode

    def takePicture(self, imgPath='captured.jpg', startDelaySeconds=0, 
                          Continuous=False, delayContinusSeconds=5, ContinusTotalCount=0):
        #if(self.preview) == True:
        #    self.camera.start_preview()
        
        time.sleep(startDelaySeconds)
        if(Continuous==True):
            if(ContinusTotalCount==0): ContinusTotalCount=99999999999
            for num in range(0,ContinusTotalCount):
                self.camera.capture(imgPath)
                time.sleep(delayContinusSeconds)
        else:
            self.camera.capture(imgPath)

        #if self.preview == True:
        #   self.camera.stop_preview()
    def recordStart(self, filename="record.h264"):
        self.camera.resolution = (1024, 768)
        self.camera.start_recording(filename)
    
    def recordStop(self):
        self.camera.camera.stop_recording()         

    def powerOff(self):
        self.camera.close()
