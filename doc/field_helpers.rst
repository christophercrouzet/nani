.. currentmodule:: nani

.. _field_helpers:

Field Helpers
=============

Structured arrays are described as a sequence of fields. Each field can be
defined as a :class:`Field` or as a tuple compatible with the :class:`Field`
structure.

A constant :data:`READ_ONLY` equivalent to the boolean value ``True`` is
provided to make the code more readable when setting the
:attr:`Field.read_only` attribute without explicitely writing the ``read_only``
keyword. Example:

.. code-block:: python

   >>> import nani
   >>> data_type = nani.Structure(
   ...     fields=(
   ...         ('do_not_touch', nani.Number(), nani.READ_ONLY),
   ...     )
   ... )


.. autosummary::
   :nosignatures:

   Field
   READ_ONLY


----

.. autoclass:: Field(name, type, read_only=False)

----

.. autodata:: READ_ONLY
