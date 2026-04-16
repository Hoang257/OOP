try:
    # Пакетный запуск: python -m lib.lab02.demo
    from ..lab01.model import Athlete
    from .collection import AthleteCollection
except ImportError:
    # Прямой запуск файла: python demo.py
    import sys
    from pathlib import Path

    lib_root = Path(__file__).resolve().parents[1]
    if str(lib_root) not in sys.path:
        sys.path.insert(0, str(lib_root))
    from lab01.model import Athlete
    from lab02.collection import AthleteCollection

def main():
    print("="*60)
    print("Лабораторная работа №2: Контейнерный класс AthleteCollection")
    print("="*60)

    # Создание объектов из класса Athlete
    a1 = Athlete(1, "Толя", 25, 70.5, 180.0, status=True, num_visiting=5, paid=False)
    a2 = Athlete(2, "Илья", 30, 80.0, 175.0, status=True, num_visiting=3, paid=True)
    a3 = Athlete(3, "Егор", 18, 60.0, 170.0, status=False, num_visiting=0, paid=False)
    a4 = Athlete(4, "Даша", 22, 55.0, 165.0, status=True, num_visiting=10, paid=True)
    a5 = Athlete(5, "Даня", 35, 90.0, 185.0, status=True, num_visiting=2, paid=False)

    # Создаём коллекцию team
    team = AthleteCollection()
    print("\n1.Добавление спортсменов в коллекцию:\n")
    for a in [a1, a2, a3, a4, a5]:
        try:
            team.add(a)
            print(f"Добавлен: {a.name}")
        except Exception as e:
            print(f"  Ошибка при добавлении {a.name}: {e}")

    print(f"\nВсего спортсменов: {len(team)}\n")
    print(team)   # использует __str__


    # Попытка добавить дубликат (с тем же id)
    print("\n2.Проверка на дубликат:\n")
    a_dupl = Athlete(1, "Толя_2", 26, 71.0, 180.0, True, 0, False)  # id=1 уже есть
    try:
        team.add(a_dupl)
    except ValueError as e:
        print(f"Ошибка: {e}")


    # Попытка добавить не спортсмена
    try:
        team.add("не спортсмен")
    except TypeError as e:
        print(f"Ошибка типа: {e}")


    # Поиск
    print("\n3.Поиск спортсменов:")

    found = team.find_by_id(1)
    print(f"\nПоиск по id=1: {found}")

    found = team.find_by_name("Егор")
    print(f"\nПоиск по имени 'Егор': {found}")

    not_found = team.find_by_name("Неизвестный")
    print(f"\nПоиск по несуществующему имени: {not_found}")


    # Итерация (for)
    print("\n4.Итерация по коллекции c for:")
    for athlete in team:
        print(f"-{athlete.name} (возраст {athlete.age})")


    # Удаление объекта
    print("\n5. Удаление спортсмена:\n")
    team.remove(a3)   # удаляем Егора
    print(f"После удаления {a3.name}, в колллекции осталось {len(team)} спортсменов\n")
    print(team)

    # Попытка удалить несуществующего
    try:
        team.remove(a3) # уже удалён
    except ValueError as e:
        print(f"\nУдаляем второй раз Егора: {e}")

    # Индексация и удаление по индексу
    print("\n6. Доступ по индексу и удаление по индексу:")
    print(f"\nПервый спортсмен: {team[0].name}")
    print(f"Последний спортсмен: {team[-1].name}")
    removed = team.remove_at(1) # удаляем второго
    print(f"Удалён по индексу 1: {removed.name}")
    print(f"После удаления по индексу: {len(team)} спортсменов\n")
    print(team)


    # Сортировка
    print("\n7.Сортировка по возрастания возраста:\n")
    team.sort_by_age()
    print(team)
    print("\n8.Сортировка по имени (обратный алфавитный порядок):\n")
    team.sort_by_name(reverse=True)
    print(team)


    # Фильтрация
    print("\n9.Получение только активных спортсменов:")
    active_team = team.get_active_athletes()
    print(f"Кол-во активных спортсменов: {len(active_team)}\n")
    print(active_team)


    print("\n10.Получение спортсменов по весовой категории 'Lightweight':\n")
    light_team = team.get_by_weight_category("Lightweight")
    print(light_team)


    # Дополнительно: использование len, for, get_all
    all_ids = [a.id for a in team.get_all()]
    print(f"\n11.Список всех id через get_all(): {all_ids}")


    print("\n" + "="*60)
    print("Демонстрация завершена.")

if __name__ == "__main__":
    main()