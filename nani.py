#                      __
#   .-----.---.-.-----|__|
#   |     |  _  |     |  |
#   |__|__|___._|__|__|__|
#

"""Alternative approach to defining and viewing NumPy's arrays."""

__all__ = ['Bool', 'Object', 'Number', 'String', 'Unicode', 'Array',
           'Structure', 'Bytes', 'Str', 'Field', 'READ_ONLY', 'Nani',
           'validate', 'resolve', 'update', 'get_data', 'get_element_view']

__title__ = 'nani'
__version__ = '0.2.0'
__summary__ = "Alternative approach to defining and viewing NumPy's arrays"
__url__ = 'https://github.com/christophercrouzet/nani'
__author__ = "Christopher Crouzet"
__contact__ = 'christopher.crouzet@gmail.com'
__license__ = "MIT"

import collections
import copy
import numbers
import sys
import types

import numpy


_PY2 = sys.version_info[0] == 2


if _PY2:
    _CLASS_TYPES = (type, types.ClassType)
    _STRING_TYPES = (basestring,)
    _BuiltinString = str
    _BuiltinUnicode = unicode
    _BUILTIN_MODULE = '__builtin__'

    _range = xrange
else:
    _CLASS_TYPES = (type,)
    _STRING_TYPES = (str,)
    _BuiltinString = bytes
    _BuiltinUnicode = str
    _BUILTIN_MODULE = 'builtins'

    _range = range

_NUMBER_TYPES = (numbers.Number, numpy.number)
_SEQUENCE_TYPES = (list, tuple)


_Bool = collections.namedtuple(
    'Bool', (
        'default',
        'view',
    ))
_Bool.__new__.__defaults__ = (False, None)


class Bool(_Bool):
    """Type corresponding to ``numpy.bool_``.

    Attributes
    ----------
    default : bool
        Default value.
    view : type or None
        If ``None``, the owning array returns a direct reference to this
        boolean value, otherwise it is expected to be a class object wrapping
        it and accepting 2 parameters: ``data``, the NumPy array owning the
        boolean value, and ``index``, its position in the array.
    """

    __slots__ = ()


_Object = collections.namedtuple(
    'Object', (
        'default',
        'view',
    ))
_Object.__new__.__defaults__ = (None, None)


class Object(_Object):
    """Type corresponding to ``numpy.object_``.

    Attributes
    ----------
    default : object
        Default value.
    view : type or None
        If ``None``, the owning array returns a direct reference to this Python
        object, otherwise it is expected to be a class object wrapping it and
        accepting 2 parameters: ``data``, the NumPy array owning the Python
        object, and ``index``, its position in the array.
    """

    __slots__ = ()


_Number = collections.namedtuple(
    'Number', (
        'type',
        'default',
        'view',
    ))
_Number.__new__.__defaults__ = (numpy.float_, 0, None)


class Number(_Number):
    """Type corresponding to ``numpy.number``.

    Attributes
    ----------
    type : type
        Type of the number. Either one inheriting from ``numbers.Number`` or
        ``numpy.number``.
    default : numbers.Number or numpy.number
        Default value.
    view : type or None
        If ``None``, the owning array returns a direct reference to this
        numeric value, otherwise it is expected to be a class object wrapping
        it and accepting 2 parameters: ``data``, the NumPy array owning the
        numeric value, and ``index``, its position in the array.
    """

    __slots__ = ()


_String = collections.namedtuple(
    'String', (
        'length',
        'default',
        'view',
    ))
_String.__new__.__defaults__ = (_BuiltinString(), None)


class String(_String):
    """Type corresponding to ``numpy.string_``.

    Attributes
    ----------
    length : int
        Number of characters.
    default : str on PY2 or bytes on PY3
        Default value.
    view : type or None
        If ``None``, the owning array returns a direct reference to this string
        value, otherwise it is expected to be a class object wrapping it and
        accepting 2 parameters: ``data``, the NumPy array owning the string
        value, and ``index``, its position in the array.
    """

    __slots__ = ()


_Unicode = collections.namedtuple(
    'Unicode', (
        'length',
        'default',
        'view',
    ))
_Unicode.__new__.__defaults__ = (_BuiltinUnicode(), None)


class Unicode(_Unicode):
    """Type corresponding to ``numpy.unicode_``.

    Attributes
    ----------
    length : int
        Number of characters.
    default : unicode on PY2 or str on PY3
        Default value.
    view : type or None
        If ``None``, the owning array returns a direct reference to this
        unicode value, otherwise it is expected to be a class object wrapping
        it and accepting 2 parameters: ``data``, the NumPy array owning the
        unicode value, and ``index``, its position in the array.
    """

    __slots__ = ()


_Array = collections.namedtuple(
    'Array', (
        'element_type',
        'shape',
        'name',
        'view',
    ))
_Array.__new__.__defaults__ = (None, None)


class Array(_Array):
    """Type corresponding to a NumPy (sub)array.

    Attributes
    ----------
    element_type : nani type
        Type of each element.
    shape : int or tuple of int
        Shape of the array. Passing an int defines a 1D array.
    name : str or None
        Name for the view type if `view` is ``None``.
    view : type or None
        If ``None``, a view for this array is dynamically generated by Nani,
        otherwise it is expected to be a class object wrapping it and accepting
        1 parameter: ``data``, the corresponding NumPy array.
    """

    __slots__ = ()


_Structure = collections.namedtuple(
    'Structure', (
        'fields',
        'name',
        'view',
    ))
_Structure.__new__.__defaults__ = (None, None)


class Structure(_Structure):
    """Type corresponding to a NumPy structured array.

    Attributes
    ----------
    fields : tuple of nani.Field or compatible tuple
        Fields defining the structure.
    name : str or None
        Name for the view type if `view` is ``None``.
    view : type or None
        If ``None``, a view for this structured array is dynamically generated
        by Nani, otherwise it is expected to be a class object wrapping it and
        accepting 1 parameter: ``data``, the corresponding NumPy structured
        array.
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
    'Field', (
        'name',
        'type',
        'read_only',
    ))
_Field.__new__.__defaults__ = (False,)


class Field(_Field):
    """Describe a field of a structured array.

    Attributes
    ----------
    name : str
        Name of the field.
    type : nani data type
        Type of the field.
    read_only : bool
        ``True`` to not define a setter property in the structured array view
        if it is set to be dynamically generated by Nani.
    """

    __slots__ = ()


#: Constant to use for the :attr:`Field.read_only` attribute's value.
#: To use for readability reasons when the ``read_only`` keyword is not
#: explicitely written.
READ_ONLY = True


_FIELD_NAME_IDX = Field._fields.index('name')
_FIELD_TYPE_IDX = Field._fields.index('type')
_FIELD_ATTR_COUNT = len(Field._fields)
_FIELD_REQUIRED_ARG_RANGE = _range(
    _FIELD_ATTR_COUNT - len(Field.__new__.__defaults__),
    _FIELD_ATTR_COUNT + 1)


_FieldInstanceCheck = collections.namedtuple(
    '_FieldInstanceCheck', (
        'name',
        'type',
        'allow_none',
    ))
_FieldInstanceCheck.__new__.__defaults__ = (False,)


_FieldSubclassCheck = collections.namedtuple(
    '_FieldSubclassCheck', (
        'name',
        'type',
        'allow_none',
    ))
_FieldSubclassCheck.__new__.__defaults__ = (False,)


_TYPE_ATTR_CHECKS = {
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
        _FieldInstanceCheck(name='shape', type=_SEQUENCE_TYPES + (int,)),
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

    def __repr__(self):
        return "[%s]" % (', '.join(str(item) for item in self._data))

    def __eq__(self, other):
        if isinstance(other, type(self)):
            return numpy.array_equal(self._data, other._data)

        return NotImplemented

    def __ne__(self, other):
        is_equal = self.__eq__(other)
        return is_equal if is_equal is NotImplemented else not is_equal

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
    '__repr__',
    '__eq__',
    '__ne__',
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

    def __repr__(self):
        return "[%s]" % (', '.join(str(self._element_view(self._data, i))
                                   for i in _range(len(self._data))))

    def __eq__(self, other):
        if isinstance(other, type(self)):
            return numpy.array_equal(self._data, other._data)

        return NotImplemented

    def __ne__(self, other):
        is_equal = self.__eq__(other)
        return is_equal if is_equal is NotImplemented else not is_equal

    def __getitem__(self, index):
        return self._element_view(self._data, index)

    def __setitem__(self, index, value):
        self._data[index] = value

    def __iter__(self):
        return (self._element_view(self._data, i)
                for i in _range(len(self._data)))

    def __len__(self):
        return len(self._data)

    def __contains__(self, item):
        return item in self._data


_MIXIN_ATTRIBUTES[_IndirectAtomicArrayViewMixin] = (
    '__slots__',
    '__init__',
    '__repr__',
    '__eq__',
    '__ne__',
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

    The element views are to be initialized with 1 parameter: ``data``, the
    NumPy array representing the element.
    """

    __slots__ = ('_data',)

    def __init__(self, data):
        self._data = data

    def __repr__(self):
        return "[%s]" % (', '.join(str(self._element_view(item))
                                   for item in self._data))

    def __eq__(self, other):
        if isinstance(other, type(self)):
            return numpy.array_equal(self._data, other._data)

        return NotImplemented

    def __ne__(self, other):
        is_equal = self.__eq__(other)
        return is_equal if is_equal is NotImplemented else not is_equal

    def __getitem__(self, index):
        return self._element_view(self._data[index])

    def __setitem__(self, index, value):
        self._data[index] = value

    def __iter__(self):
        return (self._element_view(item) for item in self._data)

    def __len__(self):
        return self._data.__len__()

    def __contains__(self, item):
        return item in self._data


_MIXIN_ATTRIBUTES[_IndirectCompositeArrayViewMixin] = (
    '__slots__',
    '__init__',
    '__repr__',
    '__eq__',
    '__ne__',
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

    def __repr__(self):
        fields_and_values = ("%s=%r" % (field, getattr(self, field))
                             for field in self._fields)
        return "%s(%s)" % (type(self).__name__, ', '.join(fields_and_values))

    def __eq__(self, other):
        if isinstance(other, type(self)):
            return numpy.array_equal(self._data, other._data)

        return NotImplemented

    def __ne__(self, other):
        is_equal = self.__eq__(other)
        return is_equal if is_equal is NotImplemented else not is_equal


_MIXIN_ATTRIBUTES[_StructuredViewMixin] = (
    '__slots__',
    '__init__',
    '__repr__',
    '__eq__',
    '__ne__',
)


_Nani = collections.namedtuple(
    'Nani', (
        'dtype',
        'default',
        'view',
    ))


class Nani(_Nani):
    """Output structure of the function `resolve`.

    Attributes
    ----------
    dtype : numpy.dtype
        NumPy's ``dtype``, that is the data type of the array elements.
    default : object
        Default value(s) for a single array element.
    view : type
        A class to use as a wrapper around the NumPy array.
    """

    __slots__ = ()


def validate(data_type):
    """Check if a data type is well-formed.

    Parameters
    ----------
    data_type : nani data type
        Data type.

    Returns
    -------
    bool
        ``True`` if the data type is well-formed.

    Raises
    ------
    TypeError or ValueError
        The data type isn't well-formed.
    """
    return _validate(data_type, '')


def resolve(data_type, name=None, listify_default=False):
    """Retrieve the properties for a given data type.

    This is the main routine where most of the work is done. It converts
    Nani's data types into properties that can be used to define a new NumPy
    array and to wrap it into a view object.

    Use :func:`validate` to check if the input data type is well-formed.

    Parameters
    ----------
    data_type : nani data type
        Type of the array elements.
    name : str
        Name for the view to be generated for the array.
    listify_default : bool
        ``True`` to output the default values with lists in place of tuples.
        This might cause the output to be incompatible with array creation
        routines such as ``numpy.array`` but it should still work for
        element assignment.

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
    ...     view=None)
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
    data_type = _consolidate(data_type)
    return Nani(
        dtype=numpy.dtype(_resolve_dtype(data_type)),
        default=_resolve_default(data_type, listify=listify_default),
        view=_resolve_view(Array(element_type=data_type, shape=-1, name=name)))


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
    ...     shape=2)
    >>> new_data_type = nani.update(
    ...     data_type,
    ...     element_type=nani.update(data_type.element_type, default=123),
    ...     shape=3)
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
        The NumPy array, ``None`` otherwise.

    Examples
    --------
    >>> import numpy
    >>> import nani
    >>> data_type = nani.Number(type=numpy.int32)
    >>> dtype, _, view = nani.resolve(data_type)
    >>> a = numpy.a_range(10, dtype=dtype)
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
        The element view, ``None`` otherwise.

    Examples
    --------
    >>> import numpy
    >>> import nani
    >>> vector2_type = nani.Array(
    ...     element_type=nani.Number(),
    ...     shape=2,
    ...     name='Vector2')
    >>> dtype, default, view = nani.resolve(vector2_type, name='Positions')
    >>> a = numpy.zeros(3, dtype=dtype)
    >>> v = view(a)
    >>> type(v)
    <class 'nani.Positions'>
    >>> nani.get_element_view(v)
    <class 'nani.Vector2'>
    """
    return getattr(view, '_element_view', None)


def _validate(data_type, parent_path):
    """Implementation for the `validate` function."""
    if isinstance(data_type, _CLASS_TYPES):
        raise TypeError(
            "The data type is expected to be an instance object, but got the "
            "type '%s' instead." % (_format_type(data_type),))

    base = _find_base_type(data_type)
    if not base:
        raise TypeError(
            "Objects of type '%s' aren't supported as data types. Use any "
            "type from %s instead."
            % (_format_type(type(data_type)), _join_types(_ALL, "or ")))

    name = getattr(data_type, 'name', None)
    if not name:
        name = type(data_type).__name__

    full_path = '%s.%s' % (parent_path, name) if parent_path else name

    # Generic checks for each attribute.
    for check in _TYPE_ATTR_CHECKS[base]:
        attribute = getattr(data_type, check.name)
        if attribute is None:
            if check.allow_none:
                continue
            else:
                raise TypeError("The attribute '%s.%s' cannot be 'None'."
                                % (full_path, check.name))

        if isinstance(check, _FieldInstanceCheck):
            check_function = isinstance
        elif isinstance(check, _FieldSubclassCheck):
            if not isinstance(attribute, _CLASS_TYPES):
                raise TypeError(
                    "The attribute '%s.%s' is expected to be a type "
                    "object%s." % (full_path, check.name,
                                   " or 'None'" if check.allow_none else ''))

            check_function = issubclass

        if not check_function(attribute, check.type):
            if isinstance(check, _FieldInstanceCheck):
                glue_1 = "an instance object of type"
                glue_2 = "not"
                glue_3 = ""
                type_name = _format_type(type(attribute))
            elif isinstance(check, _FieldSubclassCheck):
                glue_1 = "a subclass of"
                glue_2 = "but got"
                glue_3 = " instead"
                type_name = _format_type(attribute)

            raise TypeError(
                "The attribute '%s.%s' is expected to be %s %s, %s '%s'%s."
                % (full_path, check.name, glue_1,
                   _join_types(check.type, "or "), glue_2, type_name, glue_3))

    # Additional and/or recursive checks for specific attributes.
    if isinstance(data_type, Array):
        _validate(data_type.element_type, full_path)
    elif isinstance(data_type, Structure):
        for field in data_type.fields:
            if not isinstance(field, _SEQUENCE_TYPES):
                raise TypeError(
                    "Each field from the attribute '%s.fields' is expected "
                    "to be an instance object of type %s, not '%s'."
                    % (full_path,
                       _join_types(_SEQUENCE_TYPES + (Field,), "or "),
                       _format_type(type(field))))

            if len(field) not in _FIELD_REQUIRED_ARG_RANGE:
                raise TypeError(
                    "Each field from the attribute '%s.fields' is expected "
                    "to be an instance object of type %s, and compatible with "
                    "the '%s' structure, but got %r instead."
                    % (full_path,
                       _join_types(_SEQUENCE_TYPES + (Field,), "or "),
                       _format_type(Field), field))

            field = Field(*field)
            if not isinstance(field.name, _STRING_TYPES):
                raise TypeError(
                    "The first element of each field from the attribute "
                    "'%s.fields', that is the 'name' attribute, is expected "
                    "to be an instance object of type %s, not '%s'."
                    % (full_path, _join_types(_STRING_TYPES, "or "),
                       _format_type(type(field.name))))

            if not isinstance(field.type, _ALL):
                raise TypeError(
                    "The second element of each field from the attribute "
                    "'%s.fields', that is the 'type' attribute, is expected "
                    "to be an instance object of type %s, not '%s'."
                    % (full_path, _join_types(_ALL, "or "),
                       _format_type(type(field.type))))

            if not isinstance(field.read_only, bool):
                raise TypeError(
                    "The third element of each field from the attribute "
                    "'%s.fields', that is the 'read_only' attribute, is "
                    "expected to be an instance object of type 'bool', "
                    "not '%s'." % (full_path,
                                   _format_type(type(field.read_only))))

            field_path = '%s.%s' % (full_path, field.name)
            _validate(field.type, field_path)

        fields = [field[_FIELD_NAME_IDX] for field in data_type.fields]
        duplicates = _find_duplicates(fields)
        if duplicates:
            if len(duplicates) > 1:
                raise ValueError(
                    "The structure fields %s, were provided multiple times."
                    % (_join_sequence(duplicates, "and ")),)
            else:
                raise ValueError(
                    "The structure field '%s' was provided multiple times."
                    % (duplicates[0]),)

    return True


def _consolidate(data_type):
    """Enforce the structure of the data type.

    Specifically, ensure that if a field is defined as a generic tuple, then it
    will be converted into an instance of `Field`.
    """
    if isinstance(data_type, _ATOMIC):
        out = data_type
    elif isinstance(data_type, Array):
        element_type = _consolidate(data_type.element_type)
        out = data_type._replace(element_type=element_type)
    elif isinstance(data_type, Structure):
        fields = tuple(
            Field(*(_consolidate(field[i]) if i == _FIELD_TYPE_IDX
                    else field[i]
                    for i in _range(len(field))))
            for field in data_type.fields)
        out = data_type._replace(fields=fields)

    return out


def _resolve_dtype(data_type):
    """Retrieve the corresponding NumPy's `dtype` for a given data type."""
    if isinstance(data_type, _FIXED_ATOMIC):
        out = _get_atomic_dtype(data_type)
    elif isinstance(data_type, _FLEXIBLE_ATOMIC):
        out = (_get_atomic_dtype(data_type), data_type.length)
    elif isinstance(data_type, Array):
        shape = data_type.shape
        if isinstance(shape, _SEQUENCE_TYPES) and len(shape) == 1:
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
    """Retrieve the default value for a given data type."""
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
        out = element_default
        for dimension in shape:
            out = Sequence(copy.deepcopy(out) for _ in _range(dimension))
    elif isinstance(data_type, Structure):
        if listify:
            out = [_resolve_default(field.type, listify=listify)
                   for field in data_type.fields]
        else:
            field_defaults = collections.OrderedDict(
                (field.name, _resolve_default(field.type, listify=listify))
                for field in data_type.fields)
            name = ('StructureDefault_%s' % (data_type.name,)
                    if data_type.name else 'StructureDefault')
            struct = collections.namedtuple(name, field_defaults.keys())
            out = struct(**field_defaults)

    return out


def _resolve_view(data_type):
    """Retrieve the view for a given data type.

    Only one view class is returned, that is the one representing the root data
    type, but more class objects might be dynamically created if the input
    data type has nested elements, such as for the `Array` and `Structure`
    types.

    The default behaviour of dynamically and recursively creating a new view
    class can be overriden by setting the `view` attribute of a data type.
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
    """Define a new view object for a `Array` type."""
    element_type = data_type.element_type
    element_view = _resolve_view(element_type)
    if element_view is None:
        mixins = (_DirectArrayViewMixin,)
        attributes = _get_mixin_attributes(mixins)
    elif isinstance(element_type, _ATOMIC):
        mixins = (_IndirectAtomicArrayViewMixin,)
        attributes = _get_mixin_attributes(mixins)
        attributes.update({
            '_element_view': element_view,
        })
    else:
        mixins = (_IndirectCompositeArrayViewMixin,)
        attributes = _get_mixin_attributes(mixins)
        attributes.update({
            '_element_view': element_view,
        })

    name = data_type.name if data_type.name else 'ArrayView'
    return type(name, (), attributes)


def _define_structure_view(data_type):
    """Define a new view object for a `Structure` type."""
    def define_getter(field_index, field_type, field_view):
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

    def define_setter(field_index, read_only):
        def setter(self, value):
            self._data[field_index] = value

        return None if read_only else setter

    field_views = [_resolve_view(field.type) for field in data_type.fields]
    mixins = (_StructuredViewMixin,)
    attributes = _get_mixin_attributes(mixins)
    attributes.update({
        '_fields': tuple(field.name for field in data_type.fields),
    })
    attributes.update({
        field.name: property(
            fget=define_getter(i, field.type, field_view),
            fset=define_setter(i, field.read_only),
            fdel=None)
        for i, (field, field_view)
        in enumerate(zip(data_type.fields, field_views))})
    name = data_type.name if data_type.name else 'StructureView'
    return type(name, (), attributes)


def _get_mixin_attributes(mixins):
    """Retrieve the attributes for a given set of mixin classes.

    The attributes of each mixin class are being merged into a single
    dictionary.
    """
    return {attribute: mixin.__dict__[attribute]
            for mixin in mixins
            for attribute in _MIXIN_ATTRIBUTES[mixin]}


def _get_atomic_dtype(data_type):
    """Retrieve the NumPy's `dtype` for a given atomic data type."""
    atomic_type = getattr(data_type, 'type', None)
    if atomic_type is not None:
        return atomic_type

    return _PREDEFINED_ATOMIC_NUMPY_TYPES[_find_base_type(data_type)]


def _find_base_type(data_type):
    """Find the Nani's base type for a given data type.

    This is useful when Nani's data types were subclassed and the original type
    is required.
    """
    bases = type(data_type).__mro__
    for base in bases:
        if base in _ALL:
            return base

    return None


def _find_duplicates(seq):
    """Find the duplicate elements from a sequence."""
    seen = set()
    return [element for element in seq
            if seq.count(element) > 1
            and element not in seen and seen.add(element) is None]


def _format_type(cls):
    """Format a type name for printing."""
    if cls.__module__ == _BUILTIN_MODULE:
        return cls.__name__
    else:
        return '%s.%s' % (cls.__module__, cls.__name__)


def _format_element(element, count, index, last_separator):
    """Format an element from a sequence.

    This only prepends a separator for the last element and wraps each element
    with single quotes.
    """
    return ("%s'%s'" % (last_separator, element)
            if count > 1 and index == count - 1
            else "'%s'" % (element,))


def _join_sequence(seq, last_separator=''):
    """Join a sequence into a string."""
    count = len(seq)
    return ', '.join(_format_element(element, count, i, last_separator)
                     for i, element in enumerate(seq))


def _join_types(seq, last_separator=''):
    """Join class object names into a string."""
    class_names = [_format_type(cls) for cls in seq]
    return _join_sequence(class_names, last_separator)
