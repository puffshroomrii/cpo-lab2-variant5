"""Immutable set based on hash map with open addressing."""

from __future__ import annotations

from collections.abc import Callable, Iterable, Iterator
from typing import Generic, TypeVar

T = TypeVar("T")
U = TypeVar("U")


_EMPTY = object()
_DELETED = object()


class HashMapOpenAddressSet(Generic[T]):
    """Immutable set implemented with open addressing."""

    def __init__(
        self,
        values: Iterable[T] = (),
        capacity: int = 8,
    ) -> None:
        self._capacity = max(capacity, 8)
        self._size = 0
        self._table: tuple[object, ...] = tuple(
            [_EMPTY] * self._capacity,
        )

        current: HashMapOpenAddressSet[T] = self
        for value in values:
            current = cons(value, current)

        self._capacity = current._capacity
        self._size = current._size
        self._table = current._table

    def __iter__(self) -> Iterator[T]:
        for item in self._table:
            if item is not _EMPTY and item is not _DELETED:
                yield item  # type: ignore[misc]

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


def _index(value: object, capacity: int) -> int:
    return hash(value) % capacity


def _find_slot(
    value: object,
    table: tuple[object, ...] | list[object],
) -> int | None:
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
    value: object,
    table: tuple[object, ...] | list[object],
    index: int | None,
) -> bool:
    if index is None:
        return False

    item = table[index]
    return item is not _EMPTY and item is not _DELETED and item == value


def _insert_into_table(
    value: object,
    table: list[object],
) -> bool:
    index = _find_slot(value, table)

    if _contains_at_slot(value, table, index):
        return False

    if index is None:
        raise RuntimeError("Hash table has no free slot")

    table[index] = value
    return True


def _resize(s: HashMapOpenAddressSet[T]) -> HashMapOpenAddressSet[T]:
    new_set: HashMapOpenAddressSet[T] = HashMapOpenAddressSet(
        capacity=s._capacity * 2,
    )

    table = [_EMPTY] * new_set._capacity
    size = 0

    for item in s:
        if _insert_into_table(item, table):
            size += 1

    new_set._table = tuple(table)
    new_set._size = size
    return new_set


def empty() -> HashMapOpenAddressSet[T]:
    return HashMapOpenAddressSet()


def cons(value: T, s: HashMapOpenAddressSet[T]) -> HashMapOpenAddressSet[T]:
    index = _find_slot(value, s._table)

    if _contains_at_slot(value, s._table, index):
        return s

    if (s._size + 1) / s._capacity > 0.7:
        s = _resize(s)

    table = list(s._table)

    if _insert_into_table(value, table):
        result: HashMapOpenAddressSet[T] = HashMapOpenAddressSet(
            capacity=s._capacity,
        )
        result._table = tuple(table)
        result._size = s._size + 1
        return result

    return s


def remove(
    s: HashMapOpenAddressSet[T],
    value: T,
) -> HashMapOpenAddressSet[T]:
    index = _find_slot(value, s._table)

    if not _contains_at_slot(value, s._table, index):
        return s

    if index is None:
        return s

    table = list(s._table)
    table[index] = _DELETED

    result: HashMapOpenAddressSet[T] = HashMapOpenAddressSet(
        capacity=s._capacity,
    )
    result._table = tuple(table)
    result._size = s._size - 1
    return result


def length(s: HashMapOpenAddressSet[T]) -> int:
    return s._size


def member(value: T, s: HashMapOpenAddressSet[T]) -> bool:
    index = _find_slot(value, s._table)
    return _contains_at_slot(value, s._table, index)


def intersection(
    s1: HashMapOpenAddressSet[T],
    s2: HashMapOpenAddressSet[T],
) -> HashMapOpenAddressSet[T]:
    result: HashMapOpenAddressSet[T] = empty()

    for item in s1:
        if member(item, s2):
            result = cons(item, result)

    return result


def to_list(s: HashMapOpenAddressSet[T]) -> list[T]:
    return list(s)


def from_list(values: Iterable[T]) -> HashMapOpenAddressSet[T]:
    result: HashMapOpenAddressSet[T] = empty()

    for value in values:
        result = cons(value, result)

    return result


def concat(
    s1: HashMapOpenAddressSet[T],
    s2: HashMapOpenAddressSet[T],
) -> HashMapOpenAddressSet[T]:
    new_capacity = max(8, s1._capacity)

    while (s1._size + s2._size) / new_capacity > 0.7:
        new_capacity *= 2

    table = [_EMPTY] * new_capacity
    size = 0

    for item in s1:
        if _insert_into_table(item, table):
            size += 1

    for item in s2:
        if _insert_into_table(item, table):
            size += 1

    result: HashMapOpenAddressSet[T] = HashMapOpenAddressSet(
        capacity=new_capacity,
    )
    result._table = tuple(table)
    result._size = size
    return result


def filter(
    s: HashMapOpenAddressSet[T],
    predicate: Callable[[T], bool],
) -> HashMapOpenAddressSet[T]:
    result: HashMapOpenAddressSet[T] = empty()

    for item in s:
        if predicate(item):
            result = cons(item, result)

    return result


def map(
    s: HashMapOpenAddressSet[T],
    function: Callable[[T], U],
) -> HashMapOpenAddressSet[U]:
    result: HashMapOpenAddressSet[U] = empty()

    for item in s:
        result = cons(function(item), result)

    return result


def reduce(
    s: HashMapOpenAddressSet[T],
    function: Callable[..., object],
    initial: object | None = None,
) -> object:
    iterator = iter(s)

    if initial is None:
        try:
            result: object = next(iterator)
        except StopIteration as exc:
            raise TypeError(
                "reduce() of empty set with no initial value",
            ) from exc
    else:
        result = initial

    for item in iterator:
        result = function(result, item)

    return result
