from abc import ABC, abstractclassmethod

class Printable(ABC):
    @abstractclassmethod
    def to_string(self) -> str:
        pass 

class Comparable(ABC):
    @abstractclassmethod
    def compare_to(self, other) -> int:
        pass

