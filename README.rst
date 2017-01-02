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


Nani is a library that provides an alternative approach to defining and viewing
NumPy's arrays.

It offers an explicit syntax to construct NumPy's ``dtype``\s which tends to
make the code more verbose to write but easier to read and to reason about,
while being less error prone.

.. code-block:: python

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

.. code-block:: python

   >>> dtype, default, view = nani.resolve(color_type, name='Color')


If no custom views are specified, Nani dynamically generates them according to
the data types described.


Features
--------

* explicit and consistent syntax to define NumPy ``dtype``\s.
* additional properties to generate default values and view types for arrays.
* compatible with both Python 2 and Python 3.


Usage
-----

.. code-block:: python

   >>> import numpy
   >>> import nani
   >>> color_type = nani.Array(
   ...     element_type=nani.Number(type=numpy.uint8, default=255),
   ...     shape=3,
   ...     view=None
   ... )
   >>> dtype, default, view = nani.resolve(color_type, name='Color')
   >>> element_count = 2
   >>> a = numpy.array([default] * element_count, dtype=dtype)
   >>> v = view(a)
   >>> type(v)
   <class 'nani.Color'>
   >>> for color in v:
   ...     color
   [255, 255, 255]
   [255, 255, 255]


See the `Tutorial`_ section from the documentation for more information and
examples on using Nani.


Installation
------------

See the `Installation`_ section from the documentation.


Documentation
-------------

Read the documentation online at <https://nani.readthedocs.io> or check its
source in the ``doc`` directory.


Running the Tests
-----------------

Tests are available in the ``tests`` directory and can be fired through the
``run.py`` file:

.. code-block:: bash

   $ python tests/run.py


It is also possible to run specific tests by passing a space-separated list of
partial names to match:

.. code-block:: bash

   $ python tests/run.py TestClass


Finally, each test file is standalone and can be directly executed.


Author
------

Christopher Crouzet
<`christophercrouzet.com <https://christophercrouzet.com>`_>


.. _Tutorial: https://nani.readthedocs.io/en/latest/tutorial.html
.. _Installation: https://nani.readthedocs.io/en/latest/installation.html
