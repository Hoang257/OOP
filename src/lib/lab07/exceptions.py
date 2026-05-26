"""Собственные исключения приложения ЛР-7 (не путать с ValueError коллекции)."""


class DuplicateAthleteError(Exception):
    """Спортсмен с таким id уже есть в коллекции."""

    pass


class AthleteNotFoundError(Exception):
    """Запись с указанным id или критерием поиска не найдена."""

    pass
