import numpy

import nani

from . import vector2


_PARTICLE_ID = 0
_PARTICLE_POSITION = 1
_PARTICLE_MASS = 2
_PARTICLE_NEIGHBOURS = 3


class ParticleView(object):

    __slots__ = ('_data',)

    def __init__(self, data):
        self._data = data

    def __str__(self):
        return (
            "Particle(id={0}, position={1}, mass={2}, neighbours={3})"
            .format(self.id, self.position, self.mass, self.neighbours)
        )

    @property
    def id(self):
        return self._data[_PARTICLE_ID]

    @property
    def position(self):
        return vector2.Vector2View(self._data[_PARTICLE_POSITION])

    @property
    def mass(self):
        return self._data[_PARTICLE_MASS]

    @mass.setter
    def mass(self, value):
        self._data[_PARTICLE_MASS] = value

    @property
    def neighbours(self):
        return self._data[_PARTICLE_NEIGHBOURS]


PARTICLE_TYPE = nani.Structure(
    fields=(
        ('id', nani.Number(type=numpy.uint32, default=-1)),
        ('position', vector2.VECTOR2_TYPE),
        ('mass', nani.Number(type=numpy.float32, default=1.0)),
        ('neighbours', nani.Object()),
    ),
    view=ParticleView
)
