.. _data_types:

Data Types
==========

.. module:: nani
   :noindex:


.. autosummary::
   :nosignatures:

   Bool
   Object
   Number
   String
   Unicode
   Array
   Structure
   Bytes
   Str


These are the data types mimicking the `NumPy's scalar hierarchy of types`_ and
allowing to describe `NumPy's dtypes`_ in the Nani format.

They can later on be converted into NumPy's ``dtype``\s by calling the
:func:`~nani.resolve` function.


.. autoclass:: Bool(default=False, view=None)
.. autoclass:: Object(default=None, view=None)
.. autoclass:: Number(type=numpy.float_, default=0, view=None)
.. autoclass:: String(length, default='', view=None)
.. autoclass:: Unicode(length, default='', view=None)
.. autoclass:: Array(element_type, shape, name=None, view=None)
.. autoclass:: Structure(fields, name=None, view=None)


.. class:: Bytes(length, default='', view=None)

   Alias for `~nani.String`.


.. class:: Str(length, default='', view=None)

   Alias for `~nani.String` on PY2 or `~nani.Unicode` on PY3.


.. _NumPy's scalar hierarchy of types:
   https://docs.scipy.org/doc/numpy/reference/arrays.scalars.html
.. _NumPy's dtypes:
   https://docs.scipy.org/doc/numpy/reference/arrays.dtypes.html