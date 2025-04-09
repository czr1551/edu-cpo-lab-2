from typing import (
    Optional,
    Callable,
    Iterable,
    Iterator,
    List,
    Tuple,
    TypeVar,
    Generic
)

T = TypeVar('T')
U = TypeVar('U')


class HashMapOpenAddressSet(Generic[T]):
    EMPTY_SLOT = object()

    def __init__(self,
                 size: int = 8,
                 array: Optional[Iterable[object]] = None,
                 length: int = 0):
        self.size: int = size
        self.array: Tuple[object, ...] = tuple(
            array if array is not None else [self.EMPTY_SLOT] * size)
        self.length: int = length

    def __str__(self) -> str:
        elements = [str(e) for e in self.array if e is not self.EMPTY_SLOT]
        return "{" + ", ".join(sorted(elements, key=str)) + "}"

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, HashMapOpenAddressSet):
            return False
        return set(e for e in self.array if e is not self.EMPTY_SLOT) == set(
            e for e in other.array if e is not self.EMPTY_SLOT)  # type: ignore

    def __iter__(self) -> Iterator[T]:
        return (e for e in self.array if e is not self.EMPTY_SLOT)  # type: ignore

    def __hash__(self) -> int:
        return hash(
            frozenset(
                e for e in self.array if e is not self.EMPTY_SLOT))


def empty() -> HashMapOpenAddressSet[T]:
    return HashMapOpenAddressSet()


def cons(
        element: T,
        set_obj: HashMapOpenAddressSet[T]) -> HashMapOpenAddressSet[T]:
    if member(element, set_obj):
        return set_obj

    element_hash = hash(element)
    new_array = list(set_obj.array)
    inserted = False

    for i in range(set_obj.size):
        index = (element_hash + i) % set_obj.size
        if new_array[index] is set_obj.EMPTY_SLOT:
            new_array[index] = element
            inserted = True
            break

    if inserted:
        return HashMapOpenAddressSet(
            size=set_obj.size,
            array=new_array,
            length=set_obj.length + 1
        )

    new_size = set_obj.size * 2
    new_set = HashMapOpenAddressSet[T](size=new_size)
    for elem in set_obj:
        new_set = cons(elem, new_set)
    return cons(element, new_set)


def member(element: T, set_obj: HashMapOpenAddressSet[T]) -> bool:
    element_hash = hash(element)
    for i in range(set_obj.size):
        index = (element_hash + i) % set_obj.size
        if set_obj.array[index] is set_obj.EMPTY_SLOT:
            return False
        if set_obj.array[index] == element:
            return True
    return False


def remove(
        set_obj: HashMapOpenAddressSet[T],
        element: T) -> HashMapOpenAddressSet[T]:
    if not member(element, set_obj):
        return set_obj

    new_array = list(set_obj.array)
    for i in range(set_obj.size):
        index = (hash(element) + i) % set_obj.size
        if new_array[index] == element:
            new_array[index] = set_obj.EMPTY_SLOT
            return HashMapOpenAddressSet(
                size=set_obj.size,
                array=new_array,
                length=set_obj.length - 1
            )
    return set_obj


def length(set_obj: HashMapOpenAddressSet[T]) -> int:
    return set_obj.length


def from_list(lst: Iterable[T]) -> HashMapOpenAddressSet[T]:
    s: HashMapOpenAddressSet[T] = empty()
    for elem in lst:
        s = cons(elem, s)
    return s


def to_list(set_obj: HashMapOpenAddressSet[T]) -> List[T]:
    # type: ignore
    return [elem for elem in set_obj.array if elem is not set_obj.EMPTY_SLOT]


def intersection(
        set1: HashMapOpenAddressSet[T],
        set2: HashMapOpenAddressSet[T]) -> HashMapOpenAddressSet[T]:
    smaller, larger = (set1, set2) if length(
        set1) < length(set2) else (set2, set1)
    result: HashMapOpenAddressSet[T] = empty()
    for elem in smaller:
        if member(elem, larger):
            result = cons(elem, result)
    return result


def concat(
        set1: HashMapOpenAddressSet[T],
        set2: HashMapOpenAddressSet[T]) -> HashMapOpenAddressSet[T]:
    smaller, larger = (set1, set2) if length(
        set1) < length(set2) else (set2, set1)
    result: HashMapOpenAddressSet[T] = larger
    for elem in smaller:
        if not member(elem, result):
            result = cons(elem, result)
    return result


def find(set_obj: HashMapOpenAddressSet[T],
         predicate: Callable[[T],
                             bool]) -> Optional[T]:
    for elem in set_obj:
        if predicate(elem):
            return elem
    return None


def filter(set_obj: HashMapOpenAddressSet[T], predicate: Callable[[
           T], bool]) -> HashMapOpenAddressSet[T]:
    result: HashMapOpenAddressSet[T] = empty()
    for elem in set_obj:
        if predicate(elem):
            result = cons(elem, result)
    return result


def map_set(set_obj: HashMapOpenAddressSet[T], func: Callable[[
            T], U]) -> HashMapOpenAddressSet[U]:
    result: HashMapOpenAddressSet[U] = empty()
    for elem in set_obj:
        result = cons(func(elem), result)
    return result


def reduce(set_obj: HashMapOpenAddressSet[T], func: Callable[[
           U, T], U], initial: Optional[U] = None) -> U:
    it = iter(set_obj)
    if initial is None:
        try:
            initial = next(it)  # type: ignore
        except StopIteration:
            raise TypeError("reduce() of empty sequence with no initial value")

    acc = initial
    for elem in it:
        acc = func(acc, elem)  # type: ignore
    return acc


def iterator(set_obj: HashMapOpenAddressSet[T]) -> Iterator[T]:
    return iter(set_obj)
