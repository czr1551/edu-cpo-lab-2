# GROUP-NO DAY OFF - lab 2 - variant "Set based on hash map, open addressing"

This project implements a Set using a Hash Map with open
addressing strategy and supports immutable-style operations
(functional programming style) even though the underlying data
structure is mutable. It demonstrates efficient hashing with
collision resolution and functional set operations.

## Project structure

- `hashmap_open_address_set.py` — Core implementation of the
  HashMapOpenAddressSet and associated functional-style
  APIs like cons, remove, map_set, reduce, etc.

- `test_hashmap_open_address_set.py` — — Comprehensive unit
  tests for all operations on HashMapOpenAddressSet,
  including functional correctness and property-based behavior.

## Features

- **Core functionality:**

  - `cons(element, set)`: Return a new set with the element
    added (does not mutate original).
  - `remove(key)`: Returns a new set with the element removed.
  - `member(element, set)`: Check if an element exists.
  - `length(set)`: Get the number of elements.
  - `from_list(lst)`: Create a new immutable set from
    a Python list.
  - `to_list()`: Convert the set to a Python list.
  - `concat(set)`: Merge two sets, returning a new set.
  - `intersection(set1, set2)`: Return a new set with elements
    common to both.

- **Functional operations:**

  - `filter(set, predicate)`:  Filter elements based on a
    predicate function.
  - `map_set(set, func)`: Apply a function to each element
    and return a new set.
  - `reduce(set, func, initial)`: Reduce the elements using a binary
    function and initial value.

- **Other Utilities:**

- `empty()`: Create an empty set.
- `iterator(set)`: Return an iterator over the set.
- `find(set, predicate)`: Return the first element that
  satisfies a predicate.

## Contribution

- `<czr61551@gmail.com>` -- Implementation of core data
  structure and helper functions.

- `<quinn_wang0416@163.com>` -- Implementation of test cases.

## Changelog

- **12.03.2025 - 0**
  - Added HashMapOpenAddressSet with open addressing using
    linear probing.
  - Introduced immutable-like APIs that return new set instances.
  - Added functional-style methods: map_set, filter, reduce, and more.
  - Complete test suite with property-based and unit tests.

## Design notes

- Collision Resolution: Uses open addressing with linear probing.
- Slot Handling: Introduced a unique EMPTY_SLOT sentinel to
  distinguish empty entries.
- Ensured logarithmic growth factor to maintain efficient resizing.
- All operations follow immutability principles by returning new instances.
- Immutability Principle: All external operations return new set
  instances, following a functional style.
- Efficiency: Dynamic resizing maintains performance with
  logarithmic growth.
