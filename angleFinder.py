#!/usr/bin/python
import picamera
from Log import Log
import numpy as np
import math
from picamera.array import PiRGBAnalysis
from picamera.color import Color

class AngleFinder(PiRGBAnalysis):
    def __init__(self, camera):
        super(AngleFinder, self).__init__(camera)
        log=Log()


        self.last_color = ''
        self.i=0
        self.centre=(1280/2, 720/2)
        self.segList =[]

        a = np.zeros((720, 1280, 3), dtype=np.uint8)

        for i in range(360):
            x,y=self.centre
            segPoints = self.segLine(x,y,i)
            self.segList.append(segPoints)
            self.plotPoints(a,segPoints)

        o = camera.add_overlay(np.getbuffer(a), layer=3, alpha=64)

    def drawBorder(self,a):
        #a[360, :, :] = 0xff
        #a[:, 640, :] = 0xff

        a[0, :, :] = 0xff
        a[:, 0, :] = 0xff

        a[719, :, :] = 0xff
        a[:, 1279, :] = 0xff

    def plotPoints(self,a,points):
        for point in points:
            x,y=point
            a[y,x,:]=0xff
        return a

    def analyze(self, a):
        #log=Log()
        self.camera.annotate_text = "%d" % self.i
        self.i+=1


    def segments(self):
        log=Log()
        step=1
        redsMax=0
        redsMaxAngle=0
        for i in range(360):
            x,y=self.centre
            segPoints = self.segLine(x,y,i*step)
            reds = self.samplePoints(segPoints)
            if(reds> redsMax):
                redsMax=reds
                redsMaxAngle=i
            self.plotPoints(segPoints)
        print "angle",redsMaxAngle,"reds",redsMax

    def samplePoints(self,points):
        #log=Log()
        reds=0
        for point in points:
            x=point[0]
            y=point[1]
            #print x,y
            #pix = self.arrowPa[x][y]
            #reds+=pix[0]
            #if pix[0] != [0]:
            #    print pix, point
        #print pixel_array
        return reds

    def segLine(self,x,y,a):
        #log=Log()
        x1=x2=x
        y1=y2=y
        x1 += int(50*math.sin(math.radians(a)))
        y1 += int(50*math.cos(math.radians(a)))

        x2 += int((self.centre[1]-1)*math.sin(math.radians(a)))
        y2 += int((self.centre[1]-1)*math.cos(math.radians(a)))

        return self.line((x1,y1),(x2,y2))

    def circle(self,x,y,l):
        #log=Log()
        points=[]
        for a in range(360):
            points.append(self.circlePoint(x,y,a,l))
        return points

    def circlePoint(self,x,y,a,l):
        #log=Log()
        x += int(l*math.sin(math.radians(a)))
        y += int(l*math.cos(math.radians(a)))
        return (x,y)





    #   Bresenham's Line Drawing Algorithm
    #   see: http://en.wikipedia.org/wiki/Bresenham%27s_line_algorithm

    def line(self,p0, p1):
        #log=Log()
        points=[]
        x0, y0 = p0
        x1, y1 = p1
        steep = abs(y1 - y0) > abs(x1 - x0)
        if steep:
            x0, y0 = y0, x0
            x1, y1 = y1, x1
        if x0 > x1:
            x0, x1 = x1, x0
            y0, y1 = y1, y0
        delta_x = x1 - x0
        delta_y = abs(y1 - y0)
        error = delta_x // 2
        y = y0
        if y0 < y1:
            y_step = 1
        else:
            y_step = -1

        for x in range(x0, x1+1):
            if steep:
                points.append((y,x))
            else:
                points.append((x,y))
            error -= delta_y
            if error < 0:
                y += y_step
                error += delta_x
        return points



class MeterReader():
    def __init__(self):

        camera = picamera.PiCamera()
        camera.resolution = (1280, 720)
        camera.framerate = 24
        camera.start_preview()



        # Construct the analysis output and start recording data to it
        af = AngleFinder(camera)
        camera.start_recording(af, 'rgb')
        try:
            while True:
                camera.wait_recording(1)
        finally:
            camera.stop_recording()


mr=MeterReader()
