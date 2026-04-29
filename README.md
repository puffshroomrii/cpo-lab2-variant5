# GROUP-5 - lab 2 - variant 5

This is an immutable set implementation based on a hash table with
**open addressing** (linear probing).  
It supports `None` as a valid element and uses tombstone markers for deletion.  
All update operations return a new set and do not modify the original one.

## Project structure

- `hashmap_open_address_set.py` -- Immutable set implementation.
- `test_hashmap_open_address_set.py` -- Unit tests.

## Features

- Immutable `cons` and `remove` operations
- Membership test, length
- Convert to/from Python list
- Functional `filter` and `map`
- Reduce (fold) over elements
- Iterator support
- Monoid: `empty()` and `concat()`
- Set operation: `intersection()`
- Handles `None` correctly
- Automatic resize when load factor > 0.7

## Contribution

- Luo Mengyao – Core implementation: `HashMapOpenAddressSet` class, open
  addressing logic, tombstone handling, resize policy, `cons`, `remove`,
  `member`, `length`, `from_list`, `to_list`, `filter`, `map`, `reduce`,
  `concat`, `intersection`, `empty`, iterator.
- Du Huilin – Testing and documentation: unit tests, test coverage,
  `README.md` (project description, design notes, changelog), and GitHub
  Actions configuration.

## Changelog

- 29.04.2026 - 1
   - Add immutable set implementation.
   - Add unit tests for lab 2.
   - Update README for lab 2.
- 29.04.2026 - 0
   - Initial

## Design notes

- Sentinel objects: `_EMPTY` and `_DELETED` are used to distinguish free
  slots, deleted slots, and actual `None` values. Using `None` as empty would
  conflict with storing `None` as a valid element.
- Open addressing with linear probing: Simple to implement and cache-friendly.
  Deletion marks a slot as `_DELETED` to keep probe chains intact for future
  lookups.
- Resize policy: When load factor exceeds 0.7, the table size is doubled.
- Immutable operations: `cons`, `remove`, `filter`, `map`, `concat`, and
  `intersection` return new sets instead of modifying the original set.
- Map implementation: Mapped values are inserted into a new set, so duplicate
  results are removed and the set property is preserved.
