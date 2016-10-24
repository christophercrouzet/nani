#                      __
#   .-----.---.-.-----|__|
#   |     |  _  |     |  |
#   |__|__|___._|__|__|__|
#

"""
    nani
    ~~~~

    An alternative approach to defining and viewing NumPy's arrays.

    :copyright: Copyright 2016 by Christopher Crouzet.
    :license: MIT, see LICENSE for details.
"""

import collections
import copy
import functools
import numbers
import sys
import types

import numpy


__version__ = '0.1.1'


_PY2 = sys.version_info[0] == 2


if _PY2:
    _CLASS_TYPES = (type, types.ClassType)
    _STRING_TYPES = (basestring,)
    _BuiltinString = str
    _BuiltinUnicode = unicode
    _BUILTIN_MODULE = '__builtin__'
else:
    _CLASS_TYPES = (type,)
    _STRING_TYPES = (str,)
    _BuiltinString = bytes
    _BuiltinUnicode = str
    _BUILTIN_MODULE = 'builtins'

_NUMBER_TYPES = (numbers.Number, numpy.number)
_SHAPE_TYPES = (int, tuple)
_SEQUENCE_TYPES = (list, tuple)


_Bool = collections.namedtuple(
    '_Bool', (
        'default',
        'view',
    )
)
_Bool.__new__.__defaults__ = (False, None)


class Bool(_Bool):

    """Type corresponding to ``numpy.bool_``.

        Parameters
        ----------
        default : bool, optional
            Default value.
        view : type or None, optional
            If None, the owning array returns a direct reference to this
            boolean value, otherwise it is expected to be a class object
            wrapping it and accepting 2 parameters: ``data``, the NumPy array
            owning the boolean value, and ``index``, its position in the array.
    """

    __slots__ = ()


_Object = collections.namedtuple(
    '_Object', (
        'default',
        'view',
    )
)
_Object.__new__.__defaults__ = (None, None)


class Object(_Object):

    """Type corresponding to ``numpy.object_``.

        Parameters
        ----------
        default : object, optional
            Default value.
        view : type or None, optional
            If None, the owning array returns a direct reference to this
            Python object, otherwise it is expected to be a class object
            wrapping it and accepting 2 parameters: ``data``, the NumPy array
            owning the Python object, and ``index``, its position in the array.
    """

    __slots__ = ()


_Number = collections.namedtuple(
    '_Number', (
        'type',
        'default',
        'view',
    )
)
_Number.__new__.__defaults__ = (numpy.float_, 0, None)


class Number(_Number):

    """Type corresponding to ``numpy.number``.

        Parameters
        ----------
        default : numpy.number type, optional
            Default value.
        view : type or None, optional
            If None, the owning array returns a direct reference to this
            numeric value, otherwise it is expected to be a class object
            wrapping it and accepting 2 parameters: ``data``, the NumPy array
            owning the numeric value, and ``index``, its position in the array.
    """

    __slots__ = ()


_String = collections.namedtuple(
    '_String', (
        'length',
        'default',
        'view',
    )
)
_String.__new__.__defaults__ = (_BuiltinString(), None)


class String(_String):

    """Type corresponding to ``numpy.string_``.

        Parameters
        ----------
        length : int
            Number of characters.
        default : str on PY2 or bytes on PY3, optional
            Default value.
        view : type or None, optional
            If None, the owning array returns a direct reference to this
            string value, otherwise it is expected to be a class object
            wrapping it and accepting 2 parameters: ``data``, the NumPy array
            owning the string value, and ``index``, its position in the array.
    """

    __slots__ = ()


_Unicode = collections.namedtuple(
    '_Unicode', (
        'length',
        'default',
        'view',
    )
)
_Unicode.__new__.__defaults__ = (_BuiltinUnicode(), None)


class Unicode(_Unicode):

    """Type corresponding to ``numpy.unicode_``.

        Parameters
        ----------
        length : int
            Number of characters.
        default : unicode on PY2 or str on PY3, optional
            Default value.
        view : type or None, optional
            If None, the owning array returns a direct reference to this
            unicode value, otherwise it is expected to be a class object
            wrapping it and accepting 2 parameters: ``data``, the NumPy array
            owning the unicode value, and ``index``, its position in the array.
    """

    __slots__ = ()


_Array = collections.namedtuple(
    '_Array', (
        'element_type',
        'shape',
        'name',
        'view',
    )
)
_Array.__new__.__defaults__ = (None, None)


class Array(_Array):

    """Type corresponding to a NumPy array.

        Parameters
        ----------
        element_type : nani type
            Type of each element.
        shape : int or tuple of int
            Shape of the array. Passing an int defines a 1D array.
        name : str or None, optional
            Name for the view type if `view` is None.
        view : type or None, optional
            If None, a view for this array is dynamically generated by Nani,
            otherwise it is expected to be a class object wrapping it and
            accepting 1 parameter: ``data``, the corresponding NumPy array.
    """

    __slots__ = ()


_Structure = collections.namedtuple(
    '_Structure', (
        'fields',
        'name',
        'view',
    )
)
_Structure.__new__.__defaults__ = (None, None)


class Structure(_Structure):

    """Type corresponding to a NumPy structured array.

        Parameters
        ----------
        fields : tuple of nani.Field or compatible tuple
            Fields defining the structure.
        name : str or None, optional
            Name for the view type if `view` is None.
        view : type or None, optional
            If None, a view for this structured array is dynamically generated
            by Nani, otherwise it is expected to be a class object wrapping it
            and accepting 1 parameter: ``data``, the corresponding NumPy
            structured array.
    """

    __slots__ = ()


# Aliases.
Bytes = String
if _PY2:
    Str = String
else:
    Str = Unicode


_PREDEFINED_ATOMIC_NUMPY_TYPES = {
    Bool: numpy.bool_,
    Object: numpy.object_,
    String: numpy.string_,
    Unicode: numpy.unicode_,
}
_FIXED_ATOMIC = (Bool, Object, Number)
_FLEXIBLE_ATOMIC = (String, Unicode)
_ATOMIC = _FIXED_ATOMIC + _FLEXIBLE_ATOMIC
_ALL = _ATOMIC + (Array, Structure)
_TYPE_COUNT = len(_ALL)

assert(all(hasattr(type_, 'type') or type_ in _PREDEFINED_ATOMIC_NUMPY_TYPES
           for type_ in _ATOMIC))


_Field = collections.namedtuple(
    '_Field', (
        'name',
        'type',
        'read_only',
    )
)
_Field.__new__.__defaults__ = (False,)


class Field(_Field):

    """Describe a field of a structured array.

    Parameters
    ----------
    name : str
        Name of the field.
    type : nani data type
        Type of the field.
    read_only : bool
        True to not define a setter property in the structured array view if it
        is set to be dynamically generated by Nani.
    """

    __slots__ = ()


#: Constant to use for the ``read_only`` attribute of a `~nani.Field`.
#: To use for readability reasons when the ``read_only`` keyword is not
#: explicitely written.
READ_ONLY = True


_FIELD_NAME = Field._fields.index('name')
_FIELD_TYPE = Field._fields.index('type')
_FIELD_ATTRIBUTE_COUNT = len(Field._fields)
_FIELD_EXPECTED_ARGUMENT_COUNTS = range(
    _FIELD_ATTRIBUTE_COUNT - len(Field.__new__.__defaults__),
    _FIELD_ATTRIBUTE_COUNT + 1
)


_FieldInstanceCheck = collections.namedtuple(
    '_FieldInstanceCheck', (
        'name',
        'type',
        'allow_none',
    )
)
_FieldInstanceCheck.__new__.__defaults__ = (False,)


_FieldSubclassCheck = collections.namedtuple(
    '_FieldSubclassCheck', (
        'name',
        'type',
        'allow_none',
    )
)
_FieldSubclassCheck.__new__.__defaults__ = (False,)


_TYPE_ATTRIBUTE_CHECKS = {
    Bool: (
        _FieldInstanceCheck(name='default', type=bool),
        _FieldSubclassCheck(name='view', type=object, allow_none=True),
    ),
    Object: (
        _FieldInstanceCheck(name='default', type=object, allow_none=True),
        _FieldSubclassCheck(name='view', type=object, allow_none=True),
    ),
    Number: (
        _FieldSubclassCheck(name='type', type=_NUMBER_TYPES),
        _FieldInstanceCheck(name='default', type=_NUMBER_TYPES),
        _FieldSubclassCheck(name='view', type=object, allow_none=True),
    ),
    String: (
        _FieldInstanceCheck(name='length', type=int),
        _FieldInstanceCheck(name='default', type=_BuiltinString),
        _FieldSubclassCheck(name='view', type=object, allow_none=True),
    ),
    Unicode: (
        _FieldInstanceCheck(name='length', type=int),
        _FieldInstanceCheck(name='default', type=_BuiltinUnicode),
        _FieldSubclassCheck(name='view', type=object, allow_none=True),
    ),
    Array: (
        _FieldInstanceCheck(name='element_type', type=_ALL),
        _FieldInstanceCheck(name='shape', type=_SHAPE_TYPES),
        _FieldInstanceCheck(name='name', type=_STRING_TYPES, allow_none=True),
        _FieldSubclassCheck(name='view', type=object, allow_none=True),
    ),
    Structure: (
        _FieldInstanceCheck(name='fields', type=_SEQUENCE_TYPES),
        _FieldInstanceCheck(name='name', type=_STRING_TYPES, allow_none=True),
        _FieldSubclassCheck(name='view', type=object, allow_none=True),
    ),
}
_MIXIN_ATTRIBUTES = {}


class _DirectArrayViewMixin(object):

    """Mixin for array views with no element view provided.

    Element are directly accessed and set.
    """

    __slots__ = ('_data',)

    def __init__(self, data):
        self._data = data

    def __str__(self):
        return "[{0}]".format(', '.join(str(item) for item in self._data))

    def __getitem__(self, index):
        return self._data[index]

    def __setitem__(self, index, value):
        self._data[index] = value

    def __iter__(self):
        return iter(self._data)

    def __len__(self):
        return self._data.__len__()

    def __contains__(self, item):
        return item in self._data


_MIXIN_ATTRIBUTES[_DirectArrayViewMixin] = (
    '__slots__',
    '__init__',
    '__str__',
    '__getitem__',
    '__setitem__',
    '__iter__',
    '__len__',
    '__contains__',
)


class _IndirectAtomicArrayViewMixin(object):

    """Mixin for atomic array views with an element view provided.

    Atomic elements are not directly accessed and set. Instead they are first
    wrapped into the element view type then returned.
    """

    __slots__ = ('_data',)

    def __init__(self, data):
        self._data = data

    def __str__(self):
        return "[{0}]".format(', '.join(str(self._element_view(self._data, i))
                                        for i in range(len(self._data))))

    def __getitem__(self, index):
        return self._element_view(self._data, index)

    def __setitem__(self, index, value):
        self._data[index] = value

    def __iter__(self):
        return (self._element_view(self._data, i)
                for i in range(len(self._data)))

    def __len__(self):
        return len(self._data)

    def __contains__(self, item):
        return item in self._data


_MIXIN_ATTRIBUTES[_IndirectAtomicArrayViewMixin] = (
    '__slots__',
    '__init__',
    '__str__',
    '__getitem__',
    '__setitem__',
    '__iter__',
    '__len__',
    '__contains__',
)


class _IndirectCompositeArrayViewMixin(object):

    """Mixin for composite array views with an element view provided.

    Composite elements are first wrapped into the element view type then
    returned.

    The element views are to be initialized with a single parameter:

        - data: a view to the NumPy array representing the element.
    """

    __slots__ = ('_data',)

    def __init__(self, data):
        self._data = data

    def __str__(self):
        return "[{0}]".format(', '.join(str(self._element_view(item))
                                        for item in self._data))

    def __getitem__(self, index):
        return self._element_view(self._data[index])

    def __setitem__(self, index, value):
        self._data[index] = value

    def __iter__(self):
        return (self._element_view(item) for item in self._data)

    def __len__(self):
        return self._data.__len__()

    def __contains__(self, item):
        return self._data.__contains__(self, item)


_MIXIN_ATTRIBUTES[_IndirectCompositeArrayViewMixin] = (
    '__slots__',
    '__init__',
    '__str__',
    '__getitem__',
    '__setitem__',
    '__iter__',
    '__len__',
    '__contains__',
)


class _StructuredViewMixin(object):

    """Mixin for structured array views.

    Properties are to be dynamically generated for each field.
    """
    __slots__ = ('_data',)

    def __init__(self, data):
        self._data = data

    def __str__(self):
        fields_and_values = (
            "{0}={1}".format(field, getattr(self, field))
            for field in self._fields
        )
        return "{0}({1})".format(type(self).__name__,
                                 ', '.join(fields_and_values))


_MIXIN_ATTRIBUTES[_StructuredViewMixin] = (
    '__slots__',
    '__init__',
    '__str__',
)


_Nani = collections.namedtuple(
    '_Nani', (
        'dtype',
        'default',
        'view',
    )
)


class Nani(_Nani):

    """Output structure from the function `~nani.resolve`.

    Parameters
    ----------
    dtype : numpy.dtype
        NumPy's ``dtype``, that is the data type of the array elements.
    default : object
        Default value(s) for a single array element.
    view : type
        A class to use as a wrapper around the NumPy array.
    """

    __slots__ = ()


def resolve(data_type, name=None, listify_default=False, check=True):
    """Retrieve the properties for a given data type.

    This is the main routine where most of the work is done. It converts
    Nani's data types into properties that can be used to define a new NumPy
    array and to wrap it into a view object.

    Parameters
    ----------
    data_type : nani data type
        Type of the array elements.
    name : str, optional
        Name for the view to be generated for the array.
    listify_default : bool, optional
        True to output the default values with lists in place of tuples.
        This might cause the output to be incompatible with array creation
        routines such as ``numpy.array`` but it should still work for
        element assignment.
    check : bool, optional
        False to not check if ``data_type`` is well formed.

    Returns
    -------
    nani.Nani
        The properties to use to initalize a NumPy array around the data type.

    Examples
    --------
    Create a NumPy array where each element represents a color:

    >>> import numpy
    >>> import nani
    >>> color_type = nani.Array(
    ...     element_type=nani.Number(type=numpy.uint8, default=255),
    ...     shape=3,
    ...     view=None
    ... )
    >>> dtype, default, view = nani.resolve(color_type, name='Color')
    >>> a = numpy.array([default] * element_count, dtype=dtype)
    >>> v = view(a)
    >>> type(v)
    <class 'nani.Color'>
    >>> for color in v:
    ...     color
    [255, 255, 255]
    [255, 255, 255]
    """
    if check:
        _check_data_type(data_type, '')

    data_type = _consolidate(data_type)
    return Nani(
        dtype=numpy.dtype(_resolve_dtype(data_type)),
        default=_resolve_default(data_type, listify=listify_default),
        view=_resolve_view(Array(element_type=data_type, shape=-1, name=name))
    )


def update(data_type, **kwargs):
    """Update a data type with different values.

    The operation is not made in place, instead a copy is returned.

    Parameters
    ----------
    data_type : nani data type
        Data type.
    kwargs
        Keyword arguments to update.

    Returns
    -------
    nani data type
        The updated version of the data type.

    Examples
    --------
    Update the shape of an array data type and the default value of its
    elements:

    >>> import nani
    >>> data_type = nani.Array(
    ...     element_type=nani.Number(),
    ...     shape=2
    ... )
    >>> new_data_type = nani.update(
    ...     data_type,
    ...     element_type=nani.update(data_type.element_type, default=123),
    ...     shape=3
    ... )
    """
    return data_type._replace(**kwargs)


def get_data(view):
    """Retrieve the NumPy data from an array view generated by Nani.

    Parameters
    ----------
    view : nani.AtomicArrayView or nani.CompositeArrayView
        Array view.

    Returns
    -------
    type
        The NumPy array, None otherwise.

    Examples
    --------
    >>> import numpy
    >>> import nani
    >>> data_type = nani.Number(type=numpy.int32)
    >>> dtype, _, view = nani.resolve(data_type)
    >>> a = numpy.arange(10, dtype=dtype)
    >>> v = view(a)
    >>> nani.get_data(v) is a
    True
    """
    return getattr(view, '_data', None)


def get_element_view(view):
    """Retrieve the element view from an array view generated by Nani.

    Parameters
    ----------
    view : nani.AtomicArrayView or nani.CompositeArrayView
        Array view.

    Returns
    -------
    type
        The element view, None otherwise.

    Examples
    --------
    >>> import numpy
    >>> import nani
    >>> vector2_type = nani.Array(
    ...     element_type=nani.Number(),
    ...     shape=2,
    ...     name='Vector2'
    ... )
    >>> dtype, default, view = nani.resolve(vector2_type, name='Positions')
    >>> a = numpy.zeros(3, dtype=dtype)
    >>> v = view(a)
    >>> type(v)
    <class 'nani.Positions'>
    >>> nani.get_element_view(v)
    <class 'nani.Vector2'>
    """
    return getattr(view, '_element_view', None)


def _check_data_type(data_type, parent_path):
    """Check if the data type is well-formed.

    Parameters
    ----------
    data_type : nani data type
        Data type.
    parent_path : str
        Parent path in the form of a dotted path.

    Raises
    ------
    TypeError
        The data type isn't well-formed.
    """
    # The following checks are not to enforce some sort of type checking
    # in place of Python's duck typing but rather to give a chance to provide
    # more meaningful error messages to the user.

    def find_duplicate_fields(fields):
        field_names = [field[_FIELD_NAME] for field in fields]
        return [item for item in field_names if field_names.count(item) > 1]

    if isinstance(data_type, _CLASS_TYPES):
        if parent_path:
            raise TypeError(
                "The data type for '{0}' is expected to be an instance "
                "object but got the type {1} instead."
                .format(parent_path, _join_types(data_type))
            )
        else:
            raise TypeError(
                "The data type is expected to be an instance object but got "
                "the type {0} instead."
                .format(_join_types(data_type))
            )

    base = _find_base_type(data_type)
    if not base:
        raise TypeError(
            "Objects of type {0} aren't supported as data types. Use any "
            "type from {1} instead."
            .format(_join_types(type(data_type)), _join_types(_ALL, "or "))
        )

    name = getattr(data_type, 'name', None)
    if not name:
        name = type(data_type).__name__

    full_path = '{0}.{1}'.format(parent_path, name) if parent_path else name

    # Generic checks for each attribute.
    for check in _TYPE_ATTRIBUTE_CHECKS[base]:
        attribute = getattr(data_type, check.name)
        if attribute is None:
            if check.allow_none:
                continue
            else:
                raise TypeError(
                    "The attribute '{0}.{1}' cannot be 'None'."
                    .format(full_path, check.name)
                )

        if isinstance(check, _FieldInstanceCheck):
            check_function = isinstance
        elif isinstance(check, _FieldSubclassCheck):
            if not isinstance(attribute, _CLASS_TYPES):
                raise TypeError(
                    "The attribute '{0}.{1}' is expected to be a class "
                    "object{2}."
                    .format(full_path, check.name,
                            " or 'None'" if check.allow_none else '')
                )

            check_function = issubclass

        if not check_function(attribute, check.type):
            if isinstance(check, _FieldInstanceCheck):
                glue = "an instance object of type"
                type_name = _join_types(type(attribute))
            elif isinstance(check, _FieldSubclassCheck):
                glue = "a subclass of"
                type_name = _join_types(attribute)

            raise TypeError(
                "The attribute '{0}.{1}' is expected to be {2} {3}, "
                "not {4}."
                .format(full_path, check.name, glue,
                        _join_types(check.type, "or "), type_name)
            )

    # Additional and/or recursive checks for specific attributes.
    if isinstance(data_type, Array):
        _check_data_type(data_type.element_type, full_path)
    elif isinstance(data_type, Structure):
        for field in data_type.fields:
            if not isinstance(field, tuple):
                raise TypeError(
                    "Each field from the attribute '{0}.fields' is expected "
                    "to be a tuple but got {1} instead."
                    .format(full_path, _join_types(type(field)))
                )

            if len(field) not in _FIELD_EXPECTED_ARGUMENT_COUNTS:
                raise TypeError(
                    "Each field from the attribute '{0}.fields' is expected "
                    "to be a tuple compatible with {1} but got '{2}' instead."
                    .format(full_path, _join_types(Field), field)
                )

            field = Field(*field)
            if not isinstance(field.name, _STRING_TYPES):
                raise TypeError(
                    "The first element of each field from the attribute "
                    "'{0}.fields', that is the field name, is expected "
                    "to be an instance object of type {1}, not {2}."
                    .format(full_path, _join_types(_STRING_TYPES, "or "),
                            _join_types(type(field.name)))
                )

            if not isinstance(field.type, _ALL):
                raise TypeError(
                    "The second element of each field from the attribute "
                    "'{0}.fields', that is the field type, is expected "
                    "to be an instance object of type {1}, not {2}."
                    .format(full_path, _join_types(_ALL, "or "),
                            _join_types(type(field.type)))
                )

            if not isinstance(field.read_only, bool):
                raise TypeError(
                    "The third element of each field from the attribute "
                    "'{0}.fields', that is the 'read_only' attribute, is "
                    "expected to be an instance object of type 'bool', "
                    "not {1}."
                    .format(full_path, _join_types(type(field.read_only)))
                )

            field_path = '{0}.{1}'.format(full_path, field.name)
            _check_data_type(field.type, field_path)

        duplicates = find_duplicate_fields(data_type.fields)
        if duplicates:
            if len(duplicates) > 1:
                raise ValueError(
                    "The structure fields {0}, were provided multiple times."
                    .format(_join_sequence(duplicates, "and "))
                )
            else:
                raise ValueError(
                    "The structure field '{0}' was provided multiple times."
                    .format(duplicates[0])
                )


def _consolidate(data_type):
    """Enforce the structure of the data type.

    Specifically, ensure that if a field is defined as a generic tuple, then it
    will be converted into an instance of ``nani.Field``.

    Parameters
    ----------
    data_type : nani data type
        Data type.

    Returns
    -------
    nani data type
        The consolidated data type.
    """
    def get_field_item(field, i):
        if i < len(field):
            return field[i]
        else:
            return Field.__new__.__defaults__[i - _FIELD_ATTRIBUTE_COUNT]

    if isinstance(data_type, _ATOMIC):
        out = data_type
    elif isinstance(data_type, Array):
        out = data_type._replace(
            element_type=_consolidate(data_type.element_type)
        )
    elif isinstance(data_type, Structure):
        out = data_type._replace(
            fields=tuple(Field(
                *(_consolidate(get_field_item(field, i))
                  if i == _FIELD_TYPE else get_field_item(field, i)
                  for i in range(_FIELD_ATTRIBUTE_COUNT))
            ) for field in data_type.fields)
        )

    return out


def _resolve_dtype(data_type):
    """Retrieve the corresponding NumPy's ``dtype`` for a given data type.

    Parameters
    ----------
    data_type : nani data type
        Data type.

    Returns
    -------
    numpy.dtype
        The corresponding NumPy's ``dtype``.
    """
    if isinstance(data_type, _FIXED_ATOMIC):
        out = _get_atomic_dtype(data_type)
    elif isinstance(data_type, _FLEXIBLE_ATOMIC):
        out = (_get_atomic_dtype(data_type), data_type.length)
    elif isinstance(data_type, Array):
        shape = data_type.shape
        if isinstance(shape, tuple) and len(shape) == 1:
            # Workaround the exception `ValueError: invalid itemsize in
            # generic type tuple` when an `Array` of shape 0 or (0,) is nested
            # within another `Array`.
            shape = shape[0]

        out = (_resolve_dtype(data_type.element_type), shape)
    elif isinstance(data_type, Structure):
        out = [(field.name, _resolve_dtype(field.type))
               for field in data_type.fields]

    return out


def _resolve_default(data_type, listify=False):
    """Retrieve the view for a given data type.

    Only one view class will be returned, that is the one representing the root
    data type, but more class objects might be dynamically defined if the input
    data type has nested elements, such as for the ``nani.Array`` and
    ``nani.Structure`` types.

    The default behaviour of dynamically and recursively creating a new view
    class can be overriden by setting the ``view`` attribute of a data type.

    Parameters
    ----------
    data_type : nani data type
        Data type.
    listify : bool, optional
        True to output lists in place of tuples. This might cause the output
        to be incompatible with ``numpy.array``.

    Returns
    -------
    object
        The default value.
    """
    if isinstance(data_type, _ATOMIC):
        # A Python's object type needs to be left as is instead of being
        # wrapped into a NumPy type.
        out = (data_type.default if isinstance(data_type, Object)
               else _get_atomic_dtype(data_type)(data_type.default))
    elif isinstance(data_type, Array):
        element_default = _resolve_default(data_type.element_type,
                                           listify=listify)
        Sequence = list if listify else tuple
        shape = ((data_type.shape,) if isinstance(data_type.shape, int)
                 else data_type.shape)
        out = functools.reduce(
            lambda default, length: Sequence(copy.deepcopy(default)
                                             for _ in range(length)),
            shape,
            element_default
        )
    elif isinstance(data_type, Structure):
        if listify:
            out = [_resolve_default(field.type, listify=listify)
                   for field in data_type.fields]
        else:
            field_defaults = collections.OrderedDict(
                (field.name, _resolve_default(field.type, listify=listify))
                for field in data_type.fields
            )
            name = ('StructureDefault_{0}'.format(data_type.name)
                    if data_type.name else 'StructureDefault')
            struct = collections.namedtuple(name, field_defaults.keys())
            out = struct(**field_defaults)

    return out


def _resolve_view(data_type):
    """Actual implementation of the ``resolve_view`` function.

    Parameters
    ----------
    data_type : nani data type
        Data type.

    Returns
    -------
    object
        The view.
    """
    view = getattr(data_type, 'view', None)
    if view is not None:
        return view

    if isinstance(data_type, _ATOMIC):
        out = None
    elif isinstance(data_type, Array):
        out = _define_array_view(data_type)
    elif isinstance(data_type, Structure):
        out = _define_structure_view(data_type)

    return out


def _define_array_view(data_type):
    """Define a new view object for a ``nani.Array`` type.

    Parameters
    ----------
    data_type : nani.Array
        Data type.

    Returns
    -------
    object
        The new array view.
    """
    element_type = data_type.element_type
    element_view = _resolve_view(element_type)
    if element_view is None:
        mixins = (_DirectArrayViewMixin,)
        attributes = _get_mixin_attributes(mixins)
    elif isinstance(element_type, _ATOMIC):
        mixins = (_IndirectAtomicArrayViewMixin,)
        attributes = _get_mixin_attributes(mixins)
        attributes.update({
            '_element_view': element_view
        })
    else:
        mixins = (_IndirectCompositeArrayViewMixin,)
        attributes = _get_mixin_attributes(mixins)
        attributes.update({
            '_element_view': element_view
        })

    name = data_type.name if data_type.name else 'ArrayView'
    return type(name, (), attributes)


def _define_structure_view(data_type):
    """Define a new view object for a ``nani.Structure`` type.

    Parameters
    ----------
    data_type : nani.Structure
        Data type.

    Returns
    -------
    object
        The new structure view.
    """
    def _define_getter(field_index, field_type, field_view):
        if field_view is None:
            def getter(self):
                return self._data[field_index]
        elif isinstance(field_type, _ATOMIC):
            def getter(self):
                return field_view(self._data, field_index)
        else:
            def getter(self):
                return field_view(self._data[field_index])

        return getter

    def _define_setter(field_index, read_only):
        def setter(self, value):
            self._data[field_index] = value

        return None if read_only else setter

    field_views = [_resolve_view(field.type) for field in data_type.fields]
    mixins = (_StructuredViewMixin,)
    attributes = _get_mixin_attributes(mixins)
    attributes.update({
        '_fields': tuple(field.name for field in data_type.fields)
    })
    attributes.update({
        field.name: property(
            fget=_define_getter(i, field.type, field_view),
            fset=_define_setter(i, field.read_only),
            fdel=None
        )
        for i, (field, field_view)
        in enumerate(zip(data_type.fields, field_views))
    })
    name = data_type.name if data_type.name else 'StructureView'
    return type(name, (), attributes)


def _get_mixin_attributes(mixins):
    """Retrieve the attributes for a given set of mixin classes.

    The attributes of each mixin class are being merged into a single
    dictionary.

    Parameters
    ----------
    mixins : iterable
        Mixin classes.

    Returns
    -------
    dict
        A dictionary of attribute's `name: value` pairs.
    """
    return {attribute: mixin.__dict__[attribute]
            for mixin in mixins
            for attribute in _MIXIN_ATTRIBUTES[mixin]}


def _get_atomic_dtype(data_type):
    """Retrieve the NumPy's ``dtype`` for a given atomic data type.

    Parameters
    ----------
    data_type : nani data type
        Data type.

    Returns
    -------
    numpy.dtype
        The corresponding NumPy's ``dtype``.
    """
    atomic_type = getattr(data_type, 'type', None)
    if atomic_type is not None:
        return atomic_type

    return _PREDEFINED_ATOMIC_NUMPY_TYPES[_find_base_type(data_type)]


def _find_base_type(data_type):
    """Find the Nani's base type for a given data type.

    This is useful when Nani's data types were subclassed and the original type
    is required.

    Parameters
    ----------
    data_type : nani data type
        Data type.

    Returns
    -------
    object
        The Nani's base type.
    """
    bases = type(data_type).__mro__
    for base in bases:
        if base in _ALL:
            return base

    return None


def _join_sequence(seq, last_separator=''):
    """Join a sequence into a string.

    Parameters
    ----------
    seq : sequence
        Object string representations to be joined.
    last_separator : str
        Separator to be used for joining the last element when multiple
        elements are to be joined.

    Returns
    -------
    str
        The joined object string representations.
    """
    def _format(item, count, index):
        return ("{0}'{1}'".format(last_separator, item)
                if count > 1 and index == count - 1
                else "'{0}'".format(item))

    if not isinstance(seq, _SEQUENCE_TYPES):
        seq = (seq,)

    count = len(seq)
    return ', '.join(_format(item, count, i) for i, item in enumerate(seq))


def _join_types(seq, last_separator=''):
    """Join class object names into a string.

    Parameters
    ----------
    seq : sequence
        Class objects whose names are to be joined.
    last_separator : str
        Separator to be used for joining the last element when multiple types
        are to be joined.

    Returns
    -------
    str
        The joined class object names.
    """
    if not isinstance(seq, _SEQUENCE_TYPES):
        seq = (seq,)

    class_names = ['{0}.{1}'.format(cls.__module__, cls.__name__)
                   if cls.__module__ != _BUILTIN_MODULE else cls.__name__
                   for cls in seq]
    return _join_sequence(class_names, last_separator)
