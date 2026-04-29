"""Immutable set based on hash map with open addressing."""

_EMPTY = object()
_DELETED = object()


class HashMapOpenAddressSet:
    def __init__(self, values=(), capacity=8):
        self._capacity = max(capacity, 8)
        self._size = 0
        self._table = tuple([_EMPTY] * self._capacity)

        current = self
        for value in values:
            current = cons(value, current)

        self._capacity = current._capacity
        self._size = current._size
        self._table = current._table

    def __iter__(self):
        for item in self._table:
            if item is not _EMPTY and item is not _DELETED:
                yield item

    def __eq__(self, other):
        if not isinstance(other, HashMapOpenAddressSet):
            return False
        return length(self) == length(other) and all(
            member(item, other) for item in self
        )

    def __str__(self):
        if self._size == 0:
            return "{}"
        return "{" + ", ".join(str(item) for item in self) + "}"


def _index(value, capacity):
    return hash(value) % capacity


def _find_slot(value, table):
    capacity = len(table)
    index = _index(value, capacity)
    first_deleted = None

    for _ in range(capacity):
        item = table[index]

        if item is _EMPTY:
            return first_deleted if first_deleted is not None else index

        if item is _DELETED:
            if first_deleted is None:
                first_deleted = index

        elif item == value:
            return index

        index = (index + 1) % capacity

    return first_deleted


def _resize(s):
    new_set = HashMapOpenAddressSet(capacity=s._capacity * 2)
    for item in s:
        new_set = cons(item, new_set)
    return new_set


def empty():
    return HashMapOpenAddressSet()


def cons(value, s):
    if member(value, s):
        return s

    if (s._size + 1) / s._capacity > 0.7:
        s = _resize(s)

    table = list(s._table)
    index = _find_slot(value, table)
    table[index] = value

    result = HashMapOpenAddressSet(capacity=s._capacity)
    result._table = tuple(table)
    result._size = s._size + 1
    return result


def remove(s, value):
    if not member(value, s):
        return s

    table = list(s._table)
    index = _find_slot(value, table)
    table[index] = _DELETED

    result = HashMapOpenAddressSet(capacity=s._capacity)
    result._table = tuple(table)
    result._size = s._size - 1
    return result


def length(s):
    return s._size


def member(value, s):
    index = _find_slot(value, s._table)
    if index is None:
        return False

    item = s._table[index]
    return item is not _EMPTY and item is not _DELETED and item == value


def intersection(s1, s2):
    result = empty()
    for item in s1:
        if member(item, s2):
            result = cons(item, result)
    return result


def to_list(s):
    return list(s)


def from_list(values):
    result = empty()
    for value in values:
        result = cons(value, result)
    return result


def concat(s1, s2):
    result = s1
    for item in s2:
        result = cons(item, result)
    return result


def filter(s, predicate):
    result = empty()
    for item in s:
        if predicate(item):
            result = cons(item, result)
    return result


def map(s, function):
    result = empty()
    for item in s:
        result = cons(function(item), result)
    return result


def reduce(s, function, initial=None):
    items = to_list(s)

    if initial is None:
        if not items:
            raise TypeError("reduce() of empty set with no initial value")
        result = items[0]
        items = items[1:]
    else:
        result = initial

    for item in items:
        result = function(result, item)

    return result
