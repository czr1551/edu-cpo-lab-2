from hashmap_open_address_set import (
    concat,
    cons,
    from_list,
    intersection,
    length,
    member,
    remove,
    to_list,
    filter,
    map_set,
    reduce,
    empty,
)


def test_api():

    # Test basic set operations and string representation
    empty_set = empty()
    assert str(cons(None, empty_set)) == "{None}"

    l1 = cons(None, cons(1, empty_set))
    l2 = cons(1, cons(None, empty_set))

    assert str(empty_set) == "{}"
    assert str(l1) == "{None, 1}" or str(l1) == "{1, None}"
    assert empty_set != l1
    assert empty_set != l2
    assert l1 == l2
    assert l1 == cons(None, cons(1, l1))

    # Test length function
    assert length(empty_set) == 0
    assert length(l1) == 2
    assert length(l2) == 2

    # Test remove operation
    assert str(remove(l1, None)) == "{1}"
    assert str(remove(l1, 1)) == "{None}"

    # Test membership
    assert not member(None, empty_set)
    assert member(None, l1)
    assert member(1, l1)
    assert not member(2, l1)

    # Test intersection
    assert intersection(l1, l2) == l1
    assert intersection(l1, l2) == l2
    assert intersection(l1, empty_set) == empty_set
    assert intersection(l1, cons(None, empty_set)) == cons(None, empty_set)

    # Test conversion to/from list
    assert to_list(l1) == [None, 1] or to_list(l1) == [1, None]
    assert l1 == from_list([None, 1])
    assert l1 == from_list([1, None, 1])

    # Test concatenation
    assert concat(l1, l2) == from_list([None, 1, 1, None])

    # Test iteration
    buf = []
    for e in l1:
        buf.append(e)
    from itertools import permutations

    assert buf in [list(p) for p in permutations([1, None])]

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
    assert (
        to_list(filtered) == [2, 4, 6]
        or to_list(filtered) == [4, 6, 2]
        or to_list(filtered) == [2, 6, 4]
        or to_list(filtered) == [4, 2, 6]
        or to_list(filtered) == [6, 2, 4]
        or to_list(filtered) == [6, 4, 2]
    )

    # Test map function
    def increment(x):
        return x + 1 if x is not None else None

    mapped = map_set(l3, increment)
    assert (to_list(mapped) == [2, 3, 4, 5, 6, 7] or
            sorted(to_list(mapped)) == [
        2,
        3,
        4,
        5,
        6,
        7,
    ])

    # Test reduce function
    def add(acc, x):
        return acc + (x if x is not None else 0)

    total = reduce(l3, add, 0)
    assert total == 21  # 1+2+3+4+5+6

    # Test empty_set function
    assert empty() == empty()
    assert length(empty()) == 0
    assert str(empty()) == "{}"

    s = empty()
    assert s.size == 8

    for i in range(8):
        s = cons(i, s)
    assert length(s) == 8
    assert s.size == 8

    s = cons(8, s)
    assert length(s) == 9
    assert s.size == 16

    for i in range(9):
        assert member(i, s), f"Element {i} missing after resize"

    # Monoid Test

    test_set = from_list([1, 2, 3])
    assert concat(empty(), test_set) == test_set
    assert concat(test_set, empty()) == test_set

    set_a = from_list([1, 2])
    set_b = from_list([3, 4])
    set_c = from_list([5, 6])

    # (a · b) · c == a · (b · c)
    left_temp = concat(set_a, set_b)
    left_associative = concat(left_temp, set_c)

    right_temp = concat(set_b, set_c)
    right_associative = concat(set_a, right_temp)

    assert left_associative == right_associative


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
