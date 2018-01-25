import scipy as sci
import numpy as num

class Ground:
    def __init__(self):
        self._conductivity = 1
        self._permitivity = 0
        self._reflection = {'perp': 1, 'parallel': 1}

    def getSigma(self, frequency):
        return self._conductivity

    def getEpsilon(self, frequency):
        return self._permitivity

    def getReflection(self, frequency):
        return self._reflection
