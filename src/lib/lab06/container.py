from __future__ import annotations
from typing import Any, Callable, Generic, Iterator, Optional, Protocol, TypeVar, runtime_checkable

T = TypeVar("T")
R = TypeVar("R")

@runtime_checkable
class Displayable(Protocol):
    """
    Protocol для объектов, которые умеют отображаться.
    Объект подходит под Displayable, если у него есть метод display().
    """

    def display(self) -> None:
        ...

@runtime_checkable
class Scorable(Protocol):
    """
    Protocol для объектов, которые умеют возвращать числовую оценку.
    Объект подходит под Scorable, если у него есть метод score().
    """

    def score(self) -> float:
        ...

D = TypeVar("D", bound=Displayable)
S = TypeVar("S", bound=Scorable)

class TypedCollection(Generic[T]):
    """
    Generic-коллекция.

    T — тип объектов, которые лежат внутри коллекции.
    Например:
    TypedCollection[Runner]
    TypedCollection[Swimmer]
    TypedCollection[Displayable]
    """

    def __init__(self, item_type: type[Any] | None = None) -> None:
        self._items: list[T] = []
        self._item_type: type[Any] | None = item_type

    def add(self, item: T) -> None:
        """
        Добавляет объект в коллекцию.

        Если при создании коллекции был передан item_type,
        то будет выполнена runtime-проверка типа.
        """
        if self._item_type is not None and not isinstance(item, self._item_type):
            raise TypeError(f"Можно добавлять только объекты типа {self._item_type.__name__}")

        self._items.append(item)

    def remove(self, item: T) -> None:
        """
        Удаляет объект из коллекции.
        """
        if item not in self._items:
            raise ValueError("Такого объекта нет в коллекции")

        self._items.remove(item)

    def remove_at(self, index: int) -> T:
        """
        Удаляет объект по индексу и возвращает его.
        """
        if not isinstance(index, int):
            raise TypeError("Индекс должен быть целым числом")

        if index < 0 or index >= len(self._items):
            raise ValueError("Индекс вышел из диапазона")

        return self._items.pop(index)

    def get_all(self) -> list[T]:
        """
        Возвращает копию списка объектов.
        """
        return list(self._items)

    def find_by_id(self, item_id: int) -> Optional[T]:
        """
        Ищет объект по id.
        Работает с объектами, у которых есть атрибут id.
        """
        for item in self._items:
            if getattr(item, "id", None) == item_id:
                return item

        return None

    def find_by_name(self, name: str) -> Optional[T]:
        """
        Ищет объект по имени.
        Работает с объектами, у которых есть атрибут name.
        """
        for item in self._items:
            if getattr(item, "name", None) == name:
                return item

        return None

    def __len__(self) -> int:
        """
        Возвращает количество объектов в коллекции.
        """
        return len(self._items)

    def __iter__(self) -> Iterator[T]:
        """
        Позволяет итерироваться по коллекции.
        """
        return iter(self._items)

    def __getitem__(self, index: int) -> T:
        """
        Позволяет обращаться к объектам по индексу.
        """
        return self._items[index]

    def sort_by(self, key: Callable[[T], Any], reverse: bool = False) -> None:
        """
        Сортирует коллекцию на месте по переданной функции.
        """
        self._items.sort(key=key, reverse=reverse)

    def sort_by_name(self, reverse: bool = False) -> None:
        """
        Сортирует коллекцию по имени.
        """
        self.sort_by(key=lambda item: getattr(item, "name", ""), reverse=reverse)

    def sort_by_age(self, reverse: bool = False) -> None:
        """
        Сортирует коллекцию по возрасту.
        """
        self.sort_by(key=lambda item: getattr(item, "age", 0), reverse=reverse)

    def sort_by_weight(self, reverse: bool = False) -> None:
        """
        Сортирует коллекцию по весу.
        """
        self.sort_by(key=lambda item: getattr(item, "weight", 0), reverse=reverse)

    def get_active_items(self) -> TypedCollection[T]:
        """
        Возвращает новую коллекцию только с активными объектами.
        Работает с объектами, у которых есть атрибут status.
        """
        new_collection: TypedCollection[T] = TypedCollection(self._item_type)

        for item in self._items:
            if getattr(item, "status", False):
                new_collection.add(item)

        return new_collection

    def get_by_weight_category(self, category: str) -> TypedCollection[T]:
        """
        Возвращает новую коллекцию объектов с заданной весовой категорией.
        Работает с объектами, у которых есть метод weight_category().
        """
        new_collection: TypedCollection[T] = TypedCollection(self._item_type)

        for item in self._items:
            if hasattr(item, "weight_category") and item.weight_category() == category:
                new_collection.add(item)

        return new_collection

    def find(self, predicate: Callable[[T], bool]) -> Optional[T]:
        """
        Возвращает первый объект, который подходит под условие.
        Если ничего не найдено, возвращает None.
        """
        for item in self._items:
            if predicate(item):
                return item

        return None

    def filter(self, predicate: Callable[[T], bool]) -> list[T]:
        """
        Возвращает список всех объектов, которые подходят под условие.
        """
        return [item for item in self._items if predicate(item)]

    def map(self, transform: Callable[[T], R]) -> list[R]:
        """
        Применяет функцию к каждому объекту и возвращает список результатов.

        R — новый тип результата.
        Например:
        T был Runner,
        а R может быть str или float.
        """
        return [transform(item) for item in self._items]

    def display_all(self: TypedCollection[D]) -> None:
        """
        Вызывает display() у всех объектов коллекции.
        Этот метод безопасен для TypedCollection[D],
        где D ограничен Protocol Displayable.
        """
        for item in self._items:
            item.display()

    def get_scores(self: TypedCollection[S]) -> list[float]:
        """
        Возвращает список score() для всех объектов коллекции.
        Этот метод безопасен для TypedCollection[S],
        где S ограничен Protocol Scorable.
        """
        return [item.score() for item in self._items]

    def __str__(self) -> str:
        """
        Строковое представление коллекции.
        """
        if not self._items:
            return "Пустая коллекция"

        return "Коллекция: [" + ", ".join(str(item) for item in self._items) + "]"