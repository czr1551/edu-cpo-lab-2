import unittest
from typing import Optional
from hashmap_open_address_set import (
    empty, cons, remove, member, length, from_list, to_list,
    intersection, concat, filter, map_set, reduce
)
from hypothesis import given
from hypothesis.strategies import lists, integers


class TestHashMapOpenAddressSet(unittest.TestCase):

    def test_empty_and_cons(self):
        s = empty()
        self.assertEqual(str(s), "{}")
        s = cons(None, s)
        self.assertIn(str(s), ["{None}"])
        self.assertTrue(member(None, s))

    def test_length_and_remove(self):
        s = from_list([1, None])
        self.assertEqual(length(s), 2)
        s = remove(s, 1)
        self.assertIn(str(s), ["{None}"])
        s = remove(s, None)
        self.assertEqual(length(s), 0)
        self.assertEqual(str(s), "{}")

    def test_membership(self):
        s = from_list([1, 2, 3])
        self.assertTrue(member(1, s))
        self.assertFalse(member(4, s))
        self.assertFalse(member(None, s))

    def test_intersection(self):
        a = from_list([1, 2, 3])
        b = from_list([2, 3, 4])
        result = intersection(a, b)
        self.assertCountEqual(to_list(result), [2, 3])

    def test_concat(self):
        a = from_list([1, 2])
        b = from_list([3, 4])
        result = concat(a, b)
        self.assertCountEqual(to_list(result), [1, 2, 3, 4])

    def test_filter(self):
        s = from_list([1, 2, 3, 4])
        even = filter(s, lambda x: x % 2 == 0)
        self.assertCountEqual(to_list(even), [2, 4])

    def test_map_set(self):
        s = from_list([1, 2, 3])
        mapped = map_set(s, lambda x: x + 1)
        self.assertCountEqual(to_list(mapped), [2, 3, 4])

    def test_reduce(self):
        s = from_list([1, 2, 3, 4])
        total = reduce(s, lambda acc, x: acc + x, 0)
        self.assertEqual(total, 10)

    def test_none_element(self):
        s = from_list([None])
        self.assertEqual(length(s), 1)
        self.assertTrue(member(None, s))
        self.assertEqual(to_list(s), [None])

    def test_resize_behavior(self):
        initial_capacity = 8  # Default initial capacity
        num_elements = 50

        elements = list(range(num_elements))
        s = empty()
        for elem in elements:
            s = cons(elem, s)

        # Check if the reported length matches the number of inserted elements
        self.assertEqual(length(s), num_elements)

        # Verify all inserted elements are present in the set
        for elem in elements:
            self.assertTrue(member(elem, s), f"Element {elem} missing after insert")

        # Verify no duplicates (set semantics)
        unique_elements = set(elements)
        self.assertCountEqual(to_list(s), list(unique_elements))

    # Property-Based Tests for Monoid Properties
    @given(lists(integers()), lists(integers()), lists(integers()))
    def test_monoid_identity_and_associativity(self, xs1, xs2, xs3):
        set_a = from_list(xs1)
        set_b = from_list(xs2)
        set_c = from_list(xs3)

        # Identity
        self.assertEqual(concat(empty(), set_a), set_a)
        self.assertEqual(concat(set_a, empty()), set_a)

        # Associativity: (a ⋅ b) ⋅ c == a ⋅ (b ⋅ c)
        left_temp = concat(set_a, set_b)
        left_result = concat(left_temp, set_c)

        right_temp = concat(set_b, set_c)
        right_result = concat(set_a, right_temp)

        self.assertEqual(left_result, right_result)


if __name__ == "__main__":
    unittest.main()
