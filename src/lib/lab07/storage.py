"""
Сохранение и загрузка коллекции в JSON (критерий на оценку 5).

Сигнатуры по методичке: save(collection, filepath) и load(filepath) -> list.
Дата добавления хранится в JSON, не в классах Athlete/Runner/Swimmer.
"""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path
from typing import Any

from src.lib.lab05.collection import Lab05AthleteCollection

from models import Athlete, Runner, Swimmer

# Метаданные после load — забирает app через take_loaded_added_at_metadata()
_LAST_ADDED_AT: dict[int, str] = {}
# Перед save app передаёт актуальные даты сессии через bind_session_added_at()
_SESSION_ADDED_AT: dict[int, str] = {}


def bind_session_added_at(meta: dict[int, str]) -> None:
    """Служебно: app передаёт id -> ISO-дата перед записью на диск."""
    _SESSION_ADDED_AT.clear()
    _SESSION_ADDED_AT.update(meta)


def take_loaded_added_at_metadata() -> dict[int, str]:
    """Возвращает даты добавления из последнего load и очищает буфер."""
    out = dict(_LAST_ADDED_AT)
    _LAST_ADDED_AT.clear()
    return out


def _record_to_athlete(data: dict[str, Any]) -> Athlete:
    """Восстанавливает объект из словаря JSON."""
    kind = str(data.get("kind", "athlete"))
    common = (
        int(data["id"]),
        str(data["name"]),
        int(data["age"]),
        float(data["weight"]),
        float(data["height"]),
        bool(data["status"]),
        int(data["num_visiting"]),
        bool(data["paid"]),
    )
    if kind == "runner":
        return Runner(*common, int(data["distance"]), float(data["best_time"]))
    if kind == "swimmer":
        return Swimmer(
            *common,
            int(data["distance"]),
            float(data["best_time"]),
            str(data["swimming_style"]),
        )
    return Athlete(*common)


def _athlete_to_record(athlete: Athlete, added_at: str | None) -> dict[str, Any]:
    """Сериализует одного спортсмена в словарь для JSON."""
    rec: dict[str, Any] = {
        "kind": "athlete",
        "id": athlete.id,
        "name": athlete.name,
        "age": athlete.age,
        "weight": float(athlete.weight),
        "height": float(athlete.height),
        "status": bool(athlete.status),
        "num_visiting": int(athlete.num_visiting),
        "paid": bool(athlete.payment),
        "added_at": added_at,
    }
    if isinstance(athlete, Runner):
        rec["kind"] = "runner"
        rec["distance"] = int(athlete.distance)
        rec["best_time"] = float(athlete.best_time)
    elif isinstance(athlete, Swimmer):
        rec["kind"] = "swimmer"
        rec["distance"] = int(athlete.pool_distance)
        rec["best_time"] = float(athlete.best_time)
        rec["swimming_style"] = str(athlete.swimming_style)
    return rec


def save(collection: Lab05AthleteCollection, filepath: str) -> None:
    """Сохранить коллекцию в JSON-файл (формат методички)."""
    path = Path(filepath)
    path.parent.mkdir(parents=True, exist_ok=True)
    # Старые даты из файла — чтобы не потерять при пересохранении без новых id
    disk_dates: dict[int, str] = {}
    if path.is_file():
        try:
            raw = json.loads(path.read_text(encoding="utf-8"))
            for rec in raw.get("records", []):
                if isinstance(rec, dict) and "id" in rec and rec.get("added_at"):
                    disk_dates[int(rec["id"])] = str(rec["added_at"])
        except (OSError, json.JSONDecodeError):
            pass

    records = []
    for athlete in collection:
        aid = int(athlete.id)
        added = (
            _SESSION_ADDED_AT.get(aid)
            or disk_dates.get(aid)
            or datetime.now().isoformat(timespec="seconds")
        )
        records.append(_athlete_to_record(athlete, added))

    path.write_text(
        json.dumps({"version": 1, "records": records}, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )


def load(filepath: str) -> list:
    """
    Загрузить список объектов из JSON.

    Даты добавления — во внутреннем буфере; заберите через take_loaded_added_at_metadata().
    """
    _LAST_ADDED_AT.clear()
    path = Path(filepath)
    if not path.is_file():
        return []
    raw = json.loads(path.read_text(encoding="utf-8"))
    athletes: list[Athlete] = []
    for rec in raw.get("records", []):
        if not isinstance(rec, dict):
            continue
        athlete = _record_to_athlete(rec)
        athletes.append(athlete)
        at = rec.get("added_at")
        if isinstance(at, str) and at.strip():
            _LAST_ADDED_AT[int(athlete.id)] = at.strip()
    return athletes
