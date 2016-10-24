import math

import numpy

import nani


class Vector2View(object):

    __slots__ = ('_data',)

    def __init__(self, data):
        self._data = data

    def __str__(self):
        return "({0}, {1})".format(self.x, self.y)

    @property
    def x(self):
        return self._data[0]

    @x.setter
    def x(self, value):
        self._data[0] = value

    @property
    def y(self):
        return self._data[1]

    @y.setter
    def y(self, value):
        self._data[1] = value

    def set(self, x, y):
        self.x = x
        self.y = y

    def scale(self, value):
        self.x *= value
        self.y *= value


VECTOR2_TYPE = nani.Array(
    element_type=nani.Number(type=numpy.float32),
    shape=(2,),
    view=Vector2View
)
