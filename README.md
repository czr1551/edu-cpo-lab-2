# GROUP-NO DAY OFF - lab 2 - variant "Set based on hash map, open addressing"

This project implements a Set based on Hash Map (Open Addressing) and  
demonstrates mutable data structure implementation. It follows proper  
project structure and CI checks. 

## Project structure

- `open_addressing_set.py` — Implementation of the `ImmutableOpenAddressingSet`
  class with `add`, `remove`, `member`, `filter`, `map`, `reduce`,
  and other functional features.  All operations return new instances
  without modifying the original set.

- `test_open_addressing_set.py` — Unit tests and Property-Based Tests (PBT)  
  for `ImmutableOpenAddressingSet`.

## Features

- **Core functionality:**

  - `add(key)`: Returns a new set with the element added.
  - `remove(key)`: Returns a new set with the element removed.
  - `member(key)`: Check if an element exists.
  - `size`: Get the number of elements.
  - `from_list(lst)`: Create a new immutable set from a Python list.
  - `to_list()`: Convert the set to a Python list.
  - `concat(set)`: Merge two sets, returning a new set.

- **Functional operations:**

  - `filter(predicate)`: Return a new set with elements that satisfy
  the predicate.
  - `map(func)`: Apply a function to all elements and return a new set.
  - `reduce(func, initial_state)`: Aggregate values using a given function.

- **PBT:**
- `test_from_list_to_list_equality`
- `test_python_len_and_set_size_equality`
- `test_add_commutative`

- **Monoid properties:**

- `empty()`: Create an empty set.
- `concat(set)`: Combine two sets, returning a new set.

## Contribution

- `<czr61551@gmail.com>` -- Implementation of `ImmutableOpenAddressingSet`,  
  documentation.

- `<quinn_wang0416@163.com>` -- Implementation of test cases.

## Changelog

- **12.03.2025 - 0**
  - Updated implementation to use an immutable data structure design.  
    All operations now return new instances without modifying the original.

## Design notes

- Used open addressing with linear probing for collision resolution.
- Used a special marker `EMPTY` to distinguish empty slots from `None`.
- Ensured logarithmic growth factor to maintain efficient resizing.
- All operations follow immutability principles by returning new instances.
- Designed unit tests and PBT to validate properties of
  `ImmutableOpenAddressingSet`.
- Followed PEP8 and CI best practices with `pytest`, `ruff`, `mypy`,  
  and `coverage`.
