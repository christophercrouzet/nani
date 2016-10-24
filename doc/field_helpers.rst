.. _field_helpers:

Field Helpers
=============

.. module:: nani
   :noindex:

.. autosummary::
   :nosignatures:

   Field
   READ_ONLY


Structured arrays are described as a sequence of fields. Each field can be
defined as a :class:`~nani.Field` or as a tuple compatible with the
:class:`~nani.Field` structure.

A constant :data:`~nani.READ_ONLY` equivalent to the boolean value ``True`` is
provided to make the code more readable when setting the
`Field.read_only` attribute without explicitely writing the ``read_only``
keyword. Example:

    >>> import nani
    >>> data_type = nani.Structure(
    ...     fields=(
    ...         ('do_not_touch', nani.Number(), nani.READ_ONLY)
    ...     )
    ... )


.. autoclass:: Field(name, type, read_only=False)
.. autodata:: READ_ONLY
