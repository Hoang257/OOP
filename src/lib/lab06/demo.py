import sys
from pathlib import Path

project_root = Path(__file__).resolve().parents[3]

if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))


from src.lib.lab03.model import Runner, Swimmer
from src.lib.lab06.container import Displayable, Scorable, TypedCollection


def main() -> None:
    print("=== Сценарий 1. TypedCollection[Runner] и проверка типа ===\n")

    runners: TypedCollection[Runner] = TypedCollection(Runner)

    runner1 = Runner(1, "Маша", 21, 70.0, 178.0, True, 8, True, 100, 11.5)
    runner2 = Runner(2, "Егор", 23, 72.0, 181.0, True, 6, True, 100, 12.1)
    swimmer1 = Swimmer(3, "Даня", 19, 60.0, 170.0, True, 10, True, 50, 30.2, "Butterfly")

    runners.add(runner1)
    runners.add(runner2)

    print("В коллекцию бегунов добавлены:")
    for runner in runners:
        print(runner.name)

    print("\nПробуем добавить пловца в TypedCollection[Runner]:")

    try:
        runners.add(swimmer1)
    except TypeError as error:
        print("Ошибка:", error)

    print("\n=== Сценарий 2. get_all(), find(), filter() ===\n")

    all_runners = runners.get_all()

    print("Все элементы через get_all():")
    for runner in all_runners:
        print(runner.name)

    found_runner = runners.find(lambda runner: runner.name == "Маша")
    not_found_runner = runners.find(lambda runner: runner.name == "Иван")

    print("\nfind(), когда элемент найден:")
    print(found_runner)

    print("\nfind(), когда элемент не найден:")
    print(not_found_runner)

    filtered_runners = runners.filter(lambda runner: runner.age >= 22)

    print("\nfilter(), бегуны от 22 лет:")
    for runner in filtered_runners:
        print(f"{runner.name}: {runner.age}")

    print("\n=== Сценарий 3. map() меняет тип результата ===\n")

    names: list[str] = runners.map(lambda runner: runner.name)
    loads: list[float] = runners.map(lambda runner: runner.score())

    print("map() -> list[str], список имён:")
    print(names)

    print("\nmap() -> list[float], список score:")
    print(loads)

    print("\n=== Сценарий 4. Protocol Displayable ===\n")

    displayable_items: TypedCollection[Displayable] = TypedCollection(Displayable)

    displayable_items.add(runner1)
    displayable_items.add(swimmer1)

    print("Runner и Swimmer не наследуются от Displayable явно,")
    print("но подходят под Protocol, потому что у них есть display().\n")

    displayable_items.display_all()

    print("\nПроверка isinstance() с Protocol Displayable:")
    print("runner1 Displayable:", isinstance(runner1, Displayable))
    print("swimmer1 Displayable:", isinstance(swimmer1, Displayable))

    print("\n=== Сценарий 5. Protocol Scorable ===\n")

    scorable_items: TypedCollection[Scorable] = TypedCollection(Scorable)

    scorable_items.add(runner1)
    scorable_items.add(swimmer1)

    print("Runner и Swimmer подходят под Scorable, потому что у них есть score().")

    scores = scorable_items.get_scores()

    print("\nСписок score():")
    print(scores)

    print("\nПроверка isinstance() с Protocol Scorable:")
    print("runner1 Scorable:", isinstance(runner1, Scorable))
    print("swimmer1 Scorable:", isinstance(swimmer1, Scorable))


if __name__ == "__main__":
    main()