'''
Created on 19/04/2014

@author: michaelsandritter
'''

import numpy as np

Cin = np.array([255,255,255])
ks = 0.3
ka = 0.6
kd = 0.4 
l = np.array([30,30,10]) 
l2 = np.array([-10,100,30])
light_sources = [l]

def normalize(vektor):
    return vektor / np.linalg.norm(vektor)