'''
Created on 11/04/2014

@author: michaelsandritter
'''
import numpy as np
import Helper as helper
from Ray import Ray
import math

class Triangle(object):
    
    def __init__(self, a, b, c, color):
        self.a = a
        self.b = b
        self.c = c
        self.u = self.b - self.a # direction vector
        self.v = self.c - self.a # direction vector
        self._color = color
        
    def __repr__(self):
        return "Triangle(%s%s%s)" %(repr(self.a), repr(self.b), repr(self.c))
    
    def intersectionParameter(self, ray):
        w = ray.origin - self.a
        dv = np.cross(ray.direction, self.v)
        dvu = np.dot(dv, self.u) # product of ray and vector u
        if dvu == 0.0:
            return None
        wu = np.cross(w, self.u)
        r = (np.dot(dv, w)) / dvu
        s = np.dot(wu, ray.direction) / dvu
        if 0 <= r and r <= 1 and 0 <= s and s <= 1 and r+s <= 1:
            return np.dot(wu, self.v) / dvu
        else:
            return None
        
    def normalAt(self, p):
        w = self.a - p
        h = self.b - p
        x = np.cross(w, h)
        return x / np.linalg.norm(x)
    
    def colorAt(self, ray, t, objectlist):
        sp = ray.pointAtParameter(t)                                # Schnittpunkt am Objekt
        d = ray.direction
        n = self.normalAt(sp)
        Ca = np.array(self.color)
        c_out = 0         
        for light_source in helper.light_sources: 
            light = helper.normalize(sp - light_source)                                 # Vektor vom Licht zum Schnittpunkt  
            lr = light - 2 * np.dot(n, light) * n        
            lightV = helper.normalize(light_source - sp)
            c_ambient = Ca * helper.ka
            c_diffus = helper.Cin * helper.kd * np.dot(lightV, n)
            c_spec = helper.Cin * helper.ks * math.pow(np.dot(lr, d), 32)
            c_tmp = c_ambient + c_diffus + c_spec
            
            newRay = Ray(sp, light_source - sp)
            
            for o in objectlist:
                if o is self:
                    pass
                else:
                    x = o.intersectionParameter(newRay)
                    if x and x > 0:
                        c_tmp *= 0.5
                        break
            c_out += c_tmp
        return c_out
    
    
    @property
    def color(self):
        return self._color
    
    @color.setter
    def color(self, value):
        self._color = value
        