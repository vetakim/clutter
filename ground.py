import scipy as sci
import numpy as num
from scipy.constants import c

class Ground:
    '''@brief свойства земли для радиоволны заданной длины lamda'''
    def __init__(self, lamda=1.0):
        self._frequency = c / lamda
        self._conductivity = 1
        self._permitivity = 0
        self._reflection = {'perp': 1, 'parallel': 1}

    def getSigma(self):
        return self._conductivity

    def getEpsilon(self):
        return self._permitivity

    def getReflection(self):
        return self._reflection
