Nani
====

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


See the ``tutorial`` section from the documentation for more examples.


Documentation
-------------

Read the documentation online at <http://nani.readthedocs.io> or check
their source from the ``doc`` folder.

The documentation can be built in different formats using Sphinx.


Running the Tests
-----------------

A suite of unit tests is available from the ``tests`` directory. You can run it
by firing:

.. code-block:: bash

   $ python tests/run.py


To run specific tests, it is possible to pass names to match in the command
line.

.. code-block:: bash

   $ python tests/run.py TestCase test_my_code


This command will run all the tests within the ``TestCase`` class as well as
the individual tests which contains ``test_my_code`` in their name.


Get the Source
--------------

The source code is available from the `GitHub project page`_.


Contributing
------------

Found a bug or got a feature request? Don't keep it for yourself, log a new
issue on `GitHub <https://github.com/christophercrouzet/nani/issues>`_.


Author
------

Christopher Crouzet
<`christophercrouzet.com <http://christophercrouzet.com>`_>


.. _GitHub project page: https://github.com/christophercrouzet/nani
