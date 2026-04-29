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


def test_empty():
    s = empty()

    assert isinstance(s, HashMapOpenAddressSet)
    assert length(s) == 0
    assert str(s) == "{}"


def test_cons():
    s1 = empty()
    s2 = cons(1, s1)

    assert length(s1) == 0
    assert length(s2) == 1
    assert member(1, s2)


def test_cons_none():
    s = empty()
    s = cons(None, s)

    assert member(None, s)
    assert length(s) == 1


def test_no_duplicates():
    s = empty()
    s = cons(1, s)
    s = cons(1, s)

    assert length(s) == 1


def test_remove():
    s1 = from_list([1, 2, 3])
    s2 = remove(s1, 2)

    assert member(2, s1)
    assert not member(2, s2)
    assert length(s1) == 3
    assert length(s2) == 2


def test_remove_missing_value():
    s1 = from_list([1, 2, 3])
    s2 = remove(s1, 100)

    assert s1 == s2


def test_member():
    s = from_list([1, 2, 3])

    assert member(1, s)
    assert member(2, s)
    assert not member(4, s)


def test_to_list():
    s = from_list([1, 2, 3])
    result = to_list(s)

    assert sorted(result) == [1, 2, 3]


def test_from_list_removes_duplicates():
    s = from_list([1, 1, 2, 2, 3])

    assert length(s) == 3
    assert member(1, s)
    assert member(2, s)
    assert member(3, s)


def test_concat():
    s1 = from_list([1, 2])
    s2 = from_list([2, 3])
    s3 = concat(s1, s2)

    assert length(s3) == 3
    assert member(1, s3)
    assert member(2, s3)
    assert member(3, s3)


def test_intersection():
    s1 = from_list([1, 2, 3])
    s2 = from_list([2, 3, 4])
    s3 = intersection(s1, s2)

    assert length(s3) == 2
    assert member(2, s3)
    assert member(3, s3)
    assert not member(1, s3)


def test_filter():
    s = from_list([1, 2, 3, 4])
    result = filter(s, lambda x: x % 2 == 0)

    assert length(result) == 2
    assert member(2, result)
    assert member(4, result)


def test_map():
    s = from_list([1, 2, 3])
    result = map(s, lambda x: x * 2)

    assert length(result) == 3
    assert member(2, result)
    assert member(4, result)
    assert member(6, result)


def test_reduce():
    s = from_list([1, 2, 3])
    result = reduce(s, lambda acc, x: acc + x, 0)

    assert result == 6


def test_iteration():
    s = from_list([1, 2, 3])
    result = []

    for item in s:
        result.append(item)

    assert sorted(result) == [1, 2, 3]


def test_equality():
    s1 = from_list([1, 2, 3])
    s2 = from_list([3, 2, 1])

    assert s1 == s2


def test_immutable_cons():
    s1 = empty()
    s2 = cons(1, s1)

    assert length(s1) == 0
    assert length(s2) == 1


def test_immutable_remove():
    s1 = from_list([1, 2, 3])
    s2 = remove(s1, 2)

    assert member(2, s1)
    assert not member(2, s2)
