"""Immutable set based on hash map with open addressing."""

from __future__ import annotations

from collections.abc import Callable, Iterable, Iterator
from typing import Any, TypeVar, overload

T = TypeVar("T")
U = TypeVar("U")


_EMPTY = object()
_DELETED = object()


class HashMapOpenAddressSet:
    """Immutable set implemented with open addressing."""

    def __init__(
        self,
        values: Iterable[Any] = (),
        capacity: int = 8,
    ) -> None:
        self._capacity = max(capacity, 8)
        self._size = 0
        self._table: tuple[Any, ...] = tuple([_EMPTY] * self._capacity)

        current = self
        for value in values:
            current = cons(value, current)

        self._capacity = current._capacity
        self._size = current._size
        self._table = current._table

    def __iter__(self) -> Iterator[Any]:
        for item in self._table:
            if item is not _EMPTY and item is not _DELETED:
                yield item

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, HashMapOpenAddressSet):
            return False

        if self._size != other._size:
            return False

        for item in self:
            if not member(item, other):
                return False

        return True

    def __str__(self) -> str:
        if self._size == 0:
            return "{}"

        return "{" + ", ".join(str(item) for item in self) + "}"


def _index(value: Any, capacity: int) -> int:
    return hash(value) % capacity


def _find_slot(value: Any, table: tuple[Any, ...] | list[Any]) -> int | None:
    capacity = len(table)
    index = _index(value, capacity)
    first_deleted: int | None = None

    for _ in range(capacity):
        item = table[index]

        if item is _EMPTY:
            if first_deleted is not None:
                return first_deleted
            return index

        if item is _DELETED:
            if first_deleted is None:
                first_deleted = index

        elif item == value:
            return index

        index = (index + 1) % capacity

    return first_deleted


def _contains_at_slot(
    value: Any,
    table: tuple[Any, ...] | list[Any],
    index: int | None,
) -> bool:
    if index is None:
        return False

    item = table[index]
    return item is not _EMPTY and item is not _DELETED and item == value


def _resize(s: HashMapOpenAddressSet) -> HashMapOpenAddressSet:
    new_set = HashMapOpenAddressSet(capacity=s._capacity * 2)

    for item in s:
        new_set = cons(item, new_set)

    return new_set


def empty() -> HashMapOpenAddressSet:
    return HashMapOpenAddressSet()


def cons(value: Any, s: HashMapOpenAddressSet) -> HashMapOpenAddressSet:
    index = _find_slot(value, s._table)

    if _contains_at_slot(value, s._table, index):
        return s

    if (s._size + 1) / s._capacity > 0.7:
        s = _resize(s)
        index = _find_slot(value, s._table)

    if index is None:
        raise RuntimeError("Hash table has no free slot")

    table = list(s._table)
    table[index] = value

    result = HashMapOpenAddressSet(capacity=s._capacity)
    result._table = tuple(table)
    result._size = s._size + 1
    return result


def remove(
    s: HashMapOpenAddressSet,
    value: Any,
) -> HashMapOpenAddressSet:
    index = _find_slot(value, s._table)

    if not _contains_at_slot(value, s._table, index):
        return s

    if index is None:
        return s

    table = list(s._table)
    table[index] = _DELETED

    result = HashMapOpenAddressSet(capacity=s._capacity)
    result._table = tuple(table)
    result._size = s._size - 1
    return result


def length(s: HashMapOpenAddressSet) -> int:
    return s._size


def member(value: Any, s: HashMapOpenAddressSet) -> bool:
    index = _find_slot(value, s._table)
    return _contains_at_slot(value, s._table, index)


def intersection(
    s1: HashMapOpenAddressSet,
    s2: HashMapOpenAddressSet,
) -> HashMapOpenAddressSet:
    result = empty()

    for item in s1:
        if member(item, s2):
            result = cons(item, result)

    return result


def to_list(s: HashMapOpenAddressSet) -> list[Any]:
    return list(s)


def from_list(values: Iterable[Any]) -> HashMapOpenAddressSet:
    result = empty()

    for value in values:
        result = cons(value, result)

    return result


def concat(
    s1: HashMapOpenAddressSet,
    s2: HashMapOpenAddressSet,
) -> HashMapOpenAddressSet:
    result = s1

    for item in s2:
        result = cons(item, result)

    return result


def filter(
    s: HashMapOpenAddressSet,
    predicate: Callable[[Any], bool],
) -> HashMapOpenAddressSet:
    result = empty()

    for item in s:
        if predicate(item):
            result = cons(item, result)

    return result


def map(
    s: HashMapOpenAddressSet,
    function: Callable[[Any], Any],
) -> HashMapOpenAddressSet:
    result = empty()

    for item in s:
        result = cons(function(item), result)

    return result


@overload
def reduce(
    s: HashMapOpenAddressSet,
    function: Callable[[Any, Any], Any],
) -> Any:
    ...


@overload
def reduce(
    s: HashMapOpenAddressSet,
    function: Callable[[Any, Any], Any],
    initial: Any,
) -> Any:
    ...


def reduce(
    s: HashMapOpenAddressSet,
    function: Callable[[Any, Any], Any],
    initial: Any = None,
) -> Any:
    iterator = iter(s)

    if initial is None:
        try:
            result = next(iterator)
        except StopIteration as exc:
            raise TypeError(
                "reduce() of empty set with no initial value",
            ) from exc
    else:
        result = initial

    for item in iterator:
        result = function(result, item)

    return result
