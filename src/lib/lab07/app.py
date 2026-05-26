"""
Бизнес-логика ЛР-7: коллекция Lab05, поиск, фильтры, сортировка, метаданные дат.

CLI только вызывает методы этого класса — без input/print здесь.
"""

from __future__ import annotations

from datetime import datetime
from pathlib import Path
from typing import Callable, Literal

from src.lib.lab05 import strategies as st
from src.lib.lab05.collection import Lab05AthleteCollection

from exceptions import AthleteNotFoundError, DuplicateAthleteError
from models import Athlete, Runner, Swimmer
from storage import bind_session_added_at, load, save, take_loaded_added_at_metadata

SortKey = Literal["name", "load", "added_at"]
AthleteKind = Literal["athlete", "runner", "swimmer"]
FilterMode = Literal["active", "min_age", "min_load", "runners", "swimmers"]


class App:
    """Управление коллекцией и файлом data/athletes.json."""

    def __init__(self, data_file: Path) -> None:
        self._data_file = data_file
        self._collection = Lab05AthleteCollection()
        # id -> ISO-время добавления (в моделях этого поля нет — только в JSON)
        self._added_at: dict[int, str] = {}

    @property
    def data_file(self) -> Path:
        return self._data_file

    def startup_load(self) -> None:
        """При старте: загрузка из файла, если он существует."""
        if not self._data_file.is_file():
            return
        for athlete in load(str(self._data_file)):
            try:
                self._collection.add(athlete)
            except ValueError:
                # Повреждённый JSON: пропускаем дубликат, чтобы программа запустилась
                continue
        self._added_at = take_loaded_added_at_metadata()
        # На случай записей без added_at в файле
        for athlete in self._collection:
            aid = int(athlete.id)
            if aid not in self._added_at:
                self._added_at[aid] = datetime.now().isoformat(timespec="seconds")

    def shutdown_save(self) -> None:
        """Пункт 0 меню: сохранение перед выходом."""
        bind_session_added_at(dict(self._added_at))
        save(self._collection, str(self._data_file))

    def list_athletes(self) -> list[Athlete]:
        return list(self._collection)

    def added_at_iso(self, athlete_id: int) -> str | None:
        return self._added_at.get(int(athlete_id))

    def add_athlete(self, athlete: Athlete) -> None:
        try:
            self._collection.add(athlete)
        except ValueError as exc:
            raise DuplicateAthleteError(str(exc)) from exc
        self._added_at[int(athlete.id)] = datetime.now().isoformat(timespec="seconds")

    def remove_by_id(self, athlete_id: int) -> Athlete:
        athlete = self._collection.find_by_id(int(athlete_id))
        if athlete is None:
            raise AthleteNotFoundError("Спортсмен с таким ID не найден")
        self._collection.remove(athlete)
        self._added_at.pop(int(athlete_id), None)
        return athlete

    def find_by_id(self, athlete_id: int) -> Athlete:
        athlete = self._collection.find_by_id(int(athlete_id))
        if athlete is None:
            raise AthleteNotFoundError("Спортсмен с таким ID не найден")
        return athlete

    def find_by_name(self, name: str) -> Athlete:
        athlete = self._collection.find_by_name(str(name).strip())
        if athlete is None:
            raise AthleteNotFoundError("Спортсмен с таким именем не найден")
        return athlete

    def find_by_attribute(self, attr: str, raw_value: str) -> Athlete:
        """Поиск по полю: id, name, age, weight, height, num_visiting, status, paid."""
        pred = self._predicate(attr, raw_value)
        found = self._collection.filter_by(pred)
        if len(found) == 0:
            raise AthleteNotFoundError("Подходящий спортсмен не найден")
        return found[0]

    def filter_collection(
        self,
        mode: FilterMode,
        *,
        min_age: int | None = None,
        min_load: int | None = None,
    ) -> Lab05AthleteCollection:
        """Фильтрация через стратегии ЛР5 (новая коллекция, исходная не меняется)."""
        if mode == "active":
            return self._collection.filter_by(st.is_active)
        if mode == "runners":
            return self._collection.filter_by(st.is_runner)
        if mode == "swimmers":
            return self._collection.filter_by(st.is_swimmer)
        if mode == "min_age":
            if min_age is None:
                raise ValueError("Не задан минимальный возраст")
            n = int(min_age)
            return self._collection.filter_by(lambda a: int(a.age) >= n)
        if mode == "min_load":
            if min_load is None:
                raise ValueError("Не задана минимальная нагрузка")
            return self._collection.filter_by(st.make_min_training_load_filter(int(min_load)))
        raise ValueError("Неизвестный режим фильтрации")

    def sort_collection(self, key: SortKey, *, reverse: bool = False) -> None:
        """
        Сортировка на месте.

        load — тренировочная нагрузка (аналог «цены» в учебном примере с книгами).
        added_at — дата из JSON-метаданных.
        """
        if key == "name":
            self._collection = self._collection.sort_by(st.by_name, reverse=reverse)
        elif key == "load":
            self._collection = self._collection.sort_by(st.by_training_load, reverse=reverse)
        elif key == "added_at":

            def by_date(a: Athlete) -> datetime:
                iso = self._added_at.get(int(a.id))
                if not iso:
                    return datetime.min
                try:
                    return datetime.fromisoformat(iso)
                except ValueError:
                    return datetime.min

            self._collection = self._collection.sort_by(by_date, reverse=reverse)
        else:
            raise ValueError("Неизвестный ключ сортировки")

    def update_visits(self, athlete_id: int, visits: int) -> Athlete:
        athlete = self.find_by_id(athlete_id)
        athlete.num_visiting = int(visits)
        return athlete

    def build_athlete(
        self,
        kind: AthleteKind,
        *,
        athlete_id: int,
        name: str,
        age: int,
        weight: float,
        height: float,
        status: bool,
        num_visiting: int,
        paid: bool,
        distance: int | None = None,
        best_time: float | None = None,
        swimming_style: str | None = None,
    ) -> Athlete:
        """Создаёт объект без добавления в коллекцию (валидация — в моделях ЛР1)."""
        base = (
            athlete_id,
            name,
            age,
            weight,
            height,
            status,
            num_visiting,
            paid,
        )
        if kind == "athlete":
            return Athlete(*base)
        if kind == "runner":
            if distance is None or best_time is None:
                raise ValueError("Для бегуна укажите distance и best_time")
            return Runner(*base, int(distance), float(best_time))
        if kind == "swimmer":
            if distance is None or best_time is None or not (swimming_style or "").strip():
                raise ValueError("Для пловца укажите distance, best_time и стиль")
            return Swimmer(*base, int(distance), float(best_time), str(swimming_style).strip())
        raise ValueError("Неизвестный тип")

    def _predicate(self, attr: str, raw: str) -> Callable[[Athlete], bool]:
        key = attr.strip().lower()
        val = raw.strip()
        if key == "id":
            i = int(val)
            return lambda a: int(a.id) == i
        if key == "name":
            return lambda a: str(a.name) == val
        if key == "age":
            i = int(val)
            return lambda a: int(a.age) == i
        if key == "weight":
            f = float(val.replace(",", "."))
            return lambda a: float(a.weight) == f
        if key == "height":
            f = float(val.replace(",", "."))
            return lambda a: float(a.height) == f
        if key == "num_visiting":
            i = int(val)
            return lambda a: int(a.num_visiting) == i
        if key in ("status", "active"):
            b = self._parse_bool(val)
            return lambda a: bool(a.status) == b
        if key in ("paid", "payment"):
            b = self._parse_bool(val)
            return lambda a: bool(a.payment) == b
        raise ValueError(f"Поиск по атрибуту '{key}' не поддерживается")

    @staticmethod
    def _parse_bool(s: str) -> bool:
        t = s.lower()
        if t in ("1", "true", "t", "yes", "y", "да", "д"):
            return True
        if t in ("0", "false", "f", "no", "n", "нет", "н"):
            return False
        raise ValueError("Ожидалось да/нет или true/false")
