# GROUP-5 - lab 2 - variant 5

This is an **immutable set implementation** based on a hash table with
**open addressing** (linear probing).

All operations return a **new set** and do not modify the original one.
The set supports `None` as a valid element and uses tombstone markers for deletion.

## Project structure

- `hashmap_open_address_set.py` -- Immutable set implementation.
- `test_hashmap_open_address_set.py` -- Unit tests.

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
  - `cons`
  - `remove`
  - `member`
  - `length`
  - `from_list`
  - `to_list`
  - `filter`
  - `map`
  - `reduce`
  - `concat`
  - `intersection`
  - `empty`
  - iterator

- Du Huilin -- Testing and documentation:
  - unit tests
  - test coverage
  - `README.md`
  - project structure

## Changelog

- 29.04.2026 - 1
  - Implement immutable set for Lab 2.
  - Add support for `None` using sentinel `_EMPTY`.
  - Add full test suite for immutable version.

- 29.04.2026 - 0
  - Initial Lab 2 setup.

## Design notes

- Sentinel objects: `_EMPTY` and `_DELETED` are used to distinguish free
  slots, deleted slots, and actual `None` values. Using `None` as empty would
  conflict with storing `None` as a valid element.

- Open addressing with linear probing: collisions are resolved by probing
  the next available slot.

- Deletion: removed elements are marked with `_DELETED` to preserve probe chains.

- Resize policy: when load factor exceeds 0.7, the table size is doubled.

- Immutability: operations do not modify the original structure.
  Instead, a new set with an updated table is returned.

- Map implementation: results are inserted into a new set to maintain
  uniqueness and avoid duplicates.