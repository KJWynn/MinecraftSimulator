from abc import ABC, abstractmethod
from typing import TypeVar, Generic
T = TypeVar('T')


class List(ABC, Generic[T]):
    def __init__(self) -> None:
        self.length = 0

    @abstractmethod
    def __setitem__(self, index: int, item: T) -> None:
        pass

    @abstractmethod
    def __getitem__(self, index: int) -> T:
        pass

    def __len__(self) -> int:
        return self.length

    def __str__(self):
        result = "["
        for i in range(len(self)):
            if i > 0:
                result += ', '
            result += str(self[i])
        result += ']'
        return result

    def append(self, item: T) -> None:
        self.insert(len(self), item)

    @abstractmethod
    def insert(self, index: int, item: T) -> None:
        pass

    def remove(self, item: T) -> None:
        index = self.index(item)
        self.delete_at_index(index)

    @abstractmethod
    def delete_at_index(self, index: int) -> T:
        pass

    @abstractmethod
    def index(self, item: T) -> int:
        pass

    def is_empty(self) -> bool:
        return len(self) == 0

    def clear(self):
        self.length = 0