.. currentmodule:: nani

.. _overview:

Overview
========

Upon getting started with NumPy, the rules to define |numpy.dtype|_ objects
tend to quickly become *confusing*. Not only different syntaxes can create a
same data type, but it also seems *arbitrary* and hence *difficult* to remember
that sub-array data types can only be defined as tuples while structured data
types exclusively require lists made of field tuples, and so on.

To address this point, Nani takes the stance of offering one—and only one—way
of constructing ``numpy.dtype`` objects. Although this syntax makes the code
more verbose, it also makes it easier to read and to reason about.

Nani's approach allows **type introspection** which brings additional benefits
in the form of dynamically generated **default values** and **view types**.
Default values facilitate the definition of new array elements while view types
are useful to encapsulate interactions with NumPy and to expose a different
public interface to your library users instead of the one provided with
``numpy.ndarray``.


Features
--------

* explicit syntax for defining ``numpy.dtype`` objects.
* generates default values and view types.
* allows for type introspection.


Usage
-----

.. code-block:: python

   >>> import numpy
   >>> import nani
   >>> color_type = nani.Array(
   ...     element_type=nani.Number(type=numpy.uint8, default=255),
   ...     shape=3,
   ...     view=None)
   >>> dtype, default, view = nani.resolve(color_type, name='Color')
   >>> a = numpy.array([default] * 2, dtype=dtype)
   >>> v = view(a)
   >>> for color in v:
   ...     print(color)
   [255, 255, 255]
   [255, 255, 255]


The ``color_type`` above defines an array of 3 ``numpy.uint8`` elements having
each a default value of ``255``. The resulting ``dtype`` and ``default``
objects are used to initialize a new NumPy array of 10 color elements, while
the ``view`` type is used to wrap that array into a standard collection
interface.


.. seealso::

   The :ref:`tutorial` section for more detailed examples and explanations on
   how to use Nani.


.. |numpy.dtype| replace:: ``numpy.dtype``

.. _numpy.dtype: https://docs.scipy.org/doc/numpy/reference/arrays.dtypes.html
