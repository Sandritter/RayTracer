'''
Created on 20/04/2014

@author: michaelsandritter
'''

import numpy as np

class CheckerboardMaterial(object):

    def __init__(self):
        self.baseColor = (255,255,255)
        self.otherColor = (0,0,0)
        self.ac = 1.0
        self.dc = 0.6
        self.sc = 0.4
        self.checkSize = 1
        
    def baseColorAt(self, p):
        v = np.multiply(p, 1.0 / self.checkSize)
        if (int(abs(v[0]) + 0.5) + int(abs(v[1]) + 0.5)+ int(abs(v[2]) + 0.5)) % 2:
            return self.otherColor
        return self.baseColor
        