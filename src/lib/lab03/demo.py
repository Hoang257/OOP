import sys
from pathlib import Path

project_root = Path(__file__).resolve().parents[3]

if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))


try:
    from .base import Athlete
    from .model import Runner, Swimmer, Lab03AthleteCollection
except ImportError:
    from base import Athlete
    from model import Runner, Swimmer, Lab03AthleteCollection


def main():
    print("=== Сценарий 1. Создание объектов разных типов ===\n")

    athlete = Athlete(1, "Даша", 20, 75.0, 180.0, True, 5, True)

    runner1 = Runner(2, "Маша", 21, 70.0, 178.0, True, 8, True, 100, 11.5)
    runner2 = Runner(3, "Егор", 23, 72.0, 181.0, True, 6, True, 100, 12.1)

    swimmer1 = Swimmer(4, "Даня", 19, 60.0, 170.0, True, 10, True, 50, 30.2, "Butterfly")
    swimmer2 = Swimmer(5, "Ваня", 22, 62.0, 168.0, True, 7, True, 50, 31.4, "Butterfly")

    print(athlete)
    print(runner1)
    print(swimmer1)

    print("\n=== Сценарий 2. Методы базового и дочерних классов ===\n")

    print(f"BMI обычного атлета {athlete.name}: {athlete.bmi()}")
    print(f"Весовая категория {athlete.name}: {athlete.weight_category()}")

    print(f"Средняя скорость бегуна {runner1.name}: {runner1.average_speed()} м/с")
    print(f"{swimmer1.name} проплыл за 4 круга: {swimmer1.swim_distance(4)} м")

    print("\n=== Сценарий 3. Переопределение can_compete_with() ===\n")

    print(f"{runner1.name} может соревноваться с {runner2.name}: {runner1.can_compete_with(runner2)}")
    print(f"{swimmer1.name} может соревноваться с {swimmer2.name}: {swimmer1.can_compete_with(swimmer2)}")
    print(f"{runner1.name} может соревноваться с {swimmer1.name}: {runner1.can_compete_with(swimmer1)}")

    print("\n=== Сценарий 4. Работа с коллекцией из ЛР-2 ===\n")

    collection = Lab03AthleteCollection()

    collection.add(athlete)
    collection.add(runner1)
    collection.add(runner2)
    collection.add(swimmer1)
    collection.add(swimmer2)

    collection.display_all()

    print("\n=== Сценарий 5. Полиморфизм ===\n")
    print("У всех объектов вызывается один метод training_load(), но работает он по-разному:")

    collection.show_training_loads()

    print("\n=== Сценарий 6. Проверка типов через isinstance() ===\n")

    for athlete_item in collection:
        if isinstance(athlete_item, Runner):
            print(f"{athlete_item.name} — бегун")
        elif isinstance(athlete_item, Swimmer):
            print(f"{athlete_item.name} — пловец")
        elif isinstance(athlete_item, Athlete):
            print(f"{athlete_item.name} — обычный атлет")

    print("\n=== Сценарий 7. Фильтрация по типу ===\n")

    runners = collection.get_only_runners()
    swimmers = collection.get_only_swimmers()

    print("Только бегуны:")
    runners.display_all()

    print("\nТолько пловцы:")
    swimmers.display_all()

    print("\n=== Сценарий 8. Методы коллекции из ЛР-2 ===\n")

    print(f"Количество спортсменов в коллекции: {len(collection)}")

    found = collection.find_by_name("Егор")
    print(f"Поиск по имени Егор: {found}")

    active_athletes = collection.get_active_athletes()
    print("Активные спортсмены:")
    print(active_athletes)


if __name__ == "__main__":
    main()