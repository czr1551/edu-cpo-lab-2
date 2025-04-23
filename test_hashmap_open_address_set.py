import unittest
from hashmap_open_address_set import (
    empty, cons, remove, member, length, from_list, to_list,
    intersection, concat, filter, map_set, reduce
)
from hypothesis import given
from hypothesis.strategies import lists, integers


class TestHashMapOpenAddressSet(unittest.TestCase):

    def test_empty_and_cons(self):
        s = empty()
        assert str(s) == "{}"
        s = cons(None, s)
        assert str(s) in ["{None}"]
        assert member(None, s)

    def test_length_and_remove(self):
        s = from_list([1, None])
        assert length(s) == 2
        s = remove(s, 1)
        assert str(s) in ["{None}"]
        s = remove(s, None)
        assert length(s) == 0
        assert str(s) == "{}"

    def test_membership(self):
        s = from_list([1, 2, 3])
        assert member(1, s)
        assert not member(4, s)
        assert not member(None, s)

    def test_intersection(self):
        a = from_list([1, 2, 3])
        b = from_list([2, 3, 4])
        result = intersection(a, b)
        assert to_list(result) == [2, 3]

    def test_concat(self):
        a = from_list([1, 2])
        b = from_list([3, 4])
        result = concat(a, b)
        assert to_list(result) == [1, 2, 3, 4]

    def test_filter(self):
        s = from_list([1, 2, 3, 4])
        even = filter(s, lambda x: x % 2 == 0)
        assert to_list(even) == [2, 4]

    def test_map_set(self):
        s = from_list([1, 2, 3])
        mapped = map_set(s, lambda x: x + 1)
        assert to_list(mapped) == [2, 3, 4]

    def test_reduce(self):
        s = from_list([1, 2, 3, 4])
        total = reduce(s, lambda acc, x: acc + x, 0)
        assert total == 10

    def test_none_element(self):
        s = from_list([None])
        assert length(s) == 1
        assert member(None, s)
        assert to_list(s) == [None]

    def test_resize_behavior(self):
        num_elements = 50
        elements = list(range(num_elements))
        s = empty()
        for elem in elements:
            s = cons(elem, s)

        assert length(s) == num_elements

        for elem in elements:
            assert member(elem, s), f"Element {elem} missing after insert"

        unique_elements = set(elements)
        assert to_list(s) == list(unique_elements)

    @given(lists(integers()), lists(integers()), lists(integers()))
    def test_monoid_identity_and_associativity(self, xs1, xs2, xs3):
        set_a = from_list(xs1)
        set_b = from_list(xs2)
        set_c = from_list(xs3)

        assert concat(empty(), set_a) == set_a
        assert concat(set_a, empty()) == set_a

        left_temp = concat(set_a, set_b)
        left_result = concat(left_temp, set_c)

        right_temp = concat(set_b, set_c)
        right_result = concat(set_a, right_temp)

        assert left_result == right_result


if __name__ == "__main__":
    unittest.main()
