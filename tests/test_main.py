#!/usr/bin/env python

import os
import sys
_HERE = os.path.abspath(os.path.dirname(__file__))
sys.path.insert(0, os.path.abspath(os.path.join(_HERE, os.pardir)))


import sys
import unittest

from distutils.version import StrictVersion

import numpy

import nani

from tests.data import flag as _flag
from tests.data import numbers as _numbers
from tests.data import particle as _particle
from tests.data import subtypes as _subtypes
from tests.data import vector2 as _vector2


_PY2 = sys.version_info[0] == 2


_NUMPY_VERSION = StrictVersion(numpy.__version__)
_NUMPY_VERSION_1_10_1 = _NUMPY_VERSION >= StrictVersion('1.10.1')


if _PY2:
    import cPickle as pickle

    _STRING_TYPES = (basestring,)
    _String = str
    _Unicode = unicode
    _BuiltinString = str
    _BuiltinUnicode = unicode
    _BUILTIN_MODULE = '__builtin__'
else:
    import pickle

    _STRING_TYPES = (str,)
    _String = bytes
    _Unicode = str
    _BuiltinString = bytes
    _BuiltinUnicode = str
    _BUILTIN_MODULE = 'builtins'


def _array_to_list(array):
    if isinstance(array, numpy.ndarray):
        return _array_to_list(array.tolist())
    elif isinstance(array, list):
        return [_array_to_list(item) for item in array]
    elif isinstance(array, tuple):
        return tuple(_array_to_list(item) for item in array)
    else:
        return array


def _join_sequence(seq, last_separator):
    def format(item, count, index):
        return ("%s'%s'" % (last_separator, item)
                if count > 1 and index == count - 1
                else "'%s'" % (item))


    if not isinstance(seq, (list, tuple)):
        seq = (seq,)

    count = len(seq)
    return ', '.join(format(item, count, i) for i, item in enumerate(seq))


def _join_types(seq, last_separator):
    if not isinstance(seq, (list, tuple)):
        seq = (seq,)

    class_names = ['%s.%s' % (cls.__module__, cls.__name__)
                   if cls.__module__ != _BUILTIN_MODULE else cls.__name__
                   for cls in seq]
    return _join_sequence(class_names, last_separator)


class MainTest(unittest.TestCase):

    def test_aliases(self):
        self.assertIs(nani.Bytes, nani.String)
        if _PY2:
            self.assertIs(nani.Str, nani.String)
        else:
            self.assertIs(nani.Str, nani.Unicode)

    def test_bool_constructor(self):
        data_type = nani.Bool()
        self.assertEqual(data_type, (False, None))
        self.assertEqual(data_type._fields, ('default', 'view'))
        self.assertTrue(nani.validate(data_type))

    def test_object_constructor(self):
        data_type = nani.Object()
        self.assertEqual(data_type, (None, None))
        self.assertEqual(data_type._fields, ('default', 'view'))
        self.assertTrue(nani.validate(data_type))

    def test_number_constructor(self):
        data_type = nani.Number()
        self.assertEqual(data_type, (numpy.float_, 0, None))
        self.assertEqual(data_type._fields, ('type', 'default', 'view'))
        self.assertTrue(nani.validate(data_type))

    def test_string_constructor(self):
        self.assertRaises(TypeError, nani.String)

        data_type = nani.String(length=8)
        self.assertEqual(data_type, (8, _BuiltinString(), None))
        self.assertEqual(data_type._fields, ('length', 'default', 'view'))
        self.assertTrue(nani.validate(data_type))

    def test_unicode_constructor(self):
        self.assertRaises(TypeError, nani.Unicode)

        data_type = nani.Unicode(length=8)
        self.assertEqual(data_type, (8, _BuiltinUnicode(), None))
        self.assertEqual(data_type._fields, ('length', 'default', 'view'))
        self.assertTrue(nani.validate(data_type))

    def test_array_constructor(self):
        self.assertRaises(TypeError, nani.Array)
        self.assertRaises(TypeError, nani.Array, element_type=nani.Number())

        data_type = nani.Array(element_type=nani.Number(), shape=1)
        self.assertEqual(data_type, (nani.Number(), 1, None, None))
        self.assertEqual(data_type._fields, ('element_type', 'shape', 'name', 'view'))
        self.assertTrue(nani.validate(data_type))

    def test_structure_constructor(self):
        self.assertRaises(TypeError, nani.Structure)

        data_type = nani.Structure(fields=())
        self.assertEqual(data_type, ((), None, None))
        self.assertEqual(data_type._fields, ('fields', 'name', 'view'))
        self.assertTrue(nani.validate(data_type))

    def test_bool_valid_attributes(self):
        data_type = nani.Bool(default=True)
        self.assertTrue(nani.validate(data_type))
        self.assertIsNotNone(nani.resolve(data_type))

        data_type = nani.Bool(default=False)
        self.assertTrue(nani.validate(data_type))
        self.assertIsNotNone(nani.resolve(data_type))

    def test_object_valid_attributes(self):
        data_type = nani.Object(default=None)
        self.assertTrue(nani.validate(data_type))
        self.assertIsNotNone(nani.resolve(data_type))

        data_type = nani.Object(default=123)
        self.assertTrue(nani.validate(data_type))
        self.assertIsNotNone(nani.resolve(data_type))

        data_type = nani.Object(default=1.23)
        self.assertTrue(nani.validate(data_type))
        self.assertIsNotNone(nani.resolve(data_type))

        data_type = nani.Object(default='abc')
        self.assertTrue(nani.validate(data_type))
        self.assertIsNotNone(nani.resolve(data_type))

        data_type = nani.Object(default=[])
        self.assertTrue(nani.validate(data_type))
        self.assertIsNotNone(nani.resolve(data_type))

        data_type = nani.Object(default=())
        self.assertTrue(nani.validate(data_type))
        self.assertIsNotNone(nani.resolve(data_type))

        data_type = nani.Object(default={})
        self.assertTrue(nani.validate(data_type))
        self.assertIsNotNone(nani.resolve(data_type))

        data_type = nani.Object(default=_vector2.Vector2View)
        self.assertTrue(nani.validate(data_type))
        self.assertIsNotNone(nani.resolve(data_type))

    def test_number_valid_attributes(self):
        data_type = nani.Number(type=bool, default=True)
        self.assertTrue(nani.validate(data_type))
        self.assertIsNotNone(nani.resolve(data_type))

        data_type = nani.Number(type=int, default=123)
        self.assertTrue(nani.validate(data_type))
        self.assertIsNotNone(nani.resolve(data_type))

        data_type = nani.Number(type=float, default=1.23)
        self.assertTrue(nani.validate(data_type))
        self.assertIsNotNone(nani.resolve(data_type))

        data_type = nani.Number(type=complex, default=1 + 23j)
        self.assertTrue(nani.validate(data_type))
        self.assertIsNotNone(nani.resolve(data_type))

        data_type = nani.Number(type=numpy.int32, default=123)
        self.assertTrue(nani.validate(data_type))
        self.assertIsNotNone(nani.resolve(data_type))

        data_type = nani.Number(type=numpy.float32, default=1.23)
        self.assertTrue(nani.validate(data_type))
        self.assertIsNotNone(nani.resolve(data_type))

        data_type = nani.Number(type=numpy.complex64, default=1 + 23j)
        self.assertTrue(nani.validate(data_type))
        self.assertIsNotNone(nani.resolve(data_type))

        data_type = nani.Number(type=_numbers.Bool, default=True)
        self.assertTrue(nani.validate(data_type))
        self.assertIsNotNone(nani.resolve(data_type))

        data_type = nani.Number(type=_numbers.Int, default=123)
        self.assertTrue(nani.validate(data_type))
        self.assertIsNotNone(nani.resolve(data_type))

        data_type = nani.Number(type=_numbers.Float, default=1.23)
        self.assertTrue(nani.validate(data_type))
        self.assertIsNotNone(nani.resolve(data_type))

        data_type = nani.Number(type=_numbers.Complex, default=1 + 23j)
        self.assertTrue(nani.validate(data_type))
        self.assertIsNotNone(nani.resolve(data_type))

        data_type = nani.Number(type=_numbers.NumpyInt, default=123)
        self.assertTrue(nani.validate(data_type))
        self.assertIsNotNone(nani.resolve(data_type))

        data_type = nani.Number(type=_numbers.NumpyFloat, default=1.23)
        self.assertTrue(nani.validate(data_type))
        self.assertIsNotNone(nani.resolve(data_type))

        data_type = nani.Number(type=_numbers.NumpyComplex, default=1 + 23j)
        self.assertTrue(nani.validate(data_type))
        self.assertIsNotNone(nani.resolve(data_type))

    def test_string_valid_attributes(self):
        if _PY2:
            data_type = nani.String(length=8, default='abc')
            self.assertTrue(nani.validate(data_type))
            self.assertIsNotNone(nani.resolve(data_type))

            data_type = nani.String(length=8, default=b'abc')
            self.assertTrue(nani.validate(data_type))
            self.assertIsNotNone(nani.resolve(data_type))
        else:
            data_type = nani.String(length=8, default=b'abc')
            self.assertTrue(nani.validate(data_type))
            self.assertIsNotNone(nani.resolve(data_type))

    def test_unicode_valid_attributes(self):
        if _PY2:
            data_type = nani.Unicode(length=8, default=u'abc')
            self.assertTrue(nani.validate(data_type))
            self.assertIsNotNone(nani.resolve(data_type))
        else:
            data_type = nani.Unicode(length=8, default='abc')
            self.assertTrue(nani.validate(data_type))
            self.assertIsNotNone(nani.resolve(data_type))

            data_type = nani.Unicode(length=8, default=u'abc')
            self.assertTrue(nani.validate(data_type))
            self.assertIsNotNone(nani.resolve(data_type))

    def test_array_valid_attributes(self):
        data_type = nani.Array(element_type=nani.Bool(), shape=0)
        self.assertTrue(nani.validate(data_type))
        self.assertIsNotNone(nani.resolve(data_type))

        data_type = nani.Array(element_type=nani.Object(), shape=0)
        self.assertTrue(nani.validate(data_type))
        self.assertIsNotNone(nani.resolve(data_type))

        data_type = nani.Array(element_type=nani.Number(), shape=0)
        self.assertTrue(nani.validate(data_type))
        self.assertIsNotNone(nani.resolve(data_type))

        data_type = nani.Array(element_type=nani.String(length=8), shape=0)
        self.assertTrue(nani.validate(data_type))
        self.assertIsNotNone(nani.resolve(data_type))

        data_type = nani.Array(element_type=nani.Unicode(length=8), shape=0)
        self.assertTrue(nani.validate(data_type))
        self.assertIsNotNone(nani.resolve(data_type))

        data_type = nani.Array(element_type=nani.Array(element_type=nani.Number(), shape=1), shape=0)
        self.assertTrue(nani.validate(data_type))
        self.assertIsNotNone(nani.resolve(data_type))

        data_type = nani.Array(element_type=nani.Structure(fields=(('number', nani.Number()),)), shape=0)
        self.assertTrue(nani.validate(data_type))
        self.assertIsNotNone(nani.resolve(data_type))

        data_type = nani.Array(element_type=nani.Bool(), shape=1)
        self.assertTrue(nani.validate(data_type))
        self.assertIsNotNone(nani.resolve(data_type))

        data_type = nani.Array(element_type=nani.Object(), shape=1)
        self.assertTrue(nani.validate(data_type))
        self.assertIsNotNone(nani.resolve(data_type))

        data_type = nani.Array(element_type=nani.Number(), shape=1)
        self.assertTrue(nani.validate(data_type))
        self.assertIsNotNone(nani.resolve(data_type))

        data_type = nani.Array(element_type=nani.String(length=8), shape=1)
        self.assertTrue(nani.validate(data_type))
        self.assertIsNotNone(nani.resolve(data_type))

        data_type = nani.Array(element_type=nani.Unicode(length=8), shape=1)
        self.assertTrue(nani.validate(data_type))
        self.assertIsNotNone(nani.resolve(data_type))

        data_type = nani.Array(element_type=nani.Array(element_type=nani.Number(), shape=1), shape=1)
        self.assertTrue(nani.validate(data_type))
        self.assertIsNotNone(nani.resolve(data_type))

        data_type = nani.Array(element_type=nani.Structure(fields=(('number', nani.Number()),)), shape=1)
        self.assertTrue(nani.validate(data_type))
        self.assertIsNotNone(nani.resolve(data_type))

        data_type = nani.Array(element_type=nani.Bool(), shape=[0])
        self.assertTrue(nani.validate(data_type))
        self.assertIsNotNone(nani.resolve(data_type))

        data_type = nani.Array(element_type=nani.Object(), shape=(0,))
        self.assertTrue(nani.validate(data_type))
        self.assertIsNotNone(nani.resolve(data_type))

        data_type = nani.Array(element_type=nani.Number(), shape=(0,))
        self.assertTrue(nani.validate(data_type))
        self.assertIsNotNone(nani.resolve(data_type))

        data_type = nani.Array(element_type=nani.String(length=8), shape=(0,))
        self.assertTrue(nani.validate(data_type))
        self.assertIsNotNone(nani.resolve(data_type))

        data_type = nani.Array(element_type=nani.Unicode(length=8), shape=(0,))
        self.assertTrue(nani.validate(data_type))
        self.assertIsNotNone(nani.resolve(data_type))

        data_type = nani.Array(element_type=nani.Array(element_type=nani.Number(), shape=1), shape=(0,))
        self.assertTrue(nani.validate(data_type))
        self.assertIsNotNone(nani.resolve(data_type))

        data_type = nani.Array(element_type=nani.Structure(fields=(('number', nani.Number()),)), shape=(0,))
        self.assertTrue(nani.validate(data_type))
        self.assertIsNotNone(nani.resolve(data_type))

        data_type = nani.Array(element_type=nani.Bool(), shape=[1])
        self.assertTrue(nani.validate(data_type))
        self.assertIsNotNone(nani.resolve(data_type))

        data_type = nani.Array(element_type=nani.Object(), shape=(1,))
        self.assertTrue(nani.validate(data_type))
        self.assertIsNotNone(nani.resolve(data_type))

        data_type = nani.Array(element_type=nani.Number(), shape=(1,))
        self.assertTrue(nani.validate(data_type))
        self.assertIsNotNone(nani.resolve(data_type))

        data_type = nani.Array(element_type=nani.String(length=8), shape=(1,))
        self.assertTrue(nani.validate(data_type))
        self.assertIsNotNone(nani.resolve(data_type))

        data_type = nani.Array(element_type=nani.Unicode(length=8), shape=(1,))
        self.assertTrue(nani.validate(data_type))
        self.assertIsNotNone(nani.resolve(data_type))

        data_type = nani.Array(element_type=nani.Array(element_type=nani.Number(), shape=1), shape=(1,))
        self.assertTrue(nani.validate(data_type))
        self.assertIsNotNone(nani.resolve(data_type))

        data_type = nani.Array(element_type=nani.Structure(fields=(('number', nani.Number()),)), shape=(1,))
        self.assertTrue(nani.validate(data_type))
        self.assertIsNotNone(nani.resolve(data_type))

        data_type = nani.Array(element_type=nani.Bool(), shape=[1, 2])
        self.assertTrue(nani.validate(data_type))
        self.assertIsNotNone(nani.resolve(data_type))

        data_type = nani.Array(element_type=nani.Object(), shape=(1, 2))
        self.assertTrue(nani.validate(data_type))
        self.assertIsNotNone(nani.resolve(data_type))

        data_type = nani.Array(element_type=nani.Number(), shape=(1, 2))
        self.assertTrue(nani.validate(data_type))
        self.assertIsNotNone(nani.resolve(data_type))

        data_type = nani.Array(element_type=nani.String(length=8), shape=(1, 2))
        self.assertTrue(nani.validate(data_type))
        self.assertIsNotNone(nani.resolve(data_type))

        data_type = nani.Array(element_type=nani.Unicode(length=8), shape=(1, 2))
        self.assertTrue(nani.validate(data_type))
        self.assertIsNotNone(nani.resolve(data_type))

        data_type = nani.Array(element_type=nani.Array(element_type=nani.Number(), shape=1), shape=(1, 2))
        self.assertTrue(nani.validate(data_type))
        self.assertIsNotNone(nani.resolve(data_type))

        data_type = nani.Array(element_type=nani.Structure(fields=(('number', nani.Number()),)), shape=(1, 2))
        self.assertTrue(nani.validate(data_type))
        self.assertIsNotNone(nani.resolve(data_type))

    def test_structure_valid_attributes(self):
        data_type = nani.Structure(
            fields=(
                ('number', nani.Number()),
            )
        )
        self.assertTrue(nani.validate(data_type))
        self.assertIsNotNone(nani.resolve(data_type))

        data_type = nani.Structure(
            fields=(
                ('bool', nani.Bool()),
                ('string', nani.String(length=8)),
                ('array', nani.Array(element_type=nani.Number(), shape=1)),
                ('structure', nani.Structure(fields=(
                    ('unicode', nani.Unicode(length=8)),
                ))),
            )
        )
        self.assertTrue(nani.validate(data_type))
        self.assertIsNotNone(nani.resolve(data_type))

        data_type = nani.Structure(
            fields=(
                ('position', _vector2.VECTOR2_TYPE),
                ('velocity', _vector2.VECTOR2_TYPE),
                ('targets', nani.Array(element_type=_vector2.VECTOR2_TYPE, shape=1)),
                ('particle', _particle.PARTICLE_TYPE),
            )
        )
        self.assertTrue(nani.validate(data_type))
        self.assertIsNotNone(nani.resolve(data_type))

        data_type = nani.Structure(
            fields=(
                ('position', _vector2.VECTOR2_TYPE),
                ('velocity', _vector2.VECTOR2_TYPE),
                ('particle', _particle.PARTICLE_TYPE),
            )
        )
        self.assertTrue(nani.validate(data_type))
        self.assertIsNotNone(nani.resolve(data_type))

        data_type = nani.Structure(
            fields=[
                ['position', _vector2.VECTOR2_TYPE],
                ['velocity', _vector2.VECTOR2_TYPE],
                ['particle', _particle.PARTICLE_TYPE],
            ]
        )
        self.assertTrue(nani.validate(data_type))
        self.assertIsNotNone(nani.resolve(data_type))

    def test_bool_invalid_attributes(self):
        self.assertRaises(TypeError, nani.validate, nani.Bool(default=None))
        self.assertRaises(TypeError, nani.validate, nani.Bool(default=123))
        self.assertRaises(TypeError, nani.validate, nani.Bool(default=1.23))
        self.assertRaises(TypeError, nani.validate, nani.Bool(default='abc'))
        self.assertRaises(TypeError, nani.validate, nani.Bool(default=[]))
        self.assertRaises(TypeError, nani.validate, nani.Bool(default=()))
        self.assertRaises(TypeError, nani.validate, nani.Bool(default={}))

    def test_number_invalid_attributes(self):
        self.assertRaises(TypeError, nani.validate, nani.Number(type=None))
        self.assertRaises(TypeError, nani.validate, nani.Number(type=numpy.bool_))
        self.assertRaises(TypeError, nani.validate, nani.Number(type=numpy.object_))
        self.assertRaises(TypeError, nani.validate, nani.Number(type=numpy.string_))
        self.assertRaises(TypeError, nani.validate, nani.Number(type=numpy.unicode_))

        self.assertRaises(TypeError, nani.validate, nani.Number(default=None))
        self.assertRaises(TypeError, nani.validate, nani.Number(default='abc'))
        self.assertRaises(TypeError, nani.validate, nani.Number(default=[]))
        self.assertRaises(TypeError, nani.validate, nani.Number(default=()))
        self.assertRaises(TypeError, nani.validate, nani.Number(default={}))

    def test_string_invalid_attributes(self):
        self.assertRaises(TypeError, nani.validate, nani.String(length=1.23))
        self.assertRaises(TypeError, nani.validate, nani.String(length='abc'))
        self.assertRaises(TypeError, nani.validate, nani.String(length=[8]))

    def test_unicode_invalid_attributes(self):
        self.assertRaises(TypeError, nani.validate, nani.Unicode(length=1.23))
        self.assertRaises(TypeError, nani.validate, nani.Unicode(length='abc'))
        self.assertRaises(TypeError, nani.validate, nani.Unicode(length=[8]))

    def test_array_invalid_attributes(self):
        self.assertRaises(TypeError, nani.validate, nani.Array(element_type=None, shape=1))

    def test_structure_invalid_attributes(self):
        self.assertRaises(ValueError, nani.validate, nani.Structure(fields=(('duplicate', nani.Number()), ('duplicate', nani.Bool()))))

    def test_subtypes(self):
        data_type = _subtypes.Bool()
        self.assertTrue(nani.validate(data_type))
        self.assertIsNotNone(nani.resolve(data_type))

        data_type = _subtypes.Object()
        self.assertTrue(nani.validate(data_type))
        self.assertIsNotNone(nani.resolve(data_type))

        data_type = _subtypes.Number()
        self.assertTrue(nani.validate(data_type))
        self.assertIsNotNone(nani.resolve(data_type))

        data_type = _subtypes.Array(element_type=nani.Number(), shape=1)
        self.assertTrue(nani.validate(data_type))
        self.assertIsNotNone(nani.resolve(data_type))

        data_type = _subtypes.Structure(fields=())
        self.assertTrue(nani.validate(data_type))
        self.assertIsNotNone(nani.resolve(data_type))

    def test_without_listify(self):
        self.assertTrue(nani.validate(_particle.PARTICLE_TYPE))

        _, default, _ = nani.resolve(_particle.PARTICLE_TYPE)
        self.assertEqual(default, (numpy.uint32(-1), (0.0, 0.0), 1.0, None))
        self.assertEqual(default._fields, ('id', 'position', 'mass', 'neighbours'))

    def test_with_listify(self):
        self.assertTrue(nani.validate(_particle.PARTICLE_TYPE))

        _, default, _ = nani.resolve(_particle.PARTICLE_TYPE, listify_default=True)
        self.assertEqual(default, [numpy.uint32(-1), [0.0, 0.0], 1.0, None])

    def test_deep_copy(self):
        data_type = nani.Array(
            element_type=nani.Object(default=[]),
            shape=2
        )
        self.assertTrue(nani.validate(data_type))

        _, default, _ = nani.resolve(data_type)
        self.assertEqual(default, ([], []))

        default[0].append('local')
        self.assertEqual(default, (['local'], []))

    def test_error_messages(self):
        with self.assertRaises(TypeError) as c:
            nani.validate(nani.Number)

        self.assertEqual(str(c.exception), "The data type is expected to be an instance object, but got the type 'nani.Number' instead.")

        with self.assertRaises(TypeError) as c:
            nani.validate(123)

        self.assertEqual(str(c.exception), "Objects of type 'int' aren't supported as data types. Use any type from %s instead." % (_join_types(nani._ALL, "or "),))

        with self.assertRaises(TypeError) as c:
            nani.validate(nani.Number(type=None))

        self.assertEqual(str(c.exception), "The attribute 'Number.type' cannot be 'None'.")

        with self.assertRaises(TypeError) as c:
            nani.validate(nani.Number(type=123))

        self.assertEqual(str(c.exception), "The attribute 'Number.type' is expected to be a type object.")

        with self.assertRaises(TypeError) as c:
            nani.validate(nani.Array(element_type=nani.Number(), shape=0, view=123))

        self.assertEqual(str(c.exception), "The attribute 'Array.view' is expected to be a type object or 'None'.")

        with self.assertRaises(TypeError) as c:
            nani.validate(nani.Array(element_type=123, shape=0))

        self.assertEqual(str(c.exception), "The attribute 'Array.element_type' is expected to be an instance object of type %s, not 'int'." % (_join_types(nani._ALL, "or "),))

        with self.assertRaises(TypeError) as c:
            nani.validate(nani.Number(type=str))

        self.assertEqual(str(c.exception), "The attribute 'Number.type' is expected to be a subclass of %s, but got 'str' instead." % (_join_types(nani._NUMBER_TYPES, "or "),))

        with self.assertRaises(TypeError) as c:
            nani.validate(nani.Structure(fields=('abc', 123), name='Something'))

        self.assertEqual(str(c.exception), "Each field from the attribute 'Something.fields' is expected to be an instance object of type 'list', 'tuple', or 'nani.Field', not 'str'.")

        with self.assertRaises(TypeError) as c:
            nani.validate(nani.Structure(fields=(('abc',),), name='Whatever'))

        self.assertEqual(str(c.exception), "Each field from the attribute 'Whatever.fields' is expected to be an instance object of type 'list', 'tuple', or 'nani.Field', and compatible with the 'nani.Field' structure, but got ('abc',) instead.")

        with self.assertRaises(TypeError) as c:
            nani.validate(nani.Structure(fields=((1, nani.Number()),), name='Moon'))

        self.assertEqual(str(c.exception), "The first element of each field from the attribute 'Moon.fields', that is the 'name' attribute, is expected to be an instance object of type %s, not 'int'." % (_join_types(_STRING_TYPES, "or "),))

        with self.assertRaises(TypeError) as c:
            nani.validate(nani.Structure(fields=(('id', nani.Number),), name='Star'))

        self.assertEqual(str(c.exception), "The second element of each field from the attribute 'Star.fields', that is the 'type' attribute, is expected to be an instance object of type %s, not 'type'." % (_join_types(nani._ALL, "or "),))

        with self.assertRaises(TypeError) as c:
            nani.validate(nani.Structure(fields=(('id', nani.Number(), 1.23),)))

        self.assertEqual(str(c.exception), "The third element of each field from the attribute 'Structure.fields', that is the 'read_only' attribute, is expected to be an instance object of type 'bool', not 'float'.")

        with self.assertRaises(ValueError) as c:
            nani.validate(nani.Structure(fields=(('id', nani.Number()), ('id', nani.Number()), ('duplicate', nani.Bool()), ('duplicate', nani.Number()))))

        self.assertEqual(str(c.exception), "The structure fields 'id', and 'duplicate', were provided multiple times.")

    def test_update(self):
        data_type = nani.Number()
        new_data_type = nani.update(data_type, default=99)
        self.assertEqual(new_data_type.default, 99)
        self.assertEqual(data_type.default, 0)

        data_type = nani.Array(
            element_type=nani.Number(),
            shape=(2,)
        )
        new_data_type = nani.update(
            data_type,
            element_type=nani.update(data_type.element_type, default=123),
            shape=3
        )
        self.assertEqual(new_data_type.element_type.default, 123)
        self.assertEqual(new_data_type.shape, 3)

    def test_get_data(self):
        data_type = nani.Number(type=numpy.int32)
        self.assertTrue(nani.validate(data_type))

        dtype, _, view = nani.resolve(data_type)
        a = numpy.arange(10, dtype=dtype)
        v = view(a)
        self.assertIs(nani.get_data(v), a)

    def test_view(self):
        data_type = nani.Number(type=numpy.int32)
        self.assertTrue(nani.validate(data_type))

        dtype, _, view = nani.resolve(data_type)
        a = numpy.arange(10, dtype=dtype)
        v = view(a)
        self.assertEqual(len(a), len(v))

        for i, x in enumerate(v):
            self.assertEqual(x, i)
            self.assertEqual(v[i], i)
            self.assertTrue(i in v)

    def test_particles(self):
        # Create a simple array of particles.
        particle_type = _particle.PARTICLE_TYPE
        particle_count = 4
        user_default = [(i, [0, 0], 1.0, []) for i in range(particle_count)]
        expected_dtype = [
            ('id', numpy.uint32),
            ('position', numpy.float32, (2,)),
            ('mass', numpy.float32),
            ('neighbours', numpy.object_)
        ]
        expected_default = (numpy.uint32(-1), (0.0, 0.0), 1.0, None)
        self.assertTrue(nani.validate(particle_type))

        dtype, default, view = nani.resolve(particle_type, name='Particles')
        self.assertEqual(dtype, expected_dtype)
        self.assertIsInstance(default, tuple)
        self.assertEqual(default, expected_default)
        self.assertEqual(view.__name__, 'Particles')

        element_view = nani.get_element_view(view)
        self.assertEqual(element_view.__name__, 'ParticleView')

        a = numpy.array(user_default, dtype=dtype)
        self.assertEqual(a.dtype, expected_dtype)
        self.assertEqual(_array_to_list(a), user_default)

        # Custom view (the field 'id' is read-only).
        v = view(a)
        for i, p in enumerate(v):
            self.assertRaises(AttributeError, setattr, p, 'id', 0)
            self.assertEqual(type(p.position).__name__, 'Vector2View')
            self.assertTrue(hasattr(p.position, 'x'))
            self.assertTrue(hasattr(p.position, 'y'))
            self.assertTrue(hasattr(p.position, 'set'))
            self.assertTrue(hasattr(p.position, 'scale'))
            self.assertRaises(AttributeError, setattr, p, 'neighbours', [])
            p.neighbours.append(i)

        v[0].position.x = 1.25
        v[0].position.y = 1.75
        v[0].position.scale(2.0)
        v[1].position.set(3.0, 4.0)
        v[2].mass = 9.75
        v[3].neighbours.append('plenty')

        self.assertEqual(_array_to_list(a), [
            (0, [2.5, 3.5], 1.0, [0]),
            (1, [3.0, 4.0], 1.0, [1]),
            (2, [0, 0], 9.75, [2]),
            (3, [0, 0], 1.0, [3, 'plenty'])
        ])

        # Default view (all fields are settable).
        particle_type = nani.Structure(
            fields=(
                ('id', nani.Number(type=numpy.uint32)),
                ('position', nani.Array(
                    element_type=nani.Number(type=numpy.float32),
                    shape=(2,),
                    name='DefaultVector2View',
                    view=None
                )),
                ('mass', nani.Number(type=numpy.float32)),
                ('neighbours', nani.Object()),
            ),
            name='Particle',
            view=None
        )
        self.assertTrue(nani.validate(particle_type))

        _, _, view = nani.resolve(particle_type, name='Particles')
        self.assertEqual(view.__name__, 'Particles')

        element_view = nani.get_element_view(view)
        self.assertEqual(element_view.__name__, 'Particle')

        v = view(a)
        for i, p in enumerate(v):
            p.id *= 2
            self.assertEqual(type(p.position).__name__, 'DefaultVector2View')
            self.assertFalse(hasattr(p.position, 'x'))
            self.assertFalse(hasattr(p.position, 'y'))
            self.assertFalse(hasattr(p.position, 'set'))
            self.assertFalse(hasattr(p.position, 'scale'))
            p.position[0] *= 4.0
            p.position[1] *= 4.0
            p.neighbours = [i * i]

        if _NUMPY_VERSION_1_10_1:
            v[0].position = (1.0, 2.0)
            self.assertEqual(_array_to_list(a), [
                (0, [1.0, 2.0], 1.0, [0]),
                (2, [12.0, 16.0], 1.0, [1]),
                (4, [0, 0], 9.75, [4]),
                (6, [0, 0], 1.0, [9])
            ])
        else:
            self.assertEqual(_array_to_list(a), [
                (0, [10.0, 14.0], 1.0, [0]),
                (2, [12.0, 16.0], 1.0, [1]),
                (4, [0, 0], 9.75, [4]),
                (6, [0, 0], 1.0, [9])
            ])

        # Default view with explicit read-only id field.
        particle_type = nani.Structure(
            fields=(
                ('id', nani.Number(type=numpy.uint32), True),
                ('position', nani.Array(
                    element_type=nani.Number(type=numpy.float32),
                    shape=(2,),
                    name='DefaultVector2View',
                    view=None
                )),
                ('mass', nani.Number(type=numpy.float32)),
                ('neighbours', nani.Object()),
            ),
            name='Particle',
            view=None
        )
        self.assertTrue(nani.validate(particle_type))

        _, _, view = nani.resolve(particle_type, name='Particles')

        v = view(a)
        for i, p in enumerate(v):
            self.assertRaises(AttributeError, setattr, p, 'id', 0)

    def test_view_with_list(self):
        particle_type = nani.Structure(
            fields=(
                ('id', nani.Number(type=numpy.uint32)),
                ('position', nani.Array(
                    element_type=nani.Number(type=numpy.float32),
                    shape=(2,),
                    name='DefaultVector2View',
                    view=None
                )),
                ('mass', nani.Number(type=numpy.float32)),
                ('neighbours', nani.Object()),
            ),
            view=None
        )
        self.assertTrue(nani.validate(particle_type))

        _, _, view = nani.resolve(particle_type, name='Particles')
        a = [
            [0, [2.5, 3.5], 1.0, [0]],
            [1, [3.0, 4.0], 1.0, [1]],
            [2, [0, 0], 9.75, [2]],
            [3, [0, 0], 1.0, [3, 'plenty']],
        ]
        v = view(a)
        for i, p in enumerate(v):
            p.id *= 2
            p.position[0] *= 4.0
            p.position[1] *= 4.0
            p.neighbours = [i * i]

        self.assertEqual(a, [
            [0, [10.0, 14.0], 1.0, [0]],
            [2, [12.0, 16.0], 1.0, [1]],
            [4, [0, 0], 9.75, [4]],
            [6, [0, 0], 1.0, [9]]
        ])

    def test_array_flags(self):
        flag_type = nani.Number(type=numpy.uint8, view=_flag.Flag)
        self.assertTrue(nani.validate(flag_type))

        dtype, _, view = nani.resolve(flag_type, name='Flags')
        a = numpy.zeros(4, dtype=dtype)
        a[0] |= _flag.SOMETHING
        a[1] |= _flag.WHATEVER
        a[2] |= _flag.SOMETHING | _flag.WHATEVER

        v = view(a)
        self.assertTrue(v[0].something)
        self.assertFalse(v[0].whatever)
        self.assertFalse(v[1].something)
        self.assertTrue(v[1].whatever)
        self.assertTrue(v[2].something)
        self.assertTrue(v[2].whatever)
        self.assertFalse(v[3].something)
        self.assertFalse(v[3].whatever)

        v[0] |= _flag.WHATEVER
        v[1] &= ~_flag.WHATEVER
        v[2] &= ~_flag.WHATEVER
        v[3] |= _flag.SOMETHING
        self.assertTrue(a[0] & _flag.SOMETHING != 0)
        self.assertTrue(a[0] & _flag.WHATEVER != 0)
        self.assertFalse(a[1] & _flag.SOMETHING != 0)
        self.assertFalse(a[1] & _flag.WHATEVER != 0)
        self.assertTrue(a[2] & _flag.SOMETHING != 0)
        self.assertFalse(a[2] & _flag.WHATEVER != 0)
        self.assertTrue(a[3] & _flag.SOMETHING != 0)
        self.assertFalse(a[3] & _flag.WHATEVER != 0)

        v[0].something = False
        v[1].whatever = True
        self.assertFalse(a[0] & _flag.SOMETHING != 0)
        self.assertTrue(a[0] & _flag.WHATEVER != 0)
        self.assertFalse(a[1] & _flag.SOMETHING != 0)
        self.assertTrue(a[1] & _flag.WHATEVER != 0)

        first = v[0]
        first.something = True
        first &= ~_flag.WHATEVER
        self.assertTrue(a[0] & _flag.SOMETHING != 0)
        self.assertFalse(a[0] & _flag.WHATEVER != 0)
        first |= _flag.WHATEVER
        self.assertTrue(a[0] & _flag.WHATEVER != 0)

    def test_structure_flags(self):
        struct_type = nani.Structure(
            fields=[
                ['id', nani.Number(type=numpy.uint32)],
                ['flags', nani.Number(type=numpy.uint8, view=_flag.Flag)]
            ],
            name='Struct'
        )
        self.assertTrue(nani.validate(struct_type))

        dtype, _, view = nani.resolve(struct_type)
        a = numpy.zeros(4, dtype=dtype)
        a[0]['flags'] |= _flag.SOMETHING
        a[1]['flags'] |= _flag.WHATEVER
        a[2]['flags'] |= _flag.SOMETHING | _flag.WHATEVER

        v = view(a)
        self.assertTrue(v[0].flags.something)
        self.assertFalse(v[0].flags.whatever)
        self.assertFalse(v[1].flags.something)
        self.assertTrue(v[1].flags.whatever)
        self.assertTrue(v[2].flags.something)
        self.assertTrue(v[2].flags.whatever)
        self.assertFalse(v[3].flags.something)
        self.assertFalse(v[3].flags.whatever)

        v[0].flags |= _flag.WHATEVER
        v[1].flags &= ~_flag.WHATEVER
        v[2].flags &= ~_flag.WHATEVER
        v[3].flags |= _flag.SOMETHING
        self.assertTrue(a[0]['flags'] & _flag.SOMETHING != 0)
        self.assertTrue(a[0]['flags'] & _flag.WHATEVER != 0)
        self.assertFalse(a[1]['flags'] & _flag.SOMETHING != 0)
        self.assertFalse(a[1]['flags'] & _flag.WHATEVER != 0)
        self.assertTrue(a[2]['flags'] & _flag.SOMETHING != 0)
        self.assertFalse(a[2]['flags'] & _flag.WHATEVER != 0)
        self.assertTrue(a[3]['flags'] & _flag.SOMETHING != 0)
        self.assertFalse(a[3]['flags'] & _flag.WHATEVER != 0)

        v[0].flags.something = False
        v[1].flags.whatever = True
        self.assertFalse(a[0]['flags'] & _flag.SOMETHING != 0)
        self.assertTrue(a[0]['flags'] & _flag.WHATEVER != 0)
        self.assertFalse(a[1]['flags'] & _flag.SOMETHING != 0)
        self.assertTrue(a[1]['flags'] & _flag.WHATEVER != 0)

        first = v[0].flags
        first.something = True
        first &= ~_flag.WHATEVER
        self.assertTrue(a[0]['flags'] & _flag.SOMETHING != 0)
        self.assertFalse(a[0]['flags'] & _flag.WHATEVER != 0)
        first |= _flag.WHATEVER
        self.assertTrue(a[0]['flags'] & _flag.WHATEVER != 0)

    def test_array_view_1(self):
        data_type = nani.Array(
            element_type=nani.Number(type=numpy.int32),
            shape=3,
            view=None
        )
        self.assertTrue(nani.validate(data_type))

        dtype, _, view = nani.resolve(data_type)
        a = numpy.array([(1, 2, 3), (4, 5, 6)], dtype=dtype)
        b = numpy.array([(7, 8, 9), (10, 11, 12)], dtype=dtype)
        v = view(a)

        self.assertIs(v._data, a)
        self.assertEqual(_array_to_list(a), [[1, 2, 3], [4, 5, 6]])
        self.assertEqual(str(v), "[[1, 2, 3], [4, 5, 6]]")
        self.assertEqual(v, view(a))
        self.assertNotEqual(v, view(b))
        self.assertEqual(v.__eq__([[1, 2, 3], [4, 5, 6]]), NotImplemented)
        self.assertIs(v[0]._data.base, a)
        self.assertIs(v[1]._data.base, a)
        self.assertIsInstance(v[0], nani.get_element_view(view))
        self.assertIsInstance(v[1], nani.get_element_view(view))
        self.assertEqual([x for x in v], [view(a)[0], view(a)[1]])
        self.assertNotEqual([x for x in v], [view(b)[0], view(b)[1]])
        self.assertEqual(len(v), 2)
        self.assertTrue(6 in v)
        self.assertFalse(7 in v)

        self.assertEqual(str(v[0]), "[1, 2, 3]")
        self.assertEqual(str(v[1]), "[4, 5, 6]")
        self.assertEqual(v[0], view(a)[0])
        self.assertEqual(v[1], view(a)[1])
        self.assertNotEqual(v[0], view(b)[0])
        self.assertNotEqual(v[1], view(b)[1])
        self.assertEqual(v[0].__eq__([1, 2, 3]), NotImplemented)
        self.assertEqual(v[1].__eq__([4, 5, 6]), NotImplemented)
        self.assertIsInstance(v[0][0], numpy.int32)
        self.assertIsInstance(v[0][1], numpy.int32)
        self.assertIsInstance(v[0][2], numpy.int32)
        self.assertIsInstance(v[1][0], numpy.int32)
        self.assertIsInstance(v[1][1], numpy.int32)
        self.assertIsInstance(v[1][2], numpy.int32)
        self.assertEqual(v[0][0], 1)
        self.assertEqual(v[0][1], 2)
        self.assertEqual(v[0][2], 3)
        self.assertEqual(v[1][0], 4)
        self.assertEqual(v[1][1], 5)
        self.assertEqual(v[1][2], 6)
        self.assertEqual([x for x in v[0]], [1, 2, 3])
        self.assertEqual([x for x in v[1]], [4, 5, 6])
        self.assertEqual(len(v[0]), 3)
        self.assertEqual(len(v[1]), 3)
        self.assertTrue(3 in v[0])
        self.assertFalse(7 in v[0])
        self.assertTrue(6 in v[1])
        self.assertFalse(10 in v[1])

        v[0] = [7, 8, 9]
        v[1] = [10, 11, 12]

        self.assertIs(v._data, a)
        self.assertEqual(_array_to_list(a), [[7, 8, 9], [10, 11, 12]])
        self.assertEqual(str(v), "[[7, 8, 9], [10, 11, 12]]")
        self.assertEqual(v, view(a))
        self.assertEqual(v, view(b))
        self.assertEqual(v.__eq__([[7, 8, 9], [10, 11, 12]]), NotImplemented)
        self.assertIs(v[0]._data.base, a)
        self.assertIs(v[1]._data.base, a)
        self.assertIsInstance(v[0], nani.get_element_view(view))
        self.assertIsInstance(v[1], nani.get_element_view(view))
        self.assertEqual([x for x in v], [view(a)[0], view(a)[1]])
        self.assertEqual([x for x in v], [view(b)[0], view(b)[1]])
        self.assertEqual(len(v), 2)
        self.assertTrue(7 in v)
        self.assertFalse(6 in v)

        self.assertEqual(str(v[0]), "[7, 8, 9]")
        self.assertEqual(str(v[1]), "[10, 11, 12]")
        self.assertEqual(v[0], view(a)[0])
        self.assertEqual(v[1], view(a)[1])
        self.assertEqual(v[0], view(b)[0])
        self.assertEqual(v[1], view(b)[1])
        self.assertEqual(v[0].__eq__([7, 8, 9]), NotImplemented)
        self.assertEqual(v[1].__eq__([10, 11, 12]), NotImplemented)
        self.assertIsInstance(v[0][0], numpy.int32)
        self.assertIsInstance(v[0][1], numpy.int32)
        self.assertIsInstance(v[0][2], numpy.int32)
        self.assertIsInstance(v[1][0], numpy.int32)
        self.assertIsInstance(v[1][1], numpy.int32)
        self.assertIsInstance(v[1][2], numpy.int32)
        self.assertEqual(v[0][0], 7)
        self.assertEqual(v[0][1], 8)
        self.assertEqual(v[0][2], 9)
        self.assertEqual(v[1][0], 10)
        self.assertEqual(v[1][1], 11)
        self.assertEqual(v[1][2], 12)
        self.assertEqual([x for x in v[0]], [7, 8, 9])
        self.assertEqual([x for x in v[1]], [10, 11, 12])
        self.assertEqual(len(v[0]), 3)
        self.assertEqual(len(v[1]), 3)
        self.assertTrue(7 in v[0])
        self.assertFalse(3 in v[0])
        self.assertTrue(10 in v[1])
        self.assertFalse(6 in v[1])

        v[0][0] = 1
        v[0][1] = 2
        v[0][2] = 3
        v[1][0] = 4
        v[1][1] = 5
        v[1][2] = 6

        self.assertIs(v._data, a)
        self.assertEqual(_array_to_list(a), [[1, 2, 3], [4, 5, 6]])
        self.assertEqual(str(v), "[[1, 2, 3], [4, 5, 6]]")
        self.assertEqual(v, view(a))
        self.assertNotEqual(v, view(b))
        self.assertEqual(v.__eq__([[1, 2, 3], [4, 5, 6]]), NotImplemented)
        self.assertIs(v[0]._data.base, a)
        self.assertIs(v[1]._data.base, a)
        self.assertIsInstance(v[0], nani.get_element_view(view))
        self.assertIsInstance(v[1], nani.get_element_view(view))
        self.assertEqual([x for x in v], [view(a)[0], view(a)[1]])
        self.assertNotEqual([x for x in v], [view(b)[0], view(b)[1]])
        self.assertEqual(len(v), 2)
        self.assertTrue(6 in v)
        self.assertFalse(7 in v)

        self.assertEqual(str(v[0]), "[1, 2, 3]")
        self.assertEqual(str(v[1]), "[4, 5, 6]")
        self.assertEqual(v[0], view(a)[0])
        self.assertEqual(v[1], view(a)[1])
        self.assertNotEqual(v[0], view(b)[0])
        self.assertNotEqual(v[1], view(b)[1])
        self.assertEqual(v[0].__eq__([1, 2, 3]), NotImplemented)
        self.assertEqual(v[1].__eq__([4, 5, 6]), NotImplemented)
        self.assertIsInstance(v[0][0], numpy.int32)
        self.assertIsInstance(v[0][1], numpy.int32)
        self.assertIsInstance(v[0][2], numpy.int32)
        self.assertIsInstance(v[1][0], numpy.int32)
        self.assertIsInstance(v[1][1], numpy.int32)
        self.assertIsInstance(v[1][2], numpy.int32)
        self.assertEqual(v[0][0], 1)
        self.assertEqual(v[0][1], 2)
        self.assertEqual(v[0][2], 3)
        self.assertEqual(v[1][0], 4)
        self.assertEqual(v[1][1], 5)
        self.assertEqual(v[1][2], 6)
        self.assertEqual([x for x in v[0]], [1, 2, 3])
        self.assertEqual([x for x in v[1]], [4, 5, 6])
        self.assertEqual(len(v[0]), 3)
        self.assertEqual(len(v[1]), 3)
        self.assertTrue(3 in v[0])
        self.assertFalse(7 in v[0])
        self.assertTrue(6 in v[1])
        self.assertFalse(10 in v[1])

    def test_array_view_2(self):
        data_type = nani.Number(type=numpy.uint8, view=_flag.Flag)
        self.assertTrue(nani.validate(data_type))

        dtype, _, view = nani.resolve(data_type)
        a = numpy.array([_flag.NOTHING, _flag.NOTHING], dtype=dtype)
        b = numpy.array([_flag.SOMETHING, _flag.WHATEVER], dtype=dtype)
        v = view(a)

        self.assertIs(v._data, a)
        self.assertEqual(_array_to_list(a), [_flag.NOTHING, _flag.NOTHING])
        self.assertEqual(str(v), "[NOTHING, NOTHING]")
        self.assertEqual(v, view(a))
        self.assertNotEqual(v, view(b))
        self.assertEqual(v.__eq__([_flag.NOTHING, _flag.NOTHING]), NotImplemented)
        self.assertIs(v[0]._data, a)
        self.assertIs(v[1]._data, a)
        self.assertIsInstance(v[0], _flag.Flag)
        self.assertIsInstance(v[1], _flag.Flag)
        self.assertEqual(v[0], _flag.NOTHING)
        self.assertEqual(v[1], _flag.NOTHING)
        self.assertEqual([x for x in v], [_flag.NOTHING, _flag.NOTHING])
        self.assertEqual(len(v), 2)
        self.assertTrue(_flag.NOTHING in v)
        self.assertFalse(_flag.SOMETHING in v)

        v[0] = _flag.SOMETHING
        v[1] = _flag.WHATEVER

        self.assertIs(v._data, a)
        self.assertEqual(_array_to_list(a), [_flag.SOMETHING, _flag.WHATEVER])
        self.assertEqual(str(v), "[SOMETHING, WHATEVER]")
        self.assertEqual(v, view(a))
        self.assertEqual(v, view(b))
        self.assertEqual(v.__eq__([_flag.SOMETHING, _flag.WHATEVER]), NotImplemented)
        self.assertIs(v[0]._data, a)
        self.assertIs(v[1]._data, a)
        self.assertIsInstance(v[0], _flag.Flag)
        self.assertIsInstance(v[1], _flag.Flag)
        self.assertEqual(v[0], _flag.SOMETHING)
        self.assertEqual(v[1], _flag.WHATEVER)
        self.assertEqual([x for x in v], [_flag.SOMETHING, _flag.WHATEVER])
        self.assertEqual(len(v), 2)
        self.assertTrue(_flag.SOMETHING in v)
        self.assertFalse(_flag.NOTHING in v)

    def test_structured_view(self):
        data_type = nani.Structure(
            fields=[
                ('position', _vector2.VECTOR2_TYPE),
                ('velocity', _vector2.VECTOR2_TYPE),
            ],
            name='Particle'
        )
        dtype, _, view = nani.resolve(data_type, name='Particles')
        self.assertTrue(nani.validate(data_type))

        a = numpy.array([([1.0, 2.0], [3.0, 4.0]), ([5.0, 6.0], [7.0, 8.0])], dtype=dtype)
        b = numpy.array([([8.0, 7.0], [6.0, 5.0]), ([4.0, 3.0], [2.0, 1.0])], dtype=dtype)
        v = view(a)

        self.assertIs(v._data, a)
        self.assertEqual(_array_to_list(a), [([1.0, 2.0], [3.0, 4.0]), ([5.0, 6.0], [7.0, 8.0])])
        self.assertEqual(str(v), "[Particle(position=(1.0, 2.0), velocity=(3.0, 4.0)), Particle(position=(5.0, 6.0), velocity=(7.0, 8.0))]")
        self.assertEqual(v, view(a))
        self.assertNotEqual(v, view(b))
        self.assertEqual(v.__eq__([([1.0, 2.0], [3.0, 4.0]), ([5.0, 6.0], [7.0, 8.0])]), NotImplemented)
        self.assertIsInstance(v[0], nani.get_element_view(view))
        self.assertIsInstance(v[1], nani.get_element_view(view))
        self.assertEqual([x for x in v], [view(a)[0], view(a)[1]])
        self.assertNotEqual([x for x in v], [view(b)[0], view(b)[1]])
        self.assertEqual(len(v), 2)

        self.assertEqual(str(v[0]), "Particle(position=(1.0, 2.0), velocity=(3.0, 4.0))")
        self.assertEqual(str(v[1]), "Particle(position=(5.0, 6.0), velocity=(7.0, 8.0))")
        self.assertEqual(v[0], view(a)[0])
        self.assertEqual(v[1], view(a)[1])
        self.assertNotEqual(v[0], view(b)[0])
        self.assertNotEqual(v[1], view(b)[1])
        self.assertEqual(v[0].__eq__(([1.0, 2.0], [3.0, 4.0])), NotImplemented)
        self.assertEqual(v[1].__eq__(([5.0, 6.0], [7.0, 7.0])), NotImplemented)
        self.assertIsInstance(v[0].position, _vector2.Vector2View)
        self.assertIsInstance(v[0].velocity, _vector2.Vector2View)
        self.assertIsInstance(v[1].position, _vector2.Vector2View)
        self.assertIsInstance(v[1].velocity, _vector2.Vector2View)
        self.assertEqual(v[0].position.x, 1.0)
        self.assertEqual(v[0].position.y, 2.0)
        self.assertEqual(v[0].velocity.x, 3.0)
        self.assertEqual(v[0].velocity.y, 4.0)
        self.assertEqual(v[1].position.x, 5.0)
        self.assertEqual(v[1].position.y, 6.0)
        self.assertEqual(v[1].velocity.x, 7.0)
        self.assertEqual(v[1].velocity.y, 8.0)

        v[0].position.x = 8.0
        v[0].position.y = 7.0
        v[0].velocity.x = 6.0
        v[0].velocity.y = 5.0
        v[1].position.x = 4.0
        v[1].position.y = 3.0
        v[1].velocity.x = 2.0
        v[1].velocity.y = 1.0

        self.assertIs(v._data, a)
        self.assertEqual(_array_to_list(a), [([8.0, 7.0], [6.0, 5.0]), ([4.0, 3.0], [2.0, 1.0])])
        self.assertEqual(str(v), "[Particle(position=(8.0, 7.0), velocity=(6.0, 5.0)), Particle(position=(4.0, 3.0), velocity=(2.0, 1.0))]")
        self.assertEqual(v, view(a))
        self.assertEqual(v, view(b))
        self.assertEqual(v.__eq__([([8.0, 7.0], [6.0, 5.0]), ([4.0, 3.0], [2.0, 1.0])]), NotImplemented)
        self.assertIsInstance(v[0], nani.get_element_view(view))
        self.assertIsInstance(v[1], nani.get_element_view(view))
        self.assertEqual([x for x in v], [view(a)[0], view(a)[1]])
        self.assertEqual([x for x in v], [view(b)[0], view(b)[1]])
        self.assertEqual(len(v), 2)

        self.assertEqual(str(v[0]), "Particle(position=(8.0, 7.0), velocity=(6.0, 5.0))")
        self.assertEqual(str(v[1]), "Particle(position=(4.0, 3.0), velocity=(2.0, 1.0))")
        self.assertEqual(v[0], view(a)[0])
        self.assertEqual(v[1], view(a)[1])
        self.assertEqual(v[0], view(b)[0])
        self.assertEqual(v[1], view(b)[1])
        self.assertEqual(v[0].__eq__(([8.0, 7.0], [6.0, 5.0])), NotImplemented)
        self.assertEqual(v[1].__eq__(([4.0, 3.0], [2.0, 1.0])), NotImplemented)
        self.assertIsInstance(v[0].position, _vector2.Vector2View)
        self.assertIsInstance(v[0].velocity, _vector2.Vector2View)
        self.assertIsInstance(v[1].position, _vector2.Vector2View)
        self.assertIsInstance(v[1].velocity, _vector2.Vector2View)
        self.assertEqual(v[0].position.x, 8.0)
        self.assertEqual(v[0].position.y, 7.0)
        self.assertEqual(v[0].velocity.x, 6.0)
        self.assertEqual(v[0].velocity.y, 5.0)
        self.assertEqual(v[1].position.x, 4.0)
        self.assertEqual(v[1].position.y, 3.0)
        self.assertEqual(v[1].velocity.x, 2.0)
        self.assertEqual(v[1].velocity.y, 1.0)


if __name__ == '__main__':
    from tests.run import run
    run('__main__')
