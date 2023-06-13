from referential_array import ArrayR
from abstract_list import List, T


class ArrayList(List[T]):
    MIN_CAPACITY = 1

    def __init__(self, max_capacity: int) -> None:
        List.__init__(self)
        self.array = ArrayR(max(self.MIN_CAPACITY, max_capacity))

    def reset(self):
        List.__init__(self)

    def __getitem__(self, index: int) -> T:
        return self.array[index]

    def __setitem__(self, index: int, value: T) -> None:
        self.array[index] = value

    def __contains__(self, item):
        for i in range(len(self)):
            if self.array[i] == item:
                return True
        return False

    def __shuffle_right(self, index: int) -> None:
        for i in range(len(self), index, -1):
            self.array[i] = self.array[i - 1]

    def __shuffle_left(self, index: int) -> None:
        if len(self) < 0:
            raise Exception("Out of bounds")
        for i in range(index, len(self)):
            self.array[i] = self.array[i + 1]

    def __newsize(self) -> int:
        length = len(self)
        if length > 8:
            new_length = length + (length >> 3) + (4 if length < 9 else 7)
        else:
            new_length = 2 * length

        return new_length

    def __resize(self) -> None:
        new_array = ArrayR(self.__newsize())
        for i in range(self.length):
            new_array[i] = self.array[i]
        self.array = new_array

    def append(self, item: T) -> None:
        if self.is_full():
            self.__resize()
        self.array[len(self)] = item
        self.length += 1

    def insert(self, index: int, item: T) -> None:
        if self.is_full():
            self.__resize()
        self.__shuffle_right(index)
        self.array[index] = item
        self.length += 1

    def delete_at_index(self, index: int) -> T:
        if index < 0 or index > len(self):
            raise IndexError("Out of bounds")
        item = self.array[index]
        self.length -= 1
        self.__shuffle_left(index)
        return item

    def index(self, item: T) -> int:
        for i in range(len(self)):
            if item == self.array[i]:
                return i
        raise ValueError("item not in list")

    def is_full(self):
        return len(self) >= len(self.array)

    def remove(self, item: T) -> None:
        index = self.index(item)
        self.delete_at_index(index)
     
