Nani
====

.. image:: https://img.shields.io/travis/christophercrouzet/nani/master.svg
   :target: https://travis-ci.org/christophercrouzet/nani
   :alt: Build status

.. image:: https://img.shields.io/coveralls/christophercrouzet/nani/master.svg
   :target: https://coveralls.io/r/christophercrouzet/nani
   :alt: Coverage Status

.. image:: https://img.shields.io/pypi/v/nani.svg
   :target: https://pypi.python.org/pypi/nani
   :alt: PyPI latest version

.. image:: https://readthedocs.org/projects/nani/badge/?version=latest
   :target: https://nani.readthedocs.io
   :alt: Documentation status

.. image:: https://img.shields.io/pypi/l/nani.svg
   :target: https://pypi.python.org/pypi/nani
   :alt: License


Nani is a Python library that provides an alternative approach to defining and
viewing `NumPy`_'s arrays.

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


See the `Tutorial`_ section from the documentation for more detailed examples
and explanations on how to use Nani.


Documentation
-------------

Read the documentation online at `nani.readthedocs.io`_ or check its source in
the ``doc`` directory.


Out There
---------

Projects using Nani include:

* `hienoi <https://github.com/christophercrouzet/hienoi>`_


Author
------

Christopher Crouzet
<`christophercrouzet.com <https://christophercrouzet.com>`_>


.. |numpy.dtype| replace:: ``numpy.dtype``

.. _nani.readthedocs.io: https://nani.readthedocs.io
.. _NumPy: http://www.numpy.org
.. _numpy.dtype: https://docs.scipy.org/doc/numpy/reference/arrays.dtypes.html
.. _Tutorial: https://nani.readthedocs.io/en/latest/tutorial.html
