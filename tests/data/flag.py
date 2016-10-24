SOMETHING = 1 << 0
WHATEVER = 1 << 1


class Flag(object):
    def __init__(self, data, index):
        self._data = data
        self._index = index

    def __str__(self):
        return str(self._data[self._index])

    def __int__(self):
        return int(self._data[self._index])

    def __long__(self):
        return long(self._data[self._index])

    def __and__(self, other):
        return self._data[self._index] & other

    def __xor__(self, other):
        return self._data[self._index] ^ other

    def __or__(self, other):
        return self._data[self._index] | other

    __rand__ = __and__
    __rxor__ = __xor__
    __ror__ = __or__

    def __iand__(self, other):
        self._data[self._index] &= other
        return self

    def __ixor__(self, other):
        self._data[self._index] ^= other
        return self

    def __ior__(self, other):
        self._data[self._index] |= other
        return self

    @property
    def something(self):
        return self & SOMETHING != 0

    @something.setter
    def something(self, value):
        if value:
            self |= SOMETHING
        else:
            self &= ~SOMETHING

    @property
    def whatever(self):
        return self & WHATEVER != 0

    @whatever.setter
    def whatever(self, value):
        if value:
            self |= WHATEVER
        else:
            self &= ~WHATEVER
