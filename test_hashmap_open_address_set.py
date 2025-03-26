import itertools
from hashmap_open_address_set import (
    HashMapOpenAddressSet,
    concat,
    cons,
    from_list,
    intersection,
    length,
    member,
    remove,
    to_list,
    filter,
    map,
    reduce,
    empty,
)


def test_api():
    print("Running tests...")

    # Test basic set operations and string representation
    empty_set = empty()
    assert str(cons(None, empty_set)) == "{None}"
    print("Basic cons operation test passed")

    l1 = cons(None, cons(1, empty_set))
    l2 = cons(1, cons(None, empty_set))

    assert str(empty_set) == "{}"
    assert str(l1) == "{None, 1}" or str(l1) == "{1, None}"
    assert empty_set != l1
    assert empty_set != l2
    assert l1 == l2
    assert l1 == cons(None, cons(1, l1))
    print("String representation and equality tests passed")

    # Test length function
    assert length(empty_set) == 0
    print(f"l1 length: {length(l1)}")
    print(f"l1 content: {str(l1)}")
    assert length(l1) == 2
    assert length(l2) == 2
    print("Length tests passed")

    # Test remove operation
    assert str(remove(l1, None)) == "{1}"
    assert str(remove(l1, 1)) == "{None}"
    print("Remove operation tests passed")

    # Test membership
    assert not member(None, empty_set)
    assert member(None, l1)
    assert member(1, l1)
    assert not member(2, l1)
    print("Membership tests passed")

    # Test intersection
    assert intersection(l1, l2) == l1
    assert intersection(l1, l2) == l2
    assert intersection(l1, empty_set) == empty_set
    assert intersection(l1, cons(None, empty_set)) == cons(None, empty_set)
    print("Intersection tests passed")

    # Test conversion to/from list
    assert to_list(l1) == [None, 1] or to_list(l1) == [1, None]
    assert l1 == from_list([None, 1])
    assert l1 == from_list([1, None, 1])
    print("List conversion tests passed")

    # Test concatenation
    assert concat(l1, l2) == from_list([None, 1, 1, None])
    print("Concatenation test passed")

    # Test iteration
    buf = []
    for e in l1:
        buf.append(e)
    assert buf in map(list, itertools.permutations([1, None]))
    print("Iteration test passed")

    # Test complete element coverage
    lst = to_list(l1) + to_list(l2)
    for e in l1:
        lst.remove(e)
    for e in l2:
        lst.remove(e)
    assert lst == []
    print("Element coverage test passed")

    # Test filter function
    def is_even(x):
        return x % 2 == 0 if x is not None else False

    l3 = from_list([1, 2, 3, 4, 5, 6])
    filtered = filter(l3, is_even)
    assert to_list(filtered) == [2, 4, 6] or to_list(filtered) == [4, 6, 2] or \
           to_list(filtered) == [2, 6, 4] or to_list(filtered) == [4, 2, 6] or \
           to_list(filtered) == [6, 2, 4] or to_list(filtered) == [6, 4, 2]
    print("Filter test passed")

    # Test map function
    def increment(x):
        return x + 1 if x is not None else None

    mapped = map(l3, increment)
    assert to_list(mapped) == [2, 3, 4, 5, 6, 7] or \
           sorted(to_list(mapped)) == [2, 3, 4, 5, 6, 7]
    print("Map test passed")

    # Test reduce function
    def add(acc, x):
        return acc + (x if x is not None else 0)

    total = reduce(l3, add, 0)
    assert total == 21  # 1+2+3+4+5+6
    print("Reduce test passed")

    # Test empty_set function
    assert empty_set() == empty_set
    assert length(empty_set()) == 0
    assert str(empty_set()) == "{}"
    print("empty_set function tests passed")

    print("All tests passed successfully!")


def main():
    try:
        test_api()
    except AssertionError as e:
        print(f"Test failed: {e}")
        raise
    except Exception as e:
        print(f"Error occurred: {e}")
        raise


if __name__ == "__main__":
    main()
