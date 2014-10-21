'''
Created on 11/04/2014

@author: michaelsandritter
'''

import numpy as np
import Helper as helper
from Ray import Ray
import math
from CheckerboardMaterial import CheckerboardMaterial

class Plane(object):

    def __init__(self, point, normal, color):
        self.point = point # point
        self.normal = normal / np.linalg.norm(normal)
        self.color = color
        self.pattern = CheckerboardMaterial()
        
    def __repr__(self):
        return "Plane(%s%s)" %(repr(self.point), repr(self.normal))
    
    def intersectionParameter(self, ray):
        op = ray.origin - self.point
        a = np.dot(op, self.normal)
        b = np.dot(ray.direction, self.normal)
        if b:
            return -a/b
        else:
            return None
    
    def normalAt(self, p):
        return self.normal
        
    def colorAt(self, ray, t, objectlist):
        sp = ray.pointAtParameter(t)                                    # Schnittpunkt am Objekt
        d = ray.direction
        c_out = 0       
        for light_source in helper.light_sources:
            light = helper.normalize(sp - light_source)                # Vektor vom Licht zum Schnittpunkt 
            n = self.normalAt(sp)                                       # Normale des Objekts am Schnittpunkt sp
            lr = light - 2 * np.dot(n, light) * n                       # Ausfallwinkel
            self.color = self.pattern.baseColorAt(sp)
            Ca = np.array(self.color)                                   # Lichtfarbenvektor
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
    
    