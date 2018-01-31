import scipy as sci
import numpy as np
from ground import Ground
from math import *

EPSILON = 1e-12

class Vibrator:
    def __init__(self, lamda = 1):
        self._lamda = lamda
        self._k = 2 * pi / self._lamda
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
        self._get_pattern = {'elevation': self._horizontal_pattern_elevation,
                             'azimuth': self._horizontal_pattern_azimuth}
        return self

    @property
    def vertical(self):
        self._isOnGround = True
        self._get_pattern = {'elevation': self._vertical_pattern_elevation,
                             'azimuth': self._vertical_pattern_azimuth}
        return self

    @property
    def lamda(self):
        return self._lamda

    @property
    def isOnGround(self):
        return self._isOnGround


    def _free_pattern_azimuth(self, phi):
        '''ДН в свободном пространстве по азимуту'''
        return 1.0

    def _free_pattern_elevation(self, alpha):
        '''значение ДН в свободном пространстве по углу места alpha'''
        if abs(cos(alpha)) > EPSILON:
            F = cos((pi / 2) * sin(alpha)) / cos(alpha)
        else:
            F = 0.0
        return F

    def _horizontal_pattern_elevation(self, alpha, ground):
        '''значение ДН горизонтального вибратора по углу места alpha'''
        h = ground['height']
        F = sin(self._k * h * sin(alpha))
        return F

    def _horizontal_pattern_azimuth(self, phi, ground):
        '''значение ДН горизонтального вибратора по азимуту phi'''
        return nan

    def _vertical_pattern_elevation(self, alpha, ground):
        '''значение ДН вертикального вибратора по углу места alpha'''
        h = ground['height']
        F = self._free_pattern_elevation(alpha) * cos(self._k * h * sin(alpha))
        return F

    def _vertical_pattern_azimuth(self, phi, ground):
        '''значение ДН вертикального вибратора по азимуту phi'''
        return nan

    def calcPattern(self, elevation, azimuth=np.array([]), ground={}):
        ''' расчет диаграммы направленности
        @usage чтобы расчитать ДН, надо сначала задать одно из свойств:
        free, horizontal или vertical.
        '''
        try:
            self._get_pattern
        except AttributeError:
            print('Не задано свойство размещения над землей.')
            print('Допустимые свойства: free, vertical, horizontal')
        else:
            angles = {'elevation': elevation, 'azimuth': azimuth}
            for plane in self._pattern:
                self._pattern[plane] = np.array([
                    self._get_pattern[plane](angle, ground)
                    for angle in angles[plane]])
        return self

    def getPattern(self):
        '''метод для получения ДН в виде словаря, где ключом является
        плоскость, в которой рассматривается ДН: азимутальная или
        угломестная.'''
        return self._pattern

    def getField(self, ground):
        return self._field

    def getCurrents(self):
        return self._currents

    def setCurrents(self, a, phi):
        self._currents = a * cos(phi)
        return self

    def __del__(self):
        del self._pattern

