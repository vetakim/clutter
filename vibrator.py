import scipy as sci
import numpy as np
from ground import Ground
from math import *

EPSILON = 1e-12

class Vibrator:
    def __init__(self, lamda = 1):
        self._lamda = lamda
        self._pattern = { 'azimuth': 1, 'elevation': 1 }
        self._field = 1
        self._currents = 1
        self._isOnGround = False

    @property
    def free(self):
        self._isOnGround = False
        self._get_pattern = {'elevation': self._free_pattern_elevation,
                             'azimuth': self._free_pattern_azimuth}
        return self

    @property
    def horizontal(self):
        self._isOnGround = True
        return self

    @property
    def vertical(self):
        self._isOnGround = True
        return self

    @property
    def lamda(self):
        return self._lamda

    @property
    def isOnGround(self):
        return self._isOnGround

    @property
    def currents(self):
        return self._currents

    def setCurrents(self, a, phi):
        self._currents = a * cos(phi)
        return self

    def _free_pattern_azimuth(self, phi):
        return 1.0

    def _free_pattern_elevation(self, alpha):
        if abs(cos(alpha)) > EPSILON:
            F = cos((pi / 2) * sin(alpha)) / cos(alpha)
        else:
            F = 0.0
        return F

    def calcPattern(self, elevation, azimuth=np.array([]), ground={}):
        ''' расчет диаграммы направленности
        @usage чтобы расчитать ДН, надо сначала задать одно из свойств:
        free, horizontal или vertical.
        '''
        kwargs = {} if not self._isOnGround else ground
        angles = {'elevation': elevation, 'azimuth': azimuth}
        for plane in self._pattern:
            self._pattern[plane] = np.array([
                self._get_pattern[plane](angle, **kwargs)
                for angle in angles[plane]])
        return self

    def getPattern(self):
        '''метод для получения ДН в виде словаря, где ключом является
        плоскость, в которой рассматривается ДН: азимутальная или
        угломестная.'''
        return self._pattern

    def getField(self, ground):
        return self._field

    def __del__(self):
        del self._pattern

