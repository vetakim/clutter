import scipy as sci
import numpy as num
from ground import Ground

class Vibrator:
    def __init__(self, lamda = 1):
        self._lamda = lamda
        self._polarization = "both"
        self._pattern = 1
        self._field = 1
        self._currents = 1
        self._isOnGround = False

    @property
    def free(self):
        self._polarization = "both"
        self._isOnGround = False
        return self

    @property
    def horizontal(self):
        self._polarization = "perpendecular"
        self._isOnGround = True
        return self

    @property
    def vertical(self):
        self._polarization = "parallel"
        self._isOnGround = True
        return self

    @property
    def lamda(self):
        return self._lamda

    @property
    def polarization(self):
        return self._polarization

    @property
    def isOnGround(self):
        return self._isOnGround

    @property
    def currents(self):
        return self._currents

    def setCurrents(self, a, phi):
        self._currents = a * cos(phi)
        return self

    def pattern(self, ground):
        return self._pattern

    def field(self, ground):
        return self._field

