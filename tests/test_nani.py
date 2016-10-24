import sys
import unittest

from distutils.version import StrictVersion

import numpy

import nani

from . import utils
from .data import flag
from .data import numbers
from .data import particle
from .data import subtypes
from .data import vector2


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


def _join_sequence(seq, last_separator):
    def _format(item, count, index):
        return ("{0}'{1}'".format(last_separator, item)
                if count > 1 and index == count - 1
                else "'{0}'".format(item))

    if not isinstance(seq, (list, tuple)):
        seq = (seq,)

    count = len(seq)
    return ', '.join(_format(item, count, i) for i, item in enumerate(seq))


def _join_types(seq, last_separator):
    if not isinstance(seq, (list, tuple)):
        seq = (seq,)

    class_names = ['{0}.{1}'.format(cls.__module__, cls.__name__)
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

    def test_object_constructor(self):
        data_type = nani.Object()
        self.assertEqual(data_type, (None, None))
        self.assertEqual(data_type._fields, ('default', 'view'))

    def test_number_constructor(self):
        data_type = nani.Number()
        self.assertEqual(data_type, (numpy.float_, 0, None))
        self.assertEqual(data_type._fields, ('type', 'default', 'view'))

    def test_string_constructor(self):
        self.assertRaises(TypeError, nani.String)

        data_type = nani.String(length=8)
        self.assertEqual(data_type, (8, _BuiltinString(), None))
        self.assertEqual(data_type._fields, ('length', 'default', 'view'))

    def test_unicode_constructor(self):
        self.assertRaises(TypeError, nani.Unicode)

        data_type = nani.Unicode(length=8)
        self.assertEqual(data_type, (8, _BuiltinUnicode(), None))
        self.assertEqual(data_type._fields, ('length', 'default', 'view'))

    def test_array_constructor(self):
        self.assertRaises(TypeError, nani.Array)
        self.assertRaises(TypeError, nani.Array, element_type=nani.Number())

        data_type = nani.Array(element_type=nani.Number(), shape=1)
        self.assertEqual(data_type, (nani.Number(), 1, None, None))
        self.assertEqual(data_type._fields, ('element_type', 'shape', 'name', 'view'))

    def test_structure_constructor(self):
        self.assertRaises(TypeError, nani.Structure)

        data_type = nani.Structure(fields=())
        self.assertEqual(data_type, ((), None, None))
        self.assertEqual(data_type._fields, ('fields', 'name', 'view'))

    def test_bool_valid_attributes(self):
        self.assertIsNotNone(nani.resolve(nani.Bool(default=True)))
        self.assertIsNotNone(nani.resolve(nani.Bool(default=False)))

    def test_object_valid_attributes(self):
        self.assertIsNotNone(nani.resolve(nani.Object(default=None)))
        self.assertIsNotNone(nani.resolve(nani.Object(default=123)))
        self.assertIsNotNone(nani.resolve(nani.Object(default=1.23)))
        self.assertIsNotNone(nani.resolve(nani.Object(default='abc')))
        self.assertIsNotNone(nani.resolve(nani.Object(default=[])))
        self.assertIsNotNone(nani.resolve(nani.Object(default=())))
        self.assertIsNotNone(nani.resolve(nani.Object(default={})))
        self.assertIsNotNone(nani.resolve(nani.Object(default=vector2.Vector2View)))

    def test_number_valid_attributes(self):
        self.assertIsNotNone(nani.resolve(nani.Number(type=bool, default=True)))
        self.assertIsNotNone(nani.resolve(nani.Number(type=int, default=123)))
        self.assertIsNotNone(nani.resolve(nani.Number(type=float, default=1.23)))
        self.assertIsNotNone(nani.resolve(nani.Number(type=complex, default=1 + 23j)))
        self.assertIsNotNone(nani.resolve(nani.Number(type=numpy.int32, default=123)))
        self.assertIsNotNone(nani.resolve(nani.Number(type=numpy.float32, default=1.23)))
        self.assertIsNotNone(nani.resolve(nani.Number(type=numpy.complex64, default=1 + 23j)))

        self.assertIsNotNone(nani.resolve(nani.Number(type=numbers.Bool, default=True)))
        self.assertIsNotNone(nani.resolve(nani.Number(type=numbers.Int, default=123)))
        self.assertIsNotNone(nani.resolve(nani.Number(type=numbers.Float, default=1.23)))
        self.assertIsNotNone(nani.resolve(nani.Number(type=numbers.Complex, default=1 + 23j)))
        self.assertIsNotNone(nani.resolve(nani.Number(type=numbers.NumpyInt, default=123)))
        self.assertIsNotNone(nani.resolve(nani.Number(type=numbers.NumpyFloat, default=1.23)))
        self.assertIsNotNone(nani.resolve(nani.Number(type=numbers.NumpyComplex, default=1 + 23j)))

    def test_string_valid_attributes(self):
        if _PY2:
            self.assertIsNotNone(nani.resolve(nani.String(length=8, default='abc')))
            self.assertIsNotNone(nani.resolve(nani.String(length=8, default=b'abc')))
        else:
            self.assertIsNotNone(nani.resolve(nani.String(length=8, default=b'abc')))

    def test_unicode_valid_attributes(self):
        if _PY2:
            self.assertIsNotNone(nani.resolve(nani.Unicode(length=8, default=u'abc')))
        else:
            self.assertIsNotNone(nani.resolve(nani.Unicode(length=8, default='abc')))
            self.assertIsNotNone(nani.resolve(nani.Unicode(length=8, default=u'abc')))

    def test_array_valid_attributes(self):
        self.assertIsNotNone(nani.resolve(nani.Array(element_type=nani.Bool(), shape=0)))
        self.assertIsNotNone(nani.resolve(nani.Array(element_type=nani.Object(), shape=0)))
        self.assertIsNotNone(nani.resolve(nani.Array(element_type=nani.Number(), shape=0)))
        self.assertIsNotNone(nani.resolve(nani.Array(element_type=nani.String(length=8), shape=0)))
        self.assertIsNotNone(nani.resolve(nani.Array(element_type=nani.Unicode(length=8), shape=0)))
        self.assertIsNotNone(nani.resolve(nani.Array(element_type=nani.Array(element_type=nani.Number(), shape=1), shape=0)))
        self.assertIsNotNone(nani.resolve(nani.Array(element_type=nani.Structure(fields=(('number', nani.Number()),)), shape=0)))

        self.assertIsNotNone(nani.resolve(nani.Array(element_type=nani.Bool(), shape=1)))
        self.assertIsNotNone(nani.resolve(nani.Array(element_type=nani.Object(), shape=1)))
        self.assertIsNotNone(nani.resolve(nani.Array(element_type=nani.Number(), shape=1)))
        self.assertIsNotNone(nani.resolve(nani.Array(element_type=nani.String(length=8), shape=1)))
        self.assertIsNotNone(nani.resolve(nani.Array(element_type=nani.Unicode(length=8), shape=1)))
        self.assertIsNotNone(nani.resolve(nani.Array(element_type=nani.Array(element_type=nani.Number(), shape=1), shape=1)))
        self.assertIsNotNone(nani.resolve(nani.Array(element_type=nani.Structure(fields=(('number', nani.Number()),)), shape=1)))

        self.assertIsNotNone(nani.resolve(nani.Array(element_type=nani.Bool(), shape=(0,))))
        self.assertIsNotNone(nani.resolve(nani.Array(element_type=nani.Object(), shape=(0,))))
        self.assertIsNotNone(nani.resolve(nani.Array(element_type=nani.Number(), shape=(0,))))
        self.assertIsNotNone(nani.resolve(nani.Array(element_type=nani.String(length=8), shape=(0,))))
        self.assertIsNotNone(nani.resolve(nani.Array(element_type=nani.Unicode(length=8), shape=(0,))))
        self.assertIsNotNone(nani.resolve(nani.Array(element_type=nani.Array(element_type=nani.Number(), shape=1), shape=(0,))))
        self.assertIsNotNone(nani.resolve(nani.Array(element_type=nani.Structure(fields=(('number', nani.Number()),)), shape=(0,))))

        self.assertIsNotNone(nani.resolve(nani.Array(element_type=nani.Bool(), shape=(1,))))
        self.assertIsNotNone(nani.resolve(nani.Array(element_type=nani.Object(), shape=(1,))))
        self.assertIsNotNone(nani.resolve(nani.Array(element_type=nani.Number(), shape=(1,))))
        self.assertIsNotNone(nani.resolve(nani.Array(element_type=nani.String(length=8), shape=(1,))))
        self.assertIsNotNone(nani.resolve(nani.Array(element_type=nani.Unicode(length=8), shape=(1,))))
        self.assertIsNotNone(nani.resolve(nani.Array(element_type=nani.Array(element_type=nani.Number(), shape=1), shape=(1,))))
        self.assertIsNotNone(nani.resolve(nani.Array(element_type=nani.Structure(fields=(('number', nani.Number()),)), shape=(1,))))

        self.assertIsNotNone(nani.resolve(nani.Array(element_type=nani.Bool(), shape=(1, 2))))
        self.assertIsNotNone(nani.resolve(nani.Array(element_type=nani.Object(), shape=(1, 2))))
        self.assertIsNotNone(nani.resolve(nani.Array(element_type=nani.Number(), shape=(1, 2))))
        self.assertIsNotNone(nani.resolve(nani.Array(element_type=nani.String(length=8), shape=(1, 2))))
        self.assertIsNotNone(nani.resolve(nani.Array(element_type=nani.Unicode(length=8), shape=(1, 2))))
        self.assertIsNotNone(nani.resolve(nani.Array(element_type=nani.Array(element_type=nani.Number(), shape=1), shape=(1, 2))))
        self.assertIsNotNone(nani.resolve(nani.Array(element_type=nani.Structure(fields=(('number', nani.Number()),)), shape=(1, 2))))

    def test_structure_valid_attributes(self):
        self.assertIsNotNone(nani.resolve(nani.Structure(
            fields=(
                ('number', nani.Number()),
            )
        )))
        self.assertIsNotNone(nani.resolve(nani.Structure(
            fields=(
                ('bool', nani.Bool()),
                ('string', nani.String(length=8)),
                ('array', nani.Array(element_type=nani.Number(), shape=1)),
                ('structure', nani.Structure(fields=(
                    ('unicode', nani.Unicode(length=8)),
                ))),
            )
        )))
        self.assertIsNotNone(nani.resolve(nani.Structure(
            fields=(
                ('position', vector2.VECTOR2_TYPE),
                ('velocity', vector2.VECTOR2_TYPE),
                ('targets', nani.Array(element_type=vector2.VECTOR2_TYPE, shape=1)),
                ('particle', particle.PARTICLE_TYPE),
            )
        )))
        self.assertIsNotNone(nani.resolve(nani.Structure(
            fields=(
                ('position', vector2.VECTOR2_TYPE),
                ('velocity', vector2.VECTOR2_TYPE),
                ('particle', particle.PARTICLE_TYPE),
            )
        )))

    def test_bool_invalid_attributes(self):
        self.assertRaises(TypeError, nani.resolve, nani.Bool(default=None))
        self.assertRaises(TypeError, nani.resolve, nani.Bool(default=123))
        self.assertRaises(TypeError, nani.resolve, nani.Bool(default=1.23))
        self.assertRaises(TypeError, nani.resolve, nani.Bool(default='abc'))
        self.assertRaises(TypeError, nani.resolve, nani.Bool(default=[]))
        self.assertRaises(TypeError, nani.resolve, nani.Bool(default=()))
        self.assertRaises(TypeError, nani.resolve, nani.Bool(default={}))

    def test_number_invalid_attributes(self):
        self.assertRaises(TypeError, nani.resolve, nani.Number(type=None))
        self.assertRaises(TypeError, nani.resolve, nani.Number(type=numpy.bool_))
        self.assertRaises(TypeError, nani.resolve, nani.Number(type=numpy.object_))
        self.assertRaises(TypeError, nani.resolve, nani.Number(type=numpy.string_))
        self.assertRaises(TypeError, nani.resolve, nani.Number(type=numpy.unicode_))

        self.assertRaises(TypeError, nani.resolve, nani.Number(default=None))
        self.assertRaises(TypeError, nani.resolve, nani.Number(default='abc'))
        self.assertRaises(TypeError, nani.resolve, nani.Number(default=[]))
        self.assertRaises(TypeError, nani.resolve, nani.Number(default=()))
        self.assertRaises(TypeError, nani.resolve, nani.Number(default={}))

    def test_string_invalid_attributes(self):
        self.assertRaises(TypeError, nani.resolve, nani.String(length=1.23))
        self.assertRaises(TypeError, nani.resolve, nani.String(length='abc'))
        self.assertRaises(TypeError, nani.resolve, nani.String(length=[8]))

    def test_unicode_invalid_attributes(self):
        self.assertRaises(TypeError, nani.resolve, nani.Unicode(length=1.23))
        self.assertRaises(TypeError, nani.resolve, nani.Unicode(length='abc'))
        self.assertRaises(TypeError, nani.resolve, nani.Unicode(length=[8]))

    def test_array_invalid_attributes(self):
        self.assertRaises(TypeError, nani.resolve, nani.Array(element_type=None, shape=1))
        self.assertRaises(ValueError, nani.resolve, nani.Array(element_type=nani.Array(element_type=nani.Number(), shape=0), shape=(1, 2)))

    def test_structure_invalid_attributes(self):
        self.assertRaises(ValueError, nani.resolve, nani.Structure(fields=(('duplicate', nani.Number()), ('duplicate', nani.Bool()))))

    def test_subtypes(self):
        self.assertIsNotNone(nani.resolve(subtypes.Bool()))
        self.assertIsNotNone(nani.resolve(subtypes.Object()))
        self.assertIsNotNone(nani.resolve(subtypes.Number()))
        self.assertIsNotNone(nani.resolve(subtypes.Array(element_type=nani.Number(), shape=1)))
        self.assertIsNotNone(nani.resolve(subtypes.Structure(fields=())))

    def test_without_listify(self):
        _, default, _ = nani.resolve(particle.PARTICLE_TYPE)
        self.assertEqual(default, (numpy.uint32(-1), (0.0, 0.0), 1.0, None))
        self.assertEqual(default._fields, ('id', 'position', 'mass', 'neighbours'))

    def test_with_listify(self):
        _, default, _ = nani.resolve(particle.PARTICLE_TYPE, listify_default=True)
        self.assertEqual(default, [numpy.uint32(-1), [0.0, 0.0], 1.0, None])

    def test_deep_copy(self):
        _, default, _ = nani.resolve(nani.Array(
            element_type=nani.Object(default=[]),
            shape=2
        ))
        self.assertEqual(default, ([], []))

        default[0].append('local')
        self.assertEqual(default, (['local'], []))

    def test_error_messages(self):
        with self.assertRaises(TypeError) as c:
            nani.resolve(nani.Number)

        self.assertEqual(str(c.exception), "The data type is expected to be an instance object but got the type 'nani.Number' instead.")

        with self.assertRaises(TypeError) as c:
            nani.resolve(123)

        self.assertEqual(str(c.exception), "Objects of type 'int' aren't supported as data types. Use any type from {0} instead.".format(_join_types(nani._ALL, "or ")))

        with self.assertRaises(TypeError) as c:
            nani.resolve(nani.Number(type=None))

        self.assertEqual(str(c.exception), "The attribute 'Number.type' cannot be 'None'.")

        with self.assertRaises(TypeError) as c:
            nani.resolve(nani.Number(type=123))

        self.assertEqual(str(c.exception), "The attribute 'Number.type' is expected to be a class object.")

        with self.assertRaises(TypeError) as c:
            nani.resolve(nani.Array(element_type=nani.Number(), shape=0, view=123))

        self.assertEqual(str(c.exception), "The attribute 'Array.view' is expected to be a class object or 'None'.")

        with self.assertRaises(TypeError) as c:
            nani.resolve(nani.Array(element_type=123, shape=0))

        self.assertEqual(str(c.exception), "The attribute 'Array.element_type' is expected to be an instance object of type {0}, not 'int'.".format(_join_types(nani._ALL, "or ")))

        with self.assertRaises(TypeError) as c:
            nani.resolve(nani.Number(type=str))

        self.assertEqual(str(c.exception), "The attribute 'Number.type' is expected to be a subclass of {0}, not 'str'.".format(_join_types(nani._NUMBER_TYPES, "or ")))

        with self.assertRaises(TypeError) as c:
            nani.resolve(nani.Structure(fields=('abc', 123), name='Something'))

        self.assertEqual(str(c.exception), "Each field from the attribute 'Something.fields' is expected to be a tuple but got 'str' instead.")

        with self.assertRaises(TypeError) as c:
            nani.resolve(nani.Structure(fields=(('abc',),), name='Whatever'))

        self.assertEqual(str(c.exception), "Each field from the attribute 'Whatever.fields' is expected to be a tuple compatible with 'nani.Field' but got '('abc',)' instead.")

        with self.assertRaises(TypeError) as c:
            nani.resolve(nani.Structure(fields=((1, nani.Number()),), name='Moon'))

        self.assertEqual(str(c.exception), "The first element of each field from the attribute 'Moon.fields', that is the field name, is expected to be an instance object of type {0}, not 'int'.".format(_join_types(_STRING_TYPES, "or ")))

        with self.assertRaises(TypeError) as c:
            nani.resolve(nani.Structure(fields=(('id', nani.Number),), name='Star'))

        self.assertEqual(str(c.exception), "The second element of each field from the attribute 'Star.fields', that is the field type, is expected to be an instance object of type {0}, not 'type'.".format(_join_types(nani._ALL, "or ")))

        with self.assertRaises(TypeError) as c:
            nani.resolve(nani.Structure(fields=(('id', nani.Number(), 1.23),)))

        self.assertEqual(str(c.exception), "The third element of each field from the attribute 'Structure.fields', that is the 'read_only' attribute, is expected to be an instance object of type 'bool', not 'float'.")

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
        dtype, _, view = nani.resolve(data_type)
        a = numpy.arange(10, dtype=dtype)
        v = view(a)
        self.assertIs(nani.get_data(v), a)

    def test_view(self):
        data_type = nani.Number(type=numpy.int32)
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
        particle_type = particle.PARTICLE_TYPE
        particle_count = 4
        user_default = [(i, [0, 0], 1.0, []) for i in range(particle_count)]
        expected_dtype = [
            ('id', numpy.uint32),
            ('position', numpy.float32, (2,)),
            ('mass', numpy.float32),
            ('neighbours', numpy.object_)
        ]
        expected_default = (numpy.uint32(-1), (0.0, 0.0), 1.0, None)

        dtype, default, view = nani.resolve(particle_type, name='Particles')
        self.assertEqual(dtype, expected_dtype)
        self.assertIsInstance(default, tuple)
        self.assertEqual(default, expected_default)
        self.assertEqual(view.__name__, 'Particles')

        element_view = nani.get_element_view(view)
        self.assertEqual(element_view.__name__, 'ParticleView')

        a = numpy.array(user_default, dtype=dtype)
        self.assertEqual(a.dtype, expected_dtype)
        self.assertEqual(utils.array_to_list(a), user_default)

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

        self.assertEqual(utils.array_to_list(a), [
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
            self.assertEqual(utils.array_to_list(a), [
                (0, [1.0, 2.0], 1.0, [0]),
                (2, [12.0, 16.0], 1.0, [1]),
                (4, [0, 0], 9.75, [4]),
                (6, [0, 0], 1.0, [9])
            ])
        else:
            self.assertEqual(utils.array_to_list(a), [
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
        flag_type = nani.Number(type=numpy.uint8, view=flag.Flag)
        dtype, _, view = nani.resolve(flag_type, name='Flags')
        a = numpy.zeros(4, dtype=dtype)
        a[0] |= flag.SOMETHING
        a[1] |= flag.WHATEVER
        a[2] |= flag.SOMETHING | flag.WHATEVER

        v = view(a)
        self.assertTrue(v[0].something)
        self.assertFalse(v[0].whatever)
        self.assertFalse(v[1].something)
        self.assertTrue(v[1].whatever)
        self.assertTrue(v[2].something)
        self.assertTrue(v[2].whatever)
        self.assertFalse(v[3].something)
        self.assertFalse(v[3].whatever)

        v[0] |= flag.WHATEVER
        v[1] &= ~flag.WHATEVER
        v[2] &= ~flag.WHATEVER
        v[3] |= flag.SOMETHING
        self.assertTrue(a[0] & flag.SOMETHING != 0)
        self.assertTrue(a[0] & flag.WHATEVER != 0)
        self.assertFalse(a[1] & flag.SOMETHING != 0)
        self.assertFalse(a[1] & flag.WHATEVER != 0)
        self.assertTrue(a[2] & flag.SOMETHING != 0)
        self.assertFalse(a[2] & flag.WHATEVER != 0)
        self.assertTrue(a[3] & flag.SOMETHING != 0)
        self.assertFalse(a[3] & flag.WHATEVER != 0)

        v[0].something = False
        v[1].whatever = True
        self.assertFalse(a[0] & flag.SOMETHING != 0)
        self.assertTrue(a[0] & flag.WHATEVER != 0)
        self.assertFalse(a[1] & flag.SOMETHING != 0)
        self.assertTrue(a[1] & flag.WHATEVER != 0)

        first = v[0]
        first.something = True
        first &= ~flag.WHATEVER
        self.assertTrue(a[0] & flag.SOMETHING != 0)
        self.assertFalse(a[0] & flag.WHATEVER != 0)
        first |= flag.WHATEVER
        self.assertTrue(a[0] & flag.WHATEVER != 0)

    def test_structure_flags(self):
        struct_type = nani.Structure(
            fields=(
                ('id', nani.Number(type=numpy.uint32)),
                ('flags', nani.Number(type=numpy.uint8, view=flag.Flag))
            ),
            name='Struct'
        )
        dtype, _, view = nani.resolve(struct_type)
        a = numpy.zeros(4, dtype=dtype)
        a[0]['flags'] |= flag.SOMETHING
        a[1]['flags'] |= flag.WHATEVER
        a[2]['flags'] |= flag.SOMETHING | flag.WHATEVER

        v = view(a)
        self.assertTrue(v[0].flags.something)
        self.assertFalse(v[0].flags.whatever)
        self.assertFalse(v[1].flags.something)
        self.assertTrue(v[1].flags.whatever)
        self.assertTrue(v[2].flags.something)
        self.assertTrue(v[2].flags.whatever)
        self.assertFalse(v[3].flags.something)
        self.assertFalse(v[3].flags.whatever)

        v[0].flags |= flag.WHATEVER
        v[1].flags &= ~flag.WHATEVER
        v[2].flags &= ~flag.WHATEVER
        v[3].flags |= flag.SOMETHING
        self.assertTrue(a[0]['flags'] & flag.SOMETHING != 0)
        self.assertTrue(a[0]['flags'] & flag.WHATEVER != 0)
        self.assertFalse(a[1]['flags'] & flag.SOMETHING != 0)
        self.assertFalse(a[1]['flags'] & flag.WHATEVER != 0)
        self.assertTrue(a[2]['flags'] & flag.SOMETHING != 0)
        self.assertFalse(a[2]['flags'] & flag.WHATEVER != 0)
        self.assertTrue(a[3]['flags'] & flag.SOMETHING != 0)
        self.assertFalse(a[3]['flags'] & flag.WHATEVER != 0)

        v[0].flags.something = False
        v[1].flags.whatever = True
        self.assertFalse(a[0]['flags'] & flag.SOMETHING != 0)
        self.assertTrue(a[0]['flags'] & flag.WHATEVER != 0)
        self.assertFalse(a[1]['flags'] & flag.SOMETHING != 0)
        self.assertTrue(a[1]['flags'] & flag.WHATEVER != 0)

        first = v[0].flags
        first.something = True
        first &= ~flag.WHATEVER
        self.assertTrue(a[0]['flags'] & flag.SOMETHING != 0)
        self.assertFalse(a[0]['flags'] & flag.WHATEVER != 0)
        first |= flag.WHATEVER
        self.assertTrue(a[0]['flags'] & flag.WHATEVER != 0)
