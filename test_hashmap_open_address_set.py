import unittest
from typing import Optional, List

from hashmap_open_address_set import (
    HashMapOpenAddressSet,
    empty, cons, remove, member, length, from_list, to_list,
    intersection, concat, filter, map_set, reduce
)

from hypothesis import given
from hypothesis.strategies import lists, integers


class TestHashMapOpenAddressSet(unittest.TestCase):

    def test_empty_and_cons(self) -> None:
        s: HashMapOpenAddressSet[Optional[int]] = empty()
        assert str(s) == "{}"
        s = cons(None, s)
        assert str(s) in ["{None}"]
        assert member(None, s)

    def test_length_and_remove(self) -> None:
        s: HashMapOpenAddressSet[Optional[int]] = from_list([1, None])
        assert length(s) == 2
        s = remove(s, 1)
        assert str(s) in ["{None}"]
        s = remove(s, None)
        assert length(s) == 0
        assert str(s) == "{}"

    def test_membership(self) -> None:
        s: HashMapOpenAddressSet[int] = from_list([1, 2, 3])
        assert member(1, s)
        assert not member(4, s)
        assert not member(None, s)

    def test_intersection(self) -> None:
        a: HashMapOpenAddressSet[int] = from_list([1, 2, 3])
        b: HashMapOpenAddressSet[int] = from_list([2, 3, 4])
        result: HashMapOpenAddressSet[int] = intersection(a, b)
        assert to_list(result) == [2, 3]

    def test_concat(self) -> None:
        a: HashMapOpenAddressSet[int] = from_list([1, 2])
        b: HashMapOpenAddressSet[int] = from_list([3, 4])
        result: HashMapOpenAddressSet[int] = concat(a, b)
        assert to_list(result) == [1, 2, 3, 4]

    def test_filter(self) -> None:
        s: HashMapOpenAddressSet[int] = from_list([1, 2, 3, 4])
        even: HashMapOpenAddressSet[int] = filter(s, lambda x: x % 2 == 0)
        assert to_list(even) == [2, 4]

    def test_map_set(self) -> None:
        s: HashMapOpenAddressSet[int] = from_list([1, 2, 3])
        mapped: HashMapOpenAddressSet[int] = map_set(s, lambda x: x + 1)
        assert to_list(mapped) == [2, 3, 4]

    def test_reduce(self) -> None:
        s: HashMapOpenAddressSet[int] = from_list([1, 2, 3, 4])
        total: int = reduce(s, lambda acc, x: acc + x, 0)
        assert total == 10

    def test_none_element(self) -> None:
        s: HashMapOpenAddressSet[Optional[int]] = from_list([None])
        assert length(s) == 1
        assert member(None, s)
        assert to_list(s) == [None]

    def test_resize_behavior(self) -> None:
        num_elements: int = 50
        elements: List[int] = list(range(num_elements))
        s: HashMapOpenAddressSet[int] = empty()
        for elem in elements:
            s = cons(elem, s)

        assert length(s) == num_elements

        for elem in elements:
            assert member(elem, s), f"Element {elem} missing after insert"

        assert to_list(s) == list(set(elements))

    @given(lists(integers()), lists(integers()), lists(integers()))
    def test_monoid_identity_and_associativity(
        self,
        xs1: List[int],
        xs2: List[int],
        xs3: List[int]
    ) -> None:
        set_a: HashMapOpenAddressSet[int] = from_list(xs1)
        set_b: HashMapOpenAddressSet[int] = from_list(xs2)
        set_c: HashMapOpenAddressSet[int] = from_list(xs3)

        assert concat(empty(), set_a) == set_a
        assert concat(set_a, empty()) == set_a

        left_temp: HashMapOpenAddressSet[int] = concat(set_a, set_b)
        left_result: HashMapOpenAddressSet[int] = concat(left_temp, set_c)

        right_temp: HashMapOpenAddressSet[int] = concat(set_b, set_c)
        right_result: HashMapOpenAddressSet[int] = concat(set_a, right_temp)

        assert left_result == right_result


if __name__ == "__main__":
    unittest.main()
