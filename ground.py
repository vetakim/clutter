import scipy as sci
import numpy as num
from scipy.constants import c
from math import *

EPSILON = 1e-12

class Ground:
    '''@brief свойства земли для радиоволны заданной длины lamda'''
    def __init__(self, lamda=1.0):
        self._frequency = c / lamda
        self._conductivity = 1
        self._permitivity = 0
        self._n = 0
        self._reflection = {'perp': 1, 'parallel': 1}

    @property
    def real(self):
        self._n = 3
        return self

    def getSigma(self):
        return self._conductivity

    def getEpsilon(self):
        return self._permitivity

    def getReflection(self, alpha):
        '''коэффициенты френеля рассчитываются по формулам Френеля (см.
        Сивухина, Оптика, с. 406)'''
        if abs(self._n - 0.0) > EPSILON:
            phi = pi / 2 - alpha
            n = self._n
            psi = asin(sin(phi) / n)
            if (phi - 0.0) > EPSILON:
                perp = (-sin(phi - psi) / sin(phi + psi))
                parallel = (tan(phi - psi) / tan(phi + psi))
            else:
                perp = -1
                parallel = -1
            self._reflection['perp'] = perp
            self._reflection['parallel'] = parallel
        return self._reflection
