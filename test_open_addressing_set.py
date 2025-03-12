from hypothesis import given, strategies as st
from open_addressing_set import ImmutableOpenAddressingSet

# -----------------------
# Basic Functionality Tests
# -----------------------

def test_add():
    s = ImmutableOpenAddressingSet.empty()
    s1 = s.add(10)
    s2 = s1.add(20)
    # Ensure the new set contains the added elements
    assert s2.member(10) is True
    assert s2.member(20) is True
    assert s2.member(30) is False  # Non-existent element
    # Ensure the original set remains unchanged (empty)
    assert s.size == 0

def test_remove():
    s = ImmutableOpenAddressingSet.empty()
    s1 = s.add(10).add(20)
    s2 = s1.remove(10)
    assert s2.member(10) is False
    assert s2.member(20) is True
    # The original set s1 remains unaffected
    assert s1.member(10) is True

def test_size():
    s = ImmutableOpenAddressingSet.empty()
    assert s.size == 0
    s1 = s.add(10)
    s2 = s1.add(20)
    assert s2.size == 2
    s3 = s2.remove(10)
    assert s3.size == 1

def test_to_list():
    s = ImmutableOpenAddressingSet.empty()
    s1 = s.add(10)
    s2 = s1.add(20)
    assert sorted(s2.to_list()) == [10, 20]

def test_from_list():
    s = ImmutableOpenAddressingSet.from_list([1, 2, 3])
    assert s.member(1) is True
    assert s.member(2) is True
    assert s.member(3) is True
    assert s.member(4) is False

# -----------------------
# Iterator Tests
# -----------------------

def test_iterator():
    s = ImmutableOpenAddressingSet.from_list([1, 2, 3])
    result = list(iter(s))
    assert sorted(result) == [1, 2, 3]

# -----------------------
# Filter, Map, and Reduce
# -----------------------

def test_filter():
    s = ImmutableOpenAddressingSet.from_list([1, 2, 3, 4, 5])
    even_set = s.filter(lambda x: x % 2 == 0)
    assert sorted(even_set.to_list()) == [2, 4]

def test_map():
    s = ImmutableOpenAddressingSet.from_list([1, 2, 3])
    squared_set = s.map(lambda x: x ** 2)
    assert sorted(squared_set.to_list()) == [1, 4, 9]

def test_reduce():
    s = ImmutableOpenAddressingSet.from_list([1, 2, 3, 4])
    total = s.reduce(lambda acc, x: acc + x, 0)
    assert total == 10  # 1+2+3+4 = 10

# -----------------------
# Monoid (empty & concat)
# -----------------------

def test_empty():
    s = ImmutableOpenAddressingSet.empty()
    assert s.size == 0

def test_concat():
    s1 = ImmutableOpenAddressingSet.from_list([1, 2, 3])
    s2 = ImmutableOpenAddressingSet.from_list([4, 5])
    s3 = s1.concat(s2)
    assert sorted(s3.to_list()) == [1, 2, 3, 4, 5]

# -----------------------
# Handling `None` Values
# -----------------------

def test_none_value():
    s = ImmutableOpenAddressingSet.empty()
    s1 = s.add(None)
    assert s1.member(None) is True
    s2 = s1.remove(None)
    assert s2.member(None) is False

# -----------------------
# Testing Hash Set Resizing Logic
# -----------------------

def test_resize():
    # Test 1: Expansion test
    s = ImmutableOpenAddressingSet(initial_capacity=4, growth_factor=2)
    assert s.capacity == 4
    s1 = s.add(1)
    s2 = s1.add(2)
    s3 = s2.add(3)
    # After adding 3 elements, load factor 3/4 > 0.7, should trigger expansion, new capacity is 8
    assert s3.capacity == 8
    assert sorted(s3.to_list()) == [1, 2, 3]

    # Test 2: Ensure correctness after expansion
    s4 = s3.add(4)
    s5 = s4.add(5)
    s6 = s5.add(6)  # Adding the 6th element triggers expansion, capacity should be 16
    assert s6.capacity == 16
    expected = [1, 2, 3, 4, 5, 6]
    assert sorted(s6.to_list()) == expected

    # Test 3: After removing elements and expanding again, the new set should not contain removed elements
    s7 = s6.remove(3)
    s8 = s7.remove(5)

