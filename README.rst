Nani
====

An alternative approach to defining and viewing NumPy's arrays.

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


See the ``overview`` and ``tutorial`` sections from the documentation for more
information.


Documentation
-------------

Read the documentation online at <http://nani.readthedocs.org> or check
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
