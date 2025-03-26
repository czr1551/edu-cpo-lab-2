class HashMapOpenAddressSet:
    EMPTY_SLOT = object()  # 创建一个唯一的对象，代表空槽位

    def __init__(self, size=8, elements=None, length=0):
        self.size = size
        self.array = [self.EMPTY_SLOT] * size  # 用 EMPTY_SLOT 作为空槽
        self.length = length
        if elements is not None:
            for elem in elements:
                self._insert(elem)

    def _hash(self, element, i=0):
        """哈希函数 + 线性探测"""
        element_hash = hash(element)
        return (element_hash + i) % self.size

    def _insert(self, element):
        """插入元素"""
        for i in range(self.size):
            index = self._hash(element, i)
            if self.array[index] is self.EMPTY_SLOT:  # 只在空槽插入
                self.array[index] = element
                self.length += 1
                return
            if self.array[index] == element:
                return  # 已存在
        self._resize()
        self._insert(element)

    def _resize(self):
        """扩容"""
        new_size = self.size * 2
        new_array = [self.EMPTY_SLOT] * new_size  # 用 EMPTY_SLOT 替代 None
        old_array = self.array
        self.array = new_array
        self.size = new_size
        self.length = 0
        for elem in old_array:
            if elem is not self.EMPTY_SLOT:
                self._insert(elem)

    def __str__(self):
        """字符串表示"""
        elements = [str(e) for e in self.array if e is not self.EMPTY_SLOT]
        return "{" + ", ".join(sorted(elements, key=str)) + "}"

    def __eq__(self, other):
        if not isinstance(other, HashMapOpenAddressSet):
            return False
        self_elems = set(e for e in self.array if e is not self.EMPTY_SLOT)
        other_elems = set(e for e in other.array if e is not self.EMPTY_SLOT)
        return self_elems == other_elems

    def __iter__(self):
        for elem in self.array:
            if elem is not self.EMPTY_SLOT:
                yield elem


def empty():
    """返回空集合"""
    return HashMapOpenAddressSet()


def cons(element, set_obj):
    """添加元素到集合"""
    if member(element, set_obj):
        return set_obj  # 已存在，直接返回

    new_array = list(set_obj.array)  # 复制数组
    element_hash = hash(element)
    inserted = False

    for i in range(set_obj.size):
        index = (element_hash + i) % set_obj.size
        if new_array[index] is set_obj.EMPTY_SLOT:
            new_array[index] = element
            inserted = True
            break

    if not inserted:
        new_set = HashMapOpenAddressSet(size=set_obj.size * 2)
        for elem in set_obj:
            new_set = cons(elem, new_set)
        return cons(element, new_set)

    return HashMapOpenAddressSet(
        size=set_obj.size,
        elements=[e for e in new_array if e is not set_obj.EMPTY_SLOT],
        length=len([e for e in new_array if e is not set_obj.EMPTY_SLOT])
    )


def member(element, set_obj):
    """检查元素是否在集合中"""
    element_hash = hash(element)
    for i in range(set_obj.size):
        index = (element_hash + i) % set_obj.size
        if set_obj.array[index] is set_obj.EMPTY_SLOT:  # 这里修正 EMPTY_SLOT
            return False
        if set_obj.array[index] == element:
            return True
    return False


def remove(element, set_obj):
    """删除元素"""
    if not member(element, set_obj):
        return set_obj

    new_array = list(set_obj.array)
    for i in range(set_obj.size):
        index = (hash(element) + i) % set_obj.size
        if new_array[index] == element:
            new_array[index] = set_obj.EMPTY_SLOT  # 这里修正 EMPTY_SLOT
            return HashMapOpenAddressSet(
                size=set_obj.size,
                elements=[e for e in new_array if e is not set_obj.EMPTY_SLOT],
                length=set_obj.length - 1
            )
    return set_obj


def length(set_obj):
    """Return number of elements in set"""
    return set_obj.length


def from_list(lst):
    """Create set from list"""
    s = empty()
    for elem in lst:
        s = cons(elem, s)
    return s


def to_list(set_obj):
    """Convert set to list"""
    return [elem for elem in set_obj.array if elem is not None]


def intersection(set1, set2):
    """Return intersection of two sets"""
    smaller, larger = (set1, set2) if length(set1) < length(set2) else (set2, set1)
    result = empty()
    for elem in smaller:
        if member(elem, larger):
            result = cons(elem, result)
    return result


def concat(set1, set2):
    """Combine two sets"""
    smaller, larger = (set1, set2) if length(set1) < length(set2) else (set2, set1)
    result = larger
    for elem in smaller:
        if not member(elem, result):
            result = cons(elem, result)
    return result


def find(set_obj, predicate):
    """Find first element matching predicate"""
    for elem in set_obj:
        if predicate(elem):
            return elem
    return None


def filter(set_obj, predicate):
    """Filter set elements based on predicate function"""
    result = empty()
    for elem in set_obj:
        if predicate(elem):
            result = cons(elem, result)
    return result


def map(set_obj, func):
    """Apply function to each element in set"""
    result = empty()
    for elem in set_obj:
        result = cons(func(elem), result)
    return result


def reduce(set_obj, func, initial=None):
    """Reduce set elements using function"""
    acc = initial
    for elem in set_obj:
        if acc is None:
            acc = elem
        else:
            acc = func(acc, elem)
    return acc


def iterator(set_obj):
    """Return iterator for the set"""
    return iter(set_obj)
