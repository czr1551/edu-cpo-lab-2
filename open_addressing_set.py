class ImmutableOpenAddressingSet:
    """
    An immutable hash set implemented using open addressing (linear probing).

    Once created, this set cannot be modified. Any modification operations
    (such as adding or removing elements) will return a new instance, keeping
    the original set unchanged.
    """

    EMPTY = object()

    def __init__(
            self,
            initial_capacity=8,
            growth_factor=2,
            buckets=None,
            size=0):
        """
        Initializes an immutable hash set.

        Parameters:
          - initial_capacity: Initial capacity of the hash table (must be a power of 2)
          - growth_factor: The factor by which the table expands when the load factor is too high
          - buckets: Internal bucket list (internal parameter, not recommended for direct use)
          - size: Current number of elements in the set (internal parameter)
        """
        if buckets is None:
            self.capacity = initial_capacity
            self.buckets = [self.EMPTY] * self.capacity
            self.size = 0
        else:
            self.capacity = len(buckets)
            self.buckets = buckets
            self.size = size
        self.growth_factor = growth_factor

    def _clone(self):
        """
        Internal method: Creates a shallow copy of the current instance, used for modifications
        without affecting the original instance.
        """
        new_buckets = self.buckets.copy()
        return ImmutableOpenAddressingSet(
            self.capacity,
            self.growth_factor,
            buckets=new_buckets,
            size=self.size)

    def _hash(self, key):
        """
        Computes the hash value of the key and maps it to a bucket index.
        """
        return hash(key) % self.capacity

    def _probe(self, key):
        """
        Linear probing: Finds the position of the key in the bucket or the first empty slot.
        """
        index = self._hash(key)
        while (self.buckets[index] is not self.EMPTY
               and self.buckets[index] != key):
            index = (index + 1) % self.capacity
        return index

    def add(self, key):
        """
        Returns a new set with the key added.
        """
        if self.member(key):
            return self
        new_set = self._clone()
        # Resize if the load factor is too high
        if (new_set.size + 1) / new_set.capacity > 0.7:
            new_set = new_set._resize()
        index = new_set._probe(key)
        if new_set.buckets[index] is self.EMPTY:
            new_set.buckets[index] = key
            new_set.size += 1
        return new_set

    def remove(self, key):
        """
        Returns a new set with the key removed.
        """
        if not self.member(key):
            return self
        new_set = self._clone()
        index = new_set._hash(key)
        while new_set.buckets[index] is not self.EMPTY:
            if new_set.buckets[index] == key:
                new_set.buckets[index] = self.EMPTY
                new_set.size -= 1
                return new_set
            index = (index + 1) % new_set.capacity
        return new_set

    def _resize(self):
        """
        Returns a new set with increased capacity and rehashed elements when the load factor is too high.
        """
        new_capacity = self.capacity * self.growth_factor
        new_buckets = [self.EMPTY] * new_capacity
        for key in self.buckets:
            if key is not self.EMPTY:
                index = hash(key) % new_capacity
                while new_buckets[index] is not self.EMPTY:
                    index = (index + 1) % new_capacity
                new_buckets[index] = key
        new_size = sum(1 for key in new_buckets if key is not self.EMPTY)
        return ImmutableOpenAddressingSet(
            new_capacity,
            self.growth_factor,
            buckets=new_buckets,
            size=new_size)

    def filter(self, predicate):
        """
        Returns a new set containing only the elements that satisfy the predicate.
        """
        new_set = ImmutableOpenAddressingSet(self.capacity, self.growth_factor)
        for key in self.buckets:
            if key is not self.EMPTY and predicate(key):
                new_set = new_set.add(key)
        return new_set

    def map(self, func):
        """
        Returns a new set where each element is transformed by the given function.
        """
        new_set = ImmutableOpenAddressingSet(self.capacity, self.growth_factor)
        for key in self.buckets:
            if key is not self.EMPTY:
                new_set = new_set.add(func(key))
        return new_set

    def reduce(self, func, initial_state):
        """
        Reduces the set elements into a single value.
        """
        state = initial_state
        for key in self.buckets:
            if key is not self.EMPTY:
                state = func(state, key)
        return state

    def member(self, key):
        """
        Checks if the key is in the set.
        """
        index = self._hash(key)
        while self.buckets[index] is not self.EMPTY:
            if self.buckets[index] == key:
                return True
            index = (index + 1) % self.capacity
        return False

    def to_list(self):
        """
        Converts the set to a list.
        """
        return [key for key in self.buckets if key is not self.EMPTY]

    @staticmethod
    def from_list(lst, initial_capacity=8, growth_factor=2):
        """
        Constructs an immutable set from a list.
        """
        new_set = ImmutableOpenAddressingSet(initial_capacity, growth_factor)
        for key in lst:
            new_set = new_set.add(key)
        return new_set

    def __iter__(self):
        self._iter_index = 0
        return self

    def __next__(self):
        while self._iter_index < self.capacity:
            key = self.buckets[self._iter_index]
            self._iter_index += 1
            if key is not self.EMPTY:
                return key
        raise StopIteration

    @staticmethod
    def empty(initial_capacity=8, growth_factor=2):
        """
        Returns an empty immutable set.
        """
        return ImmutableOpenAddressingSet(initial_capacity, growth_factor)

    def concat(self, other_set):
        """
        Returns a new set containing all elements from self and other_set (union of sets).
        """
        new_set = self
        for key in other_set.buckets:
            if key is not self.EMPTY:
                new_set = new_set.add(key)
        return new_set