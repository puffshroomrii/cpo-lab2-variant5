from collections.abc import Iterator

from hypothesis import given
from hypothesis import strategies as st

from hashmap_open_address_set import (
    HashMapOpenAddressSet,
    concat,
    cons,
    empty,
    filter,
    from_list,
    intersection,
    length,
    map,
    member,
    reduce,
    remove,
    to_list,
)


@st.composite
def hash_sets(
    draw: st.DrawFn,
) -> HashMapOpenAddressSet[int]:
    values = draw(st.lists(st.integers()))
    result: HashMapOpenAddressSet[int] = empty()

    for value in values:
        result = cons(value, result)

    return result


@st.composite
def hash_set_and_values(
    draw: st.DrawFn,
) -> tuple[HashMapOpenAddressSet[int], list[int]]:
    values = draw(st.lists(st.integers()))
    result: HashMapOpenAddressSet[int] = empty()

    for value in values:
        result = cons(value, result)

    return result, values


def test_empty() -> None:
    s: HashMapOpenAddressSet[int] = empty()

    assert isinstance(s, HashMapOpenAddressSet)
    assert length(s) == 0
    assert str(s) == "{}"


def test_cons() -> None:
    s1: HashMapOpenAddressSet[int] = empty()
    s2 = cons(1, s1)

    assert length(s1) == 0
    assert length(s2) == 1
    assert member(1, s2)


def test_cons_none() -> None:
    s: HashMapOpenAddressSet[object] = empty()
    s = cons(None, s)

    assert member(None, s)
    assert length(s) == 1


def test_no_duplicates() -> None:
    s: HashMapOpenAddressSet[int] = empty()
    s = cons(1, s)
    s = cons(1, s)

    assert length(s) == 1


def test_remove() -> None:
    s1 = from_list([1, 2, 3])
    s2 = remove(s1, 2)

    assert member(2, s1)
    assert not member(2, s2)
    assert length(s1) == 3
    assert length(s2) == 2


def test_remove_missing_value() -> None:
    s1 = from_list([1, 2, 3])
    s2 = remove(s1, 100)

    assert s1 == s2


def test_member() -> None:
    s = from_list([1, 2, 3])

    assert member(1, s)
    assert member(2, s)
    assert not member(4, s)


def test_to_list() -> None:
    s = from_list([1, 2, 3])
    result = to_list(s)

    assert sorted(result) == [1, 2, 3]


def test_from_list_removes_duplicates() -> None:
    s = from_list([1, 1, 2, 2, 3])

    assert length(s) == 3
    assert member(1, s)
    assert member(2, s)
    assert member(3, s)


def test_concat() -> None:
    s1 = from_list([1, 2])
    s2 = from_list([2, 3])
    s3 = concat(s1, s2)

    assert length(s3) == 3
    assert member(1, s3)
    assert member(2, s3)
    assert member(3, s3)


def test_intersection() -> None:
    s1 = from_list([1, 2, 3])
    s2 = from_list([2, 3, 4])
    s3 = intersection(s1, s2)

    assert length(s3) == 2
    assert member(2, s3)
    assert member(3, s3)
    assert not member(1, s3)


def test_filter() -> None:
    s = from_list([1, 2, 3, 4])
    result = filter(s, lambda x: x % 2 == 0)

    assert length(result) == 2
    assert member(2, result)
    assert member(4, result)


def test_map() -> None:
    s = from_list([1, 2, 3])
    result = map(s, lambda x: x * 2)

    assert length(result) == 3
    assert member(2, result)
    assert member(4, result)
    assert member(6, result)


def test_reduce() -> None:
    s = from_list([1, 2, 3])

    def add(acc: object, x: int) -> object:
        return int(acc) + x

    result = reduce(s, add, 0)

    assert result == 6


def test_iteration() -> None:
    s = from_list([1, 2, 3])
    iterator: Iterator[int] = iter(s)
    result = list(iterator)

    assert sorted(result) == [1, 2, 3]


def test_equality() -> None:
    s1 = from_list([1, 2, 3])
    s2 = from_list([3, 2, 1])

    assert s1 == s2


def test_immutable_cons() -> None:
    s1: HashMapOpenAddressSet[int] = empty()
    s2 = cons(1, s1)

    assert length(s1) == 0
    assert length(s2) == 1


def test_immutable_remove() -> None:
    s1 = from_list([1, 2, 3])
    s2 = remove(s1, 2)

    assert member(2, s1)
    assert not member(2, s2)


@given(hash_set_and_values())
def test_pbt_from_list_length_equals_unique_count(
    data: tuple[HashMapOpenAddressSet[int], list[int]],
) -> None:
    s, values = data

    assert length(s) == len(set(values))


@given(hash_sets(), st.integers())
def test_pbt_cons_existing_value_does_not_change_size(
    s: HashMapOpenAddressSet[int],
    value: int,
) -> None:
    s_with_value = cons(value, s)
    s_with_duplicate = cons(value, s_with_value)

    assert length(s_with_value) == length(s_with_duplicate)


@given(hash_set_and_values())
def test_pbt_all_input_values_are_members(
    data: tuple[HashMapOpenAddressSet[int], list[int]],
) -> None:
    s, values = data

    for value in values:
        assert member(value, s)

    assert length(s) == len(set(values))


@given(hash_set_and_values(), hash_set_and_values())
def test_pbt_concat_contains_all_input_values(
    data1: tuple[HashMapOpenAddressSet[int], list[int]],
    data2: tuple[HashMapOpenAddressSet[int], list[int]],
) -> None:
    s1, values1 = data1
    s2, values2 = data2
    result = concat(s1, s2)

    for value in values1:
        assert member(value, result)

    for value in values2:
        assert member(value, result)

    expected = concat(s1, s2)
    assert length(result) == length(expected)


@given(hash_sets())
def test_pbt_monoid_identity(
    s: HashMapOpenAddressSet[int],
) -> None:
    assert concat(empty(), s) == s
    assert concat(s, empty()) == s


@given(hash_sets(), hash_sets(), hash_sets())
def test_pbt_monoid_associativity(
    s1: HashMapOpenAddressSet[int],
    s2: HashMapOpenAddressSet[int],
    s3: HashMapOpenAddressSet[int],
) -> None:
    left = concat(concat(s1, s2), s3)
    right = concat(s1, concat(s2, s3))

    assert left == right


@given(hash_sets(), hash_sets())
def test_pbt_intersection_contains_only_common_values(
    s1: HashMapOpenAddressSet[int],
    s2: HashMapOpenAddressSet[int],
) -> None:
    result = intersection(s1, s2)

    for item in result:
        assert member(item, s1)
        assert member(item, s2)

    for item in s1:
        if member(item, s2):
            assert member(item, result)


@given(hash_sets())
def test_pbt_filter_keeps_only_matching_values(
    s: HashMapOpenAddressSet[int],
) -> None:
    result = filter(s, lambda x: x % 2 == 0)

    for item in result:
        assert item % 2 == 0
        assert member(item, s)


@given(hash_sets())
def test_pbt_map_preserves_set_property(
    s: HashMapOpenAddressSet[int],
) -> None:
    result = map(s, lambda x: x % 10)

    for item in s:
        assert member(item % 10, result)

    assert length(result) <= 10


@given(hash_sets())
def test_pbt_reduce_sum(
    s: HashMapOpenAddressSet[int],
) -> None:
    def add(acc: object, x: int) -> object:
        return int(acc) + x

    result = reduce(s, add, 0)

    expected = 0
    for item in s:
        expected += item

    assert result == expected
