from abc import ABC, abstractmethod
from datetime import date
from collections import defaultdict
from typing import Callable, Any

from datetime import date
import math

class Workout:
    def __init__(self, 
                athlete_name: str,
                exercise_type: str,
                duration_min: int, 
                calories_burned: float,
                workout_date: date):
        
        self.__athlete_name = athlete_name
        self.__exercise_type = exercise_type.strip()
        self.__duration_min = duration_min
        self.__calories_burned = float(calories_burned)
        self.__date = workout_date
        
    # Валидации:

        if not isinstance(athlete_name, str):
            raise TypeError("Имя спортсмена должно быть строкой")
        athlete_name = athlete_name.strip()
        if not athlete_name:
            raise ValueError("Имя спортсмена не может быть пустым")


        if not isinstance(exercise_type, str):
            raise TypeError("Тип упражнения должен быть строкой")
        if not exercise_type.strip():
            raise ValueError("Тип упражнения не может быть пустым")


        if not isinstance(duration_min, int):
            raise TypeError("Длительность должна быть целым числом")
        if not (1 <= duration_min <= 600):
            raise ValueError("Длительность должна быть от 1 до 600 минут")


        if not isinstance(calories_burned, (int, float)):
            raise TypeError("Калории должны быть числом")
        if calories_burned <= 0:
            raise ValueError("Калории должны быть положительным числом")


        if not isinstance(workout_date, date):
            raise TypeError("Дата должна быть объектом datetime.date")
        if workout_date > date.today():
            raise ValueError("Дата не может быть в будущем")



    # Свойства @property только для чтения

    @property
    def athlete_name(self) -> str:
        return self.__athlete_name

    @property
    def exercise_type(self) -> str:
        return self.__exercise_type

    @property
    def duration_min(self) -> int:
        return self.__duration_min

    @property
    def calories_burned(self) -> float:
        return self.__calories_burned

    @property
    def date(self) -> date:
        return self.__date
    
    # Методы:

    def intensity(self) -> float:
        return self.__calories_burned / self.__duration_min

    def is_intense(self) -> bool:
        """True, если интенсивность > 10."""
        return self.intensity() > 10

    def __str__(self) -> str:
        return (f"{self.__athlete_name} — {self.__exercise_type}, "
                f"{self.__duration_min} мин, "
                f"{int(self.__calories_burned)} ккал "
                f"({self.__date.isoformat()})")

    def __eq__(self, other) -> bool:
        if not isinstance(other, Workout):
            return NotImplemented
        return (self.__athlete_name == other.__athlete_name and
                self.__date == other.__date and
                self.__exercise_type == other.__exercise_type)

    def __lt__(self, other) -> bool:
        if not isinstance(other, Workout):
            return NotImplemented
        return self.__date < other.__date

class WorkoutJournal:
    def __init__(self):
        self._workouts = []

    def add(self, workout: Workout) -> None:
        if not isinstance(workout, Workout):
            raise TypeError("Можно добавлять только объекты Workout")
        self._workouts.append(workout)

    def __iter__(self):
        return iter(self._workouts)

    def __len__(self) -> int:
        return len(self._workouts)

    def filter_by(self, predicate: Callable[[Workout], bool]) -> 'WorkoutJournal':
        new_journal = WorkoutJournal()
        for w in filter(predicate, self._workouts):
            new_journal.add(w)
        return new_journal

    def map_to(self, transform_func: Callable[[Workout], Any]) -> list:
        return list(map(transform_func, self._workouts))

    def apply(self, func: Callable[[Workout], None]) -> 'WorkoutJournal':
        for w in self._workouts:
            func(w)
        new_journal = WorkoutJournal()
        for w in self._workouts:
            new_journal.add(w)
        return new_journal

    def set_analytics(self, strategy: 'AnalyticsStrategy') -> None:
        self._analytics_strategy = strategy

    def get_report(self) -> dict:
        if not hasattr(self, '_analytics_strategy'):
            raise ValueError("Стратегия анализа не установлена. Используйте set_analytics().")
        return self._analytics_strategy.analyze(list(self._workouts))


class AnalyticsStrategy(ABC):
    @abstractmethod
    def analyze(self, workouts: list) -> dict:
        pass


class TotalStats(AnalyticsStrategy):
    def analyze(self, workouts: list) -> dict:
        total_workouts = len(workouts)
        total_minutes = sum(w.duration_min for w in workouts)
        total_calories = sum(w.calories_burned for w in workouts)
        return {
            "total_workouts": total_workouts,
            "total_minutes": total_minutes,
            "total_calories": total_calories
        }


class AverageStats(AnalyticsStrategy):
    def analyze(self, workouts: list) -> dict:
        if not workouts:
            return {
                "avg_duration": 0.0,
                "avg_calories": 0.0,
                "avg_intensity": 0.0
            }
        n = len(workouts)
        avg_duration = sum(w.duration_min for w in workouts) / n
        avg_calories = sum(w.calories_burned for w in workouts) / n
        avg_intensity = sum(w.intensity() for w in workouts) / n
        return {
            "avg_duration": round(avg_duration, 1),
            "avg_calories": round(avg_calories, 1),
            "avg_intensity": round(avg_intensity, 1)
        }


class ByExerciseStats(AnalyticsStrategy):
    def analyze(self, workouts: list) -> dict:
        stats = defaultdict(lambda: {"count": 0, "total_calories": 0})
        for w in workouts:
            stats[w.exercise_type]["count"] += 1
            stats[w.exercise_type]["total_calories"] += w.calories_burned
        return dict(stats)



def make_intensity_filter(min_intensity: float) -> Callable[[Workout], bool]:
    return lambda w: w.intensity() >= min_intensity


def make_date_range_filter(start_date: date, end_date: date) -> Callable[[Workout], bool]:
    return lambda w: start_date <= w.date <= end_date


def make_exercise_filter(exercise_type: str) -> Callable[[Workout], bool]:
    return lambda w: w.exercise_type == exercise_type



