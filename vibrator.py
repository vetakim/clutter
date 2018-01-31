import scipy as sci
import numpy as np
from ground import Ground
from math import *
from ground import *

EPSILON = 1e-12

class Vibrator:
    def __init__(self, lamda = 1):
        self._lamda = lamda
        self._k = 2 * pi / self._lamda
        self._pattern = { 'azimuth': np.array([]), 'elevation':
                         np.array([]) }
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
        self._polarization = 'perp'
        self._isOnGround = True
        self._get_pattern = {'elevation': self._horizontal_pattern_elevation,
                             'azimuth': self._horizontal_pattern_azimuth}
        return self

    @property
    def vertical(self):
        self._polarization = 'parallel'
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
        return abs(F)

    def _horizontal_pattern_elevation(self, alpha, ground, height):
        '''значение ДН горизонтального вибратора по углу места alpha'''
        h = height
        p = ground.getReflection(alpha)[self._polarization]
        k = self._k
        Fs = sin(k * h * sin(alpha))
        if (1 - p) < EPSILON:
            Fp = 1
        else:
            Fp = hypot(1 + p * cos(2 * k * h * sin(alpha)), sin(2 * k * h * sin(alpha)))
        return abs(Fs) * Fp

    def _horizontal_pattern_azimuth(self, phi, ground, height):
        '''значение ДН горизонтального вибратора по азимуту phi'''
        return nan

    def _vertical_pattern_elevation(self, alpha, ground, height):
        '''значение ДН вертикального вибратора по углу места alpha'''
        h = height
        p = ground.getReflection(alpha)[self._polarization]
        k = self._k
        Fs = self._free_pattern_elevation(alpha) * cos(k * h * sin(alpha))
        if (1 - p) < EPSILON:
            Fp = 1
        else:
            Fp = hypot(1 + p * cos(2 * k * h * sin(alpha)), sin(2 * k * h * sin(alpha)))
        return abs(Fs) * Fp

    def _vertical_pattern_azimuth(self, phi, ground, height):
        '''значение ДН вертикального вибратора по азимуту phi'''
        return nan

    def calcPattern(self, elevation, azimuth=np.array([]), height=0.0, isRealGround=False):
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
            ground = Ground(self._lamda)
            if isRealGround:
                ground.real
            angles = {'elevation': elevation, 'azimuth': azimuth}
            for plane in self._pattern:
                self._pattern[plane] = np.array([
                    self._get_pattern[plane](angle, ground, height)
                    for angle in angles[plane]])
        return self

    def getPattern(self, normed=True):
        '''метод для получения ДН в виде словаря, где ключом является
        плоскость, в которой рассматривается ДН: азимутальная или
        угломестная.'''
        if normed:
            if self._pattern['elevation'].size != 0:
                self._pattern['elevation'] /= (self._pattern['elevation']).max()
            if self._pattern['azimuth'].size != 0:
                self._pattern['azimuth'] /= (self._pattern['azimuth']).max()
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

