# GROUP-5 - lab 2 - variant 5

This is an **immutable set implementation** based on a hash table with
**open addressing** (linear probing).

All operations return a **new set** and do not modify the original one.
The set supports `None` as a valid element and uses tombstone markers for deletion.

## Project structure

- hashmap_open_address_set.py -- Immutable set implementation.
- test_hashmap_open_address_set.py -- Unit tests.

## Features

- Immutable operations (`cons`, `remove`) returning new sets
- Membership test and size
- Convert to/from Python list
- Functional operations: `map`, `filter`, `reduce`
- Iterator support
- Monoid: `empty()` and `concat()`
- Set operation: `intersection`
- Handles `None` correctly
- Automatic resize when load factor > 0.7
- Open addressing with linear probing

## Contribution

- Luo Mengyao -- Core implementation:
    - immutable set structure
    - open addressing logic
    - probing
    - resize policy
    - cons
    - remove
    - member
    - length
    - from_list
    - to_list
    - filter
    - map
    - reduce
    - concat
    - intersection
    - empty
    - iterator

- Du Huilin -- Testing and documentation:
    - unit tests
    - test coverage
    - README.md
    - project structure

## Changelog

- 29.04.2026 - 1
    - Implement immutable set for Lab 2
    - Add support for None using sentinel _EMPTY
    - Add full test suite

- 29.04.2026 - 0
    - Initial setup

## Design notes

- Sentinel objects: _EMPTY and _DELETED distinguish empty slots, deleted slots,
  and actual None values.

- Open addressing with linear probing is used for collision resolution.

- Deletion uses _DELETED to preserve probing chains.

- Resize policy: when load factor exceeds 0.7, the table size is doubled.

- Immutability: operations create new sets instead of modifying existing ones.

- Map implementation ensures uniqueness by inserting into a new set.
