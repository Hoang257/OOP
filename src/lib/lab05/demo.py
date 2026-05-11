import sys
from pathlib import Path

project_root = Path(__file__).resolve().parents[3]

if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))


from src.lib.lab03.model import Runner, Swimmer
from src.lib.lab05.collection import Lab05AthleteCollection
from src.lib.lab05.strategies import by_name, by_age, by_training_load, by_name_age, is_active, is_runner, is_swimmer, make_min_age_filter, make_min_training_load_filter, deactivate_athlete, athlete_to_string, AddVisitsStrategy, SetPaidStrategy


def main():
    print("=== Сценарий 1. Создание коллекции ===\n")

    collection = Lab05AthleteCollection()

    runner1 = Runner(2, "Маша", 21, 70.0, 178.0, True, 8, True, 100, 11.5)
    runner2 = Runner(3, "Егор", 23, 72.0, 181.0, True, 6, True, 100, 12.1)

    swimmer1 = Swimmer(4, "Даня", 19, 60.0, 170.0, True, 10, True, 50, 30.2, "Butterfly")
    swimmer2 = Swimmer(5, "Ваня", 22, 62.0, 168.0, True, 7, True, 50, 31.4, "Butterfly")

    collection.add(runner1)
    collection.add(runner2)
    collection.add(swimmer1)
    collection.add(swimmer2)

    print("Исходные спортсмены:")
    for athlete in collection:
        print(athlete)

    print("\n=== Сценарий 2. Сортировка тремя стратегиями ===\n")

    print("Сортировка по имени:")
    for athlete in collection.sort_by(by_name):
        print(athlete.name)

    print("\nСортировка по возрасту:")
    for athlete in collection.sort_by(by_age):
        print(f"{athlete.name}: {athlete.age}")

    print("\nСортировка по тренировочной нагрузке:")
    for athlete in collection.sort_by(by_training_load, reverse=True):
        print(f"{athlete.name}: {athlete.training_load()}")

    print("\n=== Сценарий 3. Фильтрация двумя разными функциями ===\n")

    print("Только активные спортсмены через filter():")
    active_athletes = list(filter(is_active, collection))
    for athlete in active_athletes:
        print(f"{athlete.name}: active={athlete.status}")

    print("\nТолько бегуны через filter_by():")
    for athlete in collection.filter_by(is_runner):
        print(f"{athlete.name}: {athlete.__class__.__name__}")

    print("\nТолько пловцы через filter_by():")
    for athlete in collection.filter_by(is_swimmer):
        print(f"{athlete.name}: {athlete.__class__.__name__}")

    print("\n=== Сценарий 4. map() для преобразования коллекции ===\n")

    names = list(map(lambda athlete: athlete.name, collection))
    print("Имена спортсменов:")
    print(names)

    string_objects = list(map(athlete_to_string, collection))
    print("\nОбъекты, преобразованные в строки:")
    for item in string_objects:
        print(item)

    print("\n=== Сценарий 5. Фабрика функций ===\n")

    min_age_filter = make_min_age_filter(21)
    print("Спортсмены от 21 года:")
    for athlete in collection.filter_by(min_age_filter):
        print(f"{athlete.name}: {athlete.age}")

    min_load_filter = make_min_training_load_filter(700)
    print("\nСпортсмены с нагрузкой от 700:")
    for athlete in collection.filter_by(min_load_filter):
        print(f"{athlete.name}: {athlete.training_load()}")

    print("\n=== Сценарий 6. Lambda и именованная функция ===\n")

    print("Сортировка по имени через lambda:")
    for athlete in collection.sort_by(lambda athlete: athlete.name):
        print(athlete.name)

    print("\nСортировка по имени через именованную функцию by_name:")
    for athlete in collection.sort_by(by_name):
        print(athlete.name)

    print("\n=== Сценарий 7. Цепочка filter → sort → apply ===\n")

    result = (
        collection
        .filter_by(is_active)
        .sort_by(by_name_age)
        .apply(deactivate_athlete)
    )

    print("Активные → сортировка по возрасту и имени → деактивация:")
    for athlete in result:
        print(f"{athlete.name}: age={athlete.age}, active={athlete.status}")

    print("\n=== Сценарий 8. Замена стратегии без изменения коллекции ===\n")

    print("Стратегия 1: сортировка по имени:")
    for athlete in collection.sort_by(by_name):
        print(athlete.name)

    print("\nСтратегия 2: сортировка по нагрузке:")
    for athlete in collection.sort_by(by_training_load, reverse=True):
        print(f"{athlete.name}: {athlete.training_load()}")

    print("\n=== Сценарий 9. Callable-объект как стратегия ===\n")

    add_visits = AddVisitsStrategy(2)
    paid_strategy = SetPaidStrategy()

    print("После AddVisitsStrategy(+2 посещения):")
    for athlete in collection.apply(add_visits):
        print(f"{athlete.name}: visits={athlete.num_visiting}")

    print("\nПосле SetPaidStrategy:")
    for athlete in collection.apply(paid_strategy):
        print(f"{athlete.name}: paid={athlete.payment}")


if __name__ == "__main__":
    main()