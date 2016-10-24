.. _overview:

Overview
========

Nani is a library that provides an alternative approach to defining and viewing
NumPy's arrays.

It offers an explicit syntax to construct NumPy's ``dtype``\s which tends to
make the code more verbose to write but easier to read and to reason about,
while being less error prone.

    >>> import numpy
    >>> import nani
    >>> color_type = nani.Array(
    ...     element_type=nani.Number(type=numpy.uint8, default=255),
    ...     shape=3,
    ...     view=None
    ... )


This syntax also brings additional features such as **default values** and 
**view types**. Default values facilitate the definition of new array elements
while view types provide an abstraction layer built around NumPy's arrays,
giving control over the public interface exposed to the end users.

   >>> dtype, default, view = nani.resolve(color_type, name='Color')


If no custom views are specified, Nani dynamically generates them according to
the data types described.


.. seealso::

   A description of the usage of Nani as well as a few examples are available
   in the :ref:`tutorial` section.
