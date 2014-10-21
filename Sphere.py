'''
Created on 11/04/2014

@author: michaelsandritter
'''

import math
import numpy as np
import Helper as helper
from Ray import Ray

class Sphere(object):
    def __init__(self, center, radius, color):
        self.center = center # point
        self.radius = radius # scalar
        self._color = color # color of sphere
        
    def __repr__(self):
        return "Sphere(%s%s)" %(repr(self.center), self.radius)
     
    def intersectionParameter(self, ray):
        co = self.center - ray.origin
        v = np.dot(co, ray.direction)
        discriminant = v*v -  np.dot(co, co) + self.radius*self.radius
        if discriminant < 0:
            return None
        else:
            return v - math.sqrt(discriminant)
        
    def normalAt(self, p):
        a = self.center - p
        return a / np.linalg.norm(a)
    
    def colorAt(self, ray, t, objectlist):
        sp = ray.pointAtParameter(t)                            # Schnittpunkt am Objekt
        d = ray.direction
        c_out = 0
        for light_source in helper.light_sources:                            
            light = helper.normalize(sp - light_source)                             # Vektor vom Licht zum Schnittpunkt 
            n = self.normalAt(sp)                                   # Normale des Objekts am Schnittpunkt sp
            lr = light - 2 * np.dot(n, light) * n                   # Ausfallwinkel
            Ca = np.array(self.color)   
            c_ambient = Ca * helper.ka
            c_diffus = helper.Cin * helper.kd * np.dot(light, n)
            c_spec = helper.Cin * helper.ks * math.pow(np.dot(lr, -1 * d), 32)
            c_tmp = c_ambient + c_diffus + c_spec
        
            newRay = Ray(sp, light_source - sp)
        
            for o in objectlist:
                x = o.intersectionParameter(newRay)
                if x:
                    c_tmp *= 0.5
                    break
            c_out += c_tmp
        return c_out
        
        
        
        
    
    @property 
    def color(self):
        return self._color
        
    @color.setter
    def color(self, color):
        self._color = color