'''
Created on 11/04/2014

@author: michaelsandritter
'''

import numpy as np

class Ray(object):
    def __init__(self, origin, direction):
        self.origin = origin # point
        self.direction = direction / np.linalg.norm(direction) # vector 
        
    def __repr__(self):
        return 'Ray(%s,%s)' %(repr(self.origin), repr(self.direction))
    
    def pointAtParameter(self, t):
        return self.origin + np.multiply(t+0.001, self.direction)
    
    
