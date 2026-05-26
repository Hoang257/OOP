"""
CLI ЛР-7: только меню, ввод и вывод.

Ошибки предметной области перехватываем здесь — программа не падает.
Числовой пункт меню — через try/except ValueError (как в методичке).
"""

from __future__ import annotations

from pathlib import Path
from typing import Iterable

from app import App, AthleteKind, SortKey
from exceptions import AthleteNotFoundError, DuplicateAthleteError
from models import Athlete, Runner, Swimmer


def _read_menu_choice() -> int | None:
    try:
        return int(input("Выберите пункт: ").strip())
    except ValueError:
        print("Ошибка: введите число")
        return None


def _prompt_int(msg: str) -> int:
    return int(input(msg).strip())


def _prompt_float(msg: str) -> float:
    return float(input(msg).strip().replace(",", "."))


def _prompt_bool(msg: str) -> bool:
    while True:
        s = input(msg).strip().lower()
        if s in ("y", "yes", "д", "да", "1", "true"):
            return True
        if s in ("n", "no", "н", "нет", "0", "false"):
            return False
        print("Введите y/n (или да/нет).")


def _kind_label(a: Athlete) -> str:
    if isinstance(a, Runner):
        return "Бегун"
    if isinstance(a, Swimmer):
        return "Пловец"
    return "Базовый"


def _print_table(app: App, athletes: Iterable[Athlete], title: str | None = None) -> None:
    rows = list(athletes)
    if title:
        print(title)
    if not rows:
        print("(пусто)")
        return
    hdr = ("ID", "Имя", "Тип", "Возраст", "Нагрузка", "Добавлен")
    print(" | ".join(hdr))
    print("-" * 72)
    for a in rows:
        added = app.added_at_iso(int(a.id)) or "-"
        print(
            f"{a.id} | {str(a.name)[:20]:20} | {_kind_label(a):8} | "
            f"{a.age:7} | {a.training_load():8} | {added[:19]}"
        )


def _print_detail(app: App, a: Athlete) -> None:
    print(f"---\n{a}\nТип: {_kind_label(a)}\nДобавлен: {app.added_at_iso(int(a.id)) or '-'}")


def _menu_add(app: App) -> None:
    print("Тип: 1 — атлет, 2 — бегун, 3 — пловец")
    try:
        t = _prompt_int("Тип: ")
    except ValueError:
        print("Ошибка: введите целое число")
        return
    kinds: dict[int, AthleteKind] = {1: "athlete", 2: "runner", 3: "swimmer"}
    kind = kinds.get(t)
    if kind is None:
        print("Ошибка: неверный тип")
        return
    try:
        athlete = app.build_athlete(
            kind,
            athlete_id=_prompt_int("ID: "),
            name=input("Имя: ").strip(),
            age=_prompt_int("Возраст: "),
            weight=_prompt_float("Вес (кг): "),
            height=_prompt_float("Рост (см): "),
            status=_prompt_bool("Активен? (y/n): "),
            num_visiting=_prompt_int("Число посещений: "),
            paid=_prompt_bool("Оплачено? (y/n): "),
            distance=_prompt_int("Дистанция (м): ") if kind != "athlete" else None,
            best_time=_prompt_float("Лучшее время (с): ") if kind != "athlete" else None,
            swimming_style=input("Стиль: ").strip() if kind == "swimmer" else None,
        )
        app.add_athlete(athlete)
        print("Спортсмен добавлен.")
        _print_detail(app, athlete)
    except ValueError as e:
        print(f"Ошибка: {e}")
    except DuplicateAthleteError as e:
        print(f"Ошибка: {e}")


def _menu_filter(app: App) -> None:
    print("1 — активные  2 — возраст ≥ N  3 — нагрузка ≥ N  4 — бегуны  5 — пловцы")
    try:
        c = _prompt_int("Режим: ")
    except ValueError:
        print("Ошибка: введите число")
        return
    try:
        if c == 1:
            res = app.filter_collection("active")
        elif c == 2:
            res = app.filter_collection("min_age", min_age=_prompt_int("Мин. возраст: "))
        elif c == 3:
            res = app.filter_collection("min_load", min_load=_prompt_int("Мин. нагрузка: "))
        elif c == 4:
            res = app.filter_collection("runners")
        elif c == 5:
            res = app.filter_collection("swimmers")
        else:
            print("Ошибка: неверный режим")
            return
        _print_table(app, res, "Результат фильтрации")
    except ValueError as e:
        print(f"Ошибка: {e}")


def _menu_sort(app: App) -> None:
    print("1. По имени  2. По нагрузке («цена»)  3. По дате добавления")
    try:
        c = _prompt_int("Пункт: ")
    except ValueError:
        print("Ошибка: введите число")
        return
    rev = _prompt_bool("По убыванию? (y/n): ")
    keys: dict[int, SortKey] = {1: "name", 2: "load", 3: "added_at"}
    key = keys.get(c)
    if key is None:
        print("Ошибка: неверный пункт")
        return
    app.sort_collection(key, reverse=rev)
    print("Коллекция отсортирована.")
    _print_table(app, app.list_athletes(), "Все спортсмены")


def _print_menu() -> None:
    print("\n=== Меню ЛР-7 ===")
    print("1. Добавить спортсмена")
    print("2. Показать всех")
    print("3. Найти по ID")
    print("4. Найти по имени")
    print("5. Поиск по атрибуту")
    print("6. Фильтрация")
    print("7. Сортировка")
    print("8. Изменить число посещений")
    print("9. Удалить по ID")
    print("0. Выход (сохранение в JSON)")


def run_cli() -> None:
    data = Path(__file__).resolve().parent / "data" / "athletes.json"
    app = App(data)
    app.startup_load()
    print(f"Файл данных: {data}")

    while True:
        _print_menu()
        choice = _read_menu_choice()
        if choice is None:
            continue
        if choice == 0:
            app.shutdown_save()
            print("Данные сохранены. До свидания.")
            return
        if choice == 1:
            _menu_add(app)
        elif choice == 2:
            _print_table(app, app.list_athletes(), "Все спортсмены")
        elif choice == 3:
            try:
                _print_detail(app, app.find_by_id(_prompt_int("ID: ")))
            except ValueError:
                print("Ошибка: введите целое число")
            except AthleteNotFoundError as e:
                print(f"Ошибка: {e}")
        elif choice == 4:
            name = input("Имя: ").strip()
            try:
                _print_detail(app, app.find_by_name(name))
            except AthleteNotFoundError as e:
                print(f"Ошибка: {e}")
        elif choice == 5:
            print("Атрибуты: id, name, age, weight, height, num_visiting, status, paid")
            try:
                _print_detail(
                    app,
                    app.find_by_attribute(input("Атрибут: ").strip(), input("Значение: ").strip()),
                )
            except (AthleteNotFoundError, ValueError) as e:
                print(f"Ошибка: {e}")
        elif choice == 6:
            _menu_filter(app)
        elif choice == 7:
            _menu_sort(app)
        elif choice == 8:
            try:
                a = app.update_visits(_prompt_int("ID: "), _prompt_int("Новое число посещений: "))
                print("Обновлено.")
                _print_detail(app, a)
            except ValueError:
                print("Ошибка: введите целые числа")
            except AthleteNotFoundError as e:
                print(f"Ошибка: {e}")
        elif choice == 9:
            try:
                aid = _prompt_int("ID: ")
                a = app.find_by_id(aid)
                if input(f'Удалить "{a.name}"? (y/n): ').strip().lower() != "y":
                    print("Отменено.")
                    continue
                app.remove_by_id(aid)
                print("Удалено.")
            except ValueError:
                print("Ошибка: введите целое число")
            except AthleteNotFoundError as e:
                print(f"Ошибка: {e}")
        else:
            print("Ошибка: неверный пункт меню")
