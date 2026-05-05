import sys
from pathlib import Path

project_root = Path(__file__).resolve().parents[3]

if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))


from src.lib.lab04.interfaces import Printable, Comparable
from src.lib.lab04.models import Runner, Swimmer, Lab04AthleteCollection


def print_all(items: list[Printable]):
    """
    Универсальная функция.
    Работает через интерфейс Printable.
    """
    for item in items:
        print(item.to_string())


def compare_two(first: Comparable, second: Comparable):
    """
    Универсальная функция.
    Работает через интерфейс Comparable.
    """
    result = first.compare_to(second)

    if result > 0:
        print(f"{first.name} has bigger training load than {second.name}")
    elif result < 0:
        print(f"{first.name} has smaller training load than {second.name}")
    else:
        print(f"{first.name} and {second.name} have equal training load")


def main():
    print("=== Сценарий 1. Создание объектов разных типов ===\n")

    runner1 = Runner(2, "Маша", 21, 70.0, 178.0, True, 8, True, 100, 11.5)
    runner2 = Runner(3, "Егор", 23, 72.0, 181.0, True, 6, True, 100, 12.1)

    swimmer1 = Swimmer(4, "Даня", 19, 60.0, 170.0, True, 10, True, 50, 30.2, "Butterfly")
    swimmer2 = Swimmer(5, "Ваня", 22, 62.0, 168.0, True, 7, True, 50, 31.4, "Butterfly")

    print(runner1)
    print(runner2)
    print(swimmer1)
    print(swimmer2)

    print("\n=== Сценарий 2. Вызов интерфейсного метода to_string() ===\n")

    print(runner1.to_string())
    print(swimmer1.to_string())

    print("\n=== Сценарий 3. Универсальная функция print_all() ===\n")

    items = [runner1, runner2, swimmer1, swimmer2]
    print_all(items)

    print("\n=== Сценарий 4. Интерфейс Comparable ===\n")

    compare_two(runner1, swimmer1)
    compare_two(runner2, swimmer2)

    print("\n=== Сценарий 5. Проверка через isinstance() ===\n")

    for item in items:
        print(f"{item.name} is Printable: {isinstance(item, Printable)}")
        print(f"{item.name} is Comparable: {isinstance(item, Comparable)}")
        print("---")

    print("\n=== Сценарий 6. Работа с коллекцией через интерфейсы ===\n")

    collection = Lab04AthleteCollection()

    collection.add(runner1)
    collection.add(runner2)
    collection.add(swimmer1)
    collection.add(swimmer2)

    print("Вывод через Printable:")
    collection.print_all_by_interface()

    print("\n=== Сценарий 7. Фильтрация по Printable ===\n")

    printable_collection = collection.get_printable()

    for item in printable_collection:
        print(item.to_string())

    print("\n=== Сценарий 8. Фильтрация по Comparable ===\n")

    comparable_collection = collection.get_comparable()

    for item in comparable_collection:
        print(f"{item.name}: training load = {item.training_load()}")

    print("\n=== Сценарий 9. Сортировка через Comparable ===\n")

    sorted_collection = collection.sort_by_comparable(reverse=True)

    for item in sorted_collection:
        print(f"{item.name}: training load = {item.training_load()}")


if __name__ == "__main__":
    main()