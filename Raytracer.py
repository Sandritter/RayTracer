'''
Created on 11/04/2014

@author: michaelsandritter
'''

from Plane import Plane
from Sphere import Sphere
from Triangle import Triangle
from Ray import Ray
import math
import numpy as np
from PIL import Image
import Helper as helper

wRes = 200
hRes = 200
viewAngle = 45
alpha = viewAngle / 2
BACKGROUND_COLOR = np.array([0,0,0])
REFLECTION_FACTOR = 0.2

image = Image.new("RGB", (wRes, hRes), (BACKGROUND_COLOR[0],BACKGROUND_COLOR[1],BACKGROUND_COLOR[2]))

aspectratio = wRes / hRes
height = 2 * np.tan(np.deg2rad(alpha))
width = aspectratio * height

e = np.array([0,1.8,10])
c = np.array([0,3,0])
up = np.array([0,1,0])
ce = c - e
f =  ce / math.sqrt(np.dot(ce,ce))
tmp = np.cross(f, up)
s = tmp / math.sqrt(np.dot(tmp, tmp))
u = np.cross(s, f)

class Raytracer(object):
    
    def __init__(self):
        self.objectList = self.initObjects()
        
    def computeReflectedRay(self, hitPointData):
        ray = hitPointData[1]
        o = hitPointData[0]
        sp = ray.pointAtParameter(hitPointData[2])
        light = helper.normalize(sp - ray.direction)
        n = o.normalAt(sp)
        lr = light - 2 * np.dot(n, light) * n
        return Ray(sp, lr)
        
    def shade(self, level, hitPointData):
        directColor = hitPointData[0].colorAt(hitPointData[1], hitPointData[2], self.objectList)
        reflectedRay = self.computeReflectedRay(hitPointData)
        reflectColor = self.traceRay(level+1, reflectedRay)
        return directColor + REFLECTION_FACTOR*reflectColor
    
    def intersect(self, level, ray, maxlevel):        
        maxdist = float('inf')
        for o in self.objectList:  
            hitdist = o.intersectionParameter(ray)
            if hitdist:
                if hitdist < 0:
                    pass
                elif hitdist < maxdist:
                    if level == 0 and type(o) is Plane or type(o) is Triangle: # check if first intersection is non-reflecting object
                        return ("flag", o, ray, hitdist)
                    elif level == maxlevel:
                        return ("flag", o, ray, hitdist)
                    maxdist = hitdist
                    tmp = o
                    return (tmp, ray, maxdist)
        return None
        
        
    def traceRay(self, level, ray):
        hitPointData = self.intersect(level, ray, 3)
        if hitPointData:
            if hitPointData[0] == "flag": # if object is non-reflecting return only direct light
                return hitPointData[1].colorAt(ray, hitPointData[3], self.objectList)
            return self.shade(level, hitPointData)
        return BACKGROUND_COLOR
        
    def raycast(self):
        pixelwidth = width / (wRes-1)
        pixelheight = height / (hRes-1)
        for x in range(wRes):
            for y in range(hRes):
                color = BACKGROUND_COLOR
                ray = self.calcRay(x,y, pixelwidth, pixelheight)
                color = self.traceRay(0, ray)
                image.putpixel((x,hRes-1-y), (int(color[0]),int(color[1]),int(color[2])))
        image.show()

    def calcRay(self, x, y, pixelwidth, pixelheight):
        xcomp = np.multiply(s, x*pixelwidth - width/2)
        ycomp = np.multiply(u, y*pixelheight - height/2)
        return Ray(e, f + xcomp + ycomp)
                
    def initObjects(self):
        ret = []
        s1 = np.array([0,7.5,-10])
        s2 = np.array([-2.5, 3, -10])
        s3 = np.array([2.5, 3, -10])
        ret.append(Sphere(s1, 2, (255,0,0)))
        ret.append(Sphere(s2, 2, (0,255,0)))
        ret.append(Sphere(s3, 2, (0,0,255)))
        ret.append(Triangle(np.array([0,7.5,-10]), np.array([-3, 3, -10]), np.array([3, 3, -10]), (255,255,0)))
        ret.append(Plane(np.array([0,0,0]), np.array([0,1,0]), (100,100,100)))
        return ret
    
if __name__ == '__main__':
    rayTracer = Raytracer()
    rayTracer.raycast()