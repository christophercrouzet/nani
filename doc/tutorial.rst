.. currentmodule:: nani

.. _tutorial:

Tutorial
========

Creating an array in NumPy requires to provide a ``dtype`` describing the data
type for each element of the array. With Nani, a more explicit syntax is used
to define the data type, as well as other properties such as the default values
and the view types.

As a result, creating a NumPy array through Nani requires an additional step:

    * describe a NumPy array's ``dtype`` with Nani, using the
      :ref:`data types <data_types>` provided, such as :class:`Number`,
      :class:`Array`, :class:`Structure`, and so on.
    * resolve Nani's data type into a format compatible with NumPy, using
      the function :func:`resolve`.
    * use the resolved properties to create the NumPy array through the usual
      `numpy`'s API, and to optionally offer an abstraction layer around
      it.


.. _flat_number_array:

Flat Array of Integers
----------------------

.. code-block:: python

   >>> import numpy
   >>> import nani
   >>> data_type = nani.Number(type=numpy.int32)
   >>> dtype, default, view = nani.resolve(data_type)
   >>> a = numpy.arange(15, dtype=dtype)
   >>> a
   [ 0  1  2  3  4  5  6  7  8  9 10 11 12 13 14]
   >>> type(a)
   <type 'numpy.ndarray'>
   >>> v = view(a)
   >>> v
   [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14]
   >>> type(v)
   <class 'nani.ArrayView'>


This example is the simplest usage possible, making it a good start to
understand what's going on.

Firstly, an integral data type using :class:`Number` is defined. This is
describing the type of each element of the NumPy array that will be created. By
default, :class:`Number` has a ``type`` value set to ``numpy.float_``,
which needs to be overriden here to describe an integer instead.

Then the :func:`resolve` function returns, amongst other properties, a NumPy
``dtype`` which is directly used to initialize the NumPy array.

The view generated by :func:`resolve` can be used to wrap the whole NumPy
array. Here it is nothing more than a simple emulation of a Python container
[1]_: it has a length, it is iterable, and it can be queried for membership
using the ``in`` keyword. Of course, it is possible to provide a different
interface.


.. _vector2:

Array of Vector2-like Elements
------------------------------

.. code-block:: python

   >>> import numpy
   >>> import nani
   >>> vector2_type = nani.Array(
   ...     element_type=nani.Number(),
   ...     shape=2,
   ...     name='Vector2')
   >>> dtype, default, view = nani.resolve(vector2_type, name='Positions')
   >>> a = numpy.zeros(3, dtype=dtype)
   >>> v = view(a)
   >>> for i, position in enumerate(v):
   ...     position[0] = i + 1
   ...     position[1] = i + 2
   >>> v
   [[1.0, 2.0], [2.0, 3.0], [3.0, 4.0]]
   >>> type(v)
   <class 'nani.Positions'>
   >>> type(v[0])
   <class 'nani.Vector2'>


Vector2 structures are best represented in NumPy using a sub-array of size 2.
The same can be expressed in Nani and the view generated will correctly wrap
the whole NumPy array into a container-like class [1]_, but accessing its
elements will also return yet another object with a similar interface.


.. _vector2_custom_view:

Vector2 Array With a Custom View
--------------------------------

.. code-block:: python

   >>> import math
   >>> import numpy
   >>> import nani
   >>> class Vector2(object):
   ...     __slots__ = ('_data',)
   ...     def __init__(self, data):
   ...         self._data = data
   ...     def __str__(self):
   ...         return "(%s, %s)" % (self.x, self.y)
   ...     @property
   ...     def x(self):
   ...         return self._data[0]
   ...     @x.setter
   ...     def x(self, value):
   ...         self._data[0] = value
   ...     @property
   ...     def y(self):
   ...         return self._data[1]
   ...     @y.setter
   ...     def y(self, value):
   ...         self._data[1] = value
   ...     def length(self):
   ...         return math.sqrt(self.x ** 2 + self.y ** 2)
   >>> vector2_type = nani.Array(
   ...     element_type=nani.Number(),
   ...     shape=2,
   ...     view=Vector2)
   >>> dtype, default, view = nani.resolve(vector2_type, name='Positions')
   >>> a = numpy.array([(1.0, 3.0), (2.0, 4.0)], dtype=dtype)
   >>> v = view(a)
   >>> for position in v:
   ...     position.x *= 1.5
   ...     position.y *= 2.5
   ...     position.length()
   7.64852927039
   10.4403065089
   >>> a
   [[  1.5   7.5]
   [  3.   10. ]]
   >>>  v
   [(1.5, 7.5), (3.0, 10.0)]


This time a custom view for the Vector2 elements is provided. As per the
documentation for the Nani data type :class:`Array`, the view is a class
accepting a single parameter ``data``.

This view defines a custom interface that allows accessing the Vector2 elements
through the ``x`` and ``y`` properties, as well as retrieving the length of
the vector.

.. note::

   To expose a sequence-like interface, similar to what Nani generates
   dynamically, it is necessary to implement it manually.


.. _particle_struct:

Particle Structure
------------------

.. code-block:: python

   >>> import numpy
   >>> import nani
   >>> class Vector2(object):
   ...     __slots__ = ('_data',)
   ...     def __init__(self, data):
   ...         self._data = data
   ...     def __str__(self):
   ...         return "(%s, %s)" % (self.x, self.y)
   ...     @property
   ...     def x(self):
   ...         return self._data[0]
   ...     @x.setter
   ...     def x(self, value):
   ...         self._data[0] = value
   ...     @property
   ...     def y(self):
   ...         return self._data[1]
   ...     @y.setter
   ...     def y(self, value):
   ...         self._data[1] = value
   >>> vector2_type = nani.Array(
   ...     element_type=nani.Number(),
   ...     shape=2,
   ...     view=Vector2)
   >>> particle_type = nani.Structure(
   ...     fields=(
   ...         ('position', vector2_type),
   ...         ('velocity', vector2_type),
   ...         ('size', nani.Number(default=1.0)),
   ...     ),
   ...     name='Particle')
   >>> dtype, default, view = nani.resolve(particle_type, name='Particles')
   >>> a = numpy.array([default] * 2, dtype=dtype)
   >>> v = view(a)
   >>> for i, particle in enumerate(v):
   ...     particle.position.x = (i + 2) * 3
   ...     particle.velocity.y = (i + 2) * 4
   ...     particle.size *= 2
   ...     particle
   Particle(position=(6.0, 0.0), velocity=(0.0, 8.0), size=2.0)
   Particle(position=(9.0, 0.0), velocity=(0.0, 12.0), size=2.0)
   >>> data = nani.get_data(v)
   >>> data['position'] += data['velocity']
   >>> data
   [([6.0, 8.0], [0.0, 8.0], 1.0) ([9.0, 12.0], [0.0, 12.0], 2.0)]


Building upon the previous example, a particle data type is defined in the form
of a NumPy structured array. The Vector2 data type is reused for the
``position`` and ``velocity`` fields, with its custom view still giving access
to the ``x`` and ``y`` properties.

The default values returned by the :func:`resolve` function is also used
here to initialize NumPy's array, ensuring that the ``size`` field is set to
``1.0`` for each particle.

At any time, the NumPy array data can be retrieved from an array view generated
by Nani using the :func:`get_data` function, allowing the user to bypass
the interface provided.


.. _atomic_views:

Atomic Views
------------

When accessing or setting an atomic element—such as a number—in a NumPy array,
its value is directly returned. The views dynamically generated by Nani follow
this principle by default but also offer the possibility to add an extra layer
between the user and the value. One use case could be to provide a more
user-friendly interface to manipulate bit fields (or flags):

   >>> import sys
   >>> import numpy
   >>> import nani
   >>> if sys.version_info[0] == 2:
   ...     def iteritems(d):
   ...         return d.iteritems()
   ... else:
   ...     def iteritems(d):
   ...         return iter(d.items())
   >>> _PLAYER_STATE_ALIVE = 1 << 0
   >>> _PLAYER_STATE_MOVING = 1 << 1
   >>> _PLAYER_STATE_SHOOTING = 1 << 2
   >>> _PLAYER_STATE_LABELS = {
   ...     _PLAYER_STATE_ALIVE: 'alive',
   ...     _PLAYER_STATE_MOVING: 'moving',
   ...     _PLAYER_STATE_SHOOTING: 'shooting'
   ... }
   >>> class PlayerState(object):
   ...     __slots__ = ('_data', '_index')
   ...     def __init__(self, data, index):
   ...         self._data = data
   ...         self._index = index
   ...     def __str__(self):
   ...         value = self._data[self._index]
   ...         return ('(%s)' % (', '.join([
   ...             "'%s'" % (name,)
   ...             for state, name in iteritems(_PLAYER_STATE_LABELS)
   ...             if value & state
   ...         ])))
   ...     @property
   ...     def alive(self):
   ...         return self._data[self._index] & _PLAYER_STATE_ALIVE != 0
   ...     @alive.setter
   ...     def alive(self, value):
   ...         self._data[self._index] |= _PLAYER_STATE_ALIVE
   ...     @property
   ...     def moving(self):
   ...         return self._data[self._index] & _PLAYER_STATE_MOVING != 0
   ...     @moving.setter
   ...     def moving(self, value):
   ...         self._data[self._index] |= _PLAYER_STATE_MOVING
   ...     @property
   ...     def shooting(self):
   ...         return self._data[self._index] & _PLAYER_STATE_SHOOTING != 0
   ...     @shooting.setter
   ...     def shooting(self, value):
   ...         self._data[self._index] |= _PLAYER_STATE_SHOOTING
   >>> vector2_type = nani.Array(
   ...     element_type=nani.Number(),
   ...     shape=2)
   >>> player_type = nani.Structure(
   ...     fields=(
   ...         ('name', nani.String(length=32, default='unnamed')),
   ...         ('position', vector2_type),
   ...         ('state', nani.Number(
   ...             type=numpy.uint8,
   ...             default=_PLAYER_STATE_ALIVE,
   ...             view=PlayerState)),
   ...     ),
   ...     name='Player')
   >>> dtype, default, view = nani.resolve(player_type, name='Players')
   >>> a = numpy.array([default] * 2, dtype=dtype)
   >>> v = view(a)
   >>> first_player = v[0]
   >>> first_player
   Player(name=unnamed, position=[0.0, 0.0], state=('alive'))
   >>> first_player.state.moving = True
   >>> first_player.state
   ('alive', 'moving')
   >>> first_player.state.shooting
   False


The NumPy array created here is made of elements each representing a ``Player``
from a game. The view class ``PlayerState`` allows to manipulate the state
of the player (alive, moving, shooting) by abstracting the bitwise operations
required to read/set the flags from/to the ``numpy.uint8`` data. As per the
documentation of the data type :class:`Number`, the view class' ``__init__``
method is required to accept 2 parameters: ``data`` and ``index``.

----

.. [1] See the ``Collection`` item in the table for
   `Abstract Base Classes for Containers`_.

.. _Abstract Base Classes for Containers:
   https://docs.python.org/library/collections.abc.html