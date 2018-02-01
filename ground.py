import scipy as sci
import numpy as num
from scipy.constants import c
from math import *

EPSILON = 1e-12

class Ground:
    '''@brief свойства земли для радиоволны заданной длины lamda
    sigma - проводимость в См/м;
    epsilon - действительная часть диэлектрической проницаемости
    '''
    def __init__(self, lamda=1.0, _type='default'):
        self._frequency = c / lamda
        self._type = _type
        self._conductivity = 1
        self._permitivity = 0
        self._n = 0
        self._reflection = {'perp': 1, 'parallel': 1}
        self._parameters = {'default': {'sigma': inf, 'epsilon': 0},
                            'moist silty loam': {'sigma': 0.026, 'epsilon': 30},
                            'dry silty loam': {'sigma': 0.007, 'epsilon': 4},
                            'silty clay': {'sigma': 0.018, 'epsilon': 23},
                            'vegetations': {'sigma': 0.19, 'epsilon': 32},
                            'dry ice': {'sigma': 0.004, 'epsilon': 1.58},
                            }

    def _get_n(self):
        '''коэффициент преломления считается по формуле из википедии через
        мнимую и действительную части диэлектрической проницаемости'''
        sigma = self._parameters[self._type]['sigma']
        epsilon = self._parameters[self._type]['epsilon']
        w = 2 * pi * self._frequency
        imepsilon = sigma / w
        self._n = sqrt((epsilon + sqrt(epsilon ** 2 + imepsilon ** 2)) / 2)
        return self

    def getReflection(self, alpha):
        if self._parameters[self._type]['sigma'] == inf:
            rho = {'perp': 1, 'parallel': 1}
        else:
            self._get_n()
            rho = self._getReflection(alpha)
        return rho

    def _getReflection(self, alpha):
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

