#!/usr/bin/python
import picamera
import numpy as np
from picamera.array import PiRGBAnalysis
from picamera.color import Color

class AngleFinder(PiRGBAnalysis):
    def __init__(self, camera):
        super(AngleFinder, self).__init__(camera)
        self.last_color = ''

        self.i=0

    def analyze(self, a):
        self.camera.annotate_text = "%d" % self.i
        self.i+=1

#with picamera.PiCamera(resolution='160x90', framerate=24) as camera:
with picamera.PiCamera() as camera:
    camera.resolution = (1280, 720)
    camera.framerate = 24
    # Fix the camera's white-balance gains
    #camera.awb_mode = 'auto'
    #camera.awb_gains = (1.4, 1.5)
    # Draw a box over the area we're going to watch
    camera.start_preview()


    a = np.zeros((720, 1280, 3), dtype=np.uint8)
    a[360, :, :] = 0xff
    a[:, 640, :] = 0xff
    o = camera.add_overlay(np.getbuffer(a), layer=3, alpha=64)


    # Construct the analysis output and start recording data to it
    with AngleFinder(camera) as analyzer:
        camera.start_recording(analyzer, 'rgb')
        try:
            while True:
                camera.wait_recording(1)
        finally:
            camera.stop_recording()

