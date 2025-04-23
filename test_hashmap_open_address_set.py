import unittest, cast
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
        self.assertEqual(str(s), "{}")
        s = cons(None, s)
        self.assertIn(str(s), ["{None}"])
        self.assertTrue(member(None, s))

    def test_length_and_remove(self) -> None:
        s: HashMapOpenAddressSet[Optional[int]] = from_list([1, None])
        self.assertEqual(length(s), 2)
        s = remove(s, 1)
        self.assertIn(str(s), ["{None}"])
        s = remove(s, None)
        self.assertEqual(length(s), 0)
        self.assertEqual(str(s), "{}")

    def test_membership(self) -> None:
        s: HashMapOpenAddressSet[int] = from_list([1, 2, 3])
        self.assertTrue(member(1, s))
        self.assertFalse(member(4, s))
        self.assertFalse(member(cast(Optional[int], None), s))

    def test_intersection(self) -> None:
        a: HashMapOpenAddressSet[int] = from_list([1, 2, 3])
        b: HashMapOpenAddressSet[int] = from_list([2, 3, 4])
        result: HashMapOpenAddressSet[int] = intersection(a, b)
        self.assertCountEqual(to_list(result), [2, 3])

    def test_concat(self) -> None:
        a: HashMapOpenAddressSet[int] = from_list([1, 2])
        b: HashMapOpenAddressSet[int] = from_list([3, 4])
        result: HashMapOpenAddressSet[int] = concat(a, b)
        self.assertCountEqual(to_list(result), [1, 2, 3, 4])

    def test_filter(self) -> None:
        s: HashMapOpenAddressSet[int] = from_list([1, 2, 3, 4])
        even: HashMapOpenAddressSet[int] = filter(s, lambda x: x % 2 == 0)
        self.assertCountEqual(to_list(even), [2, 4])

    def test_map_set(self) -> None:
        s: HashMapOpenAddressSet[int] = from_list([1, 2, 3])
        mapped: HashMapOpenAddressSet[int] = map_set(s, lambda x: x + 1)
        self.assertCountEqual(to_list(mapped), [2, 3, 4])

    def test_reduce(self) -> None:
        s: HashMapOpenAddressSet[int] = from_list([1, 2, 3, 4])
        total: int = reduce(s, lambda acc, x: acc + x, 0)
        self.assertEqual(total, 10)

    def test_none_element(self) -> None:
        s: HashMapOpenAddressSet[Optional[int]] = from_list([None])
        self.assertEqual(length(s), 1)
        self.assertTrue(member(None, s))
        self.assertEqual(to_list(s), [None])

    def test_resize_behavior(self) -> None:
        num_elements: int = 50
        elements: List[int] = list(range(num_elements))
        s: HashMapOpenAddressSet[int] = empty()
        for elem in elements:
            s = cons(elem, s)

        self.assertEqual(length(s), num_elements)

        for elem in elements:
            self.assertTrue(
                member(elem, s),
                f"Element {elem} missing after insert"
            )

        self.assertCountEqual(to_list(s), list(set(elements)))

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

        self.assertEqual(concat(empty(), set_a), set_a)
        self.assertEqual(concat(set_a, empty()), set_a)

        left_result: HashMapOpenAddressSet[int] = concat(
            concat(set_a, set_b), set_c
        )
        right_result: HashMapOpenAddressSet[int] = concat(
            set_a, concat(set_b, set_c)
        )

        self.assertEqual(left_result, right_result)


if __name__ == "__main__":
    unittest.main()
