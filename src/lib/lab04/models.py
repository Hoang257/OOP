import sys
from pathlib import Path
from functools import cmp_to_key

project_root = Path(__file__).resolve().parents[3]

if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))


from src.lib.lab04.interfaces import Printable, Comparable

from src.lib.lab03.model import Runner as Lab03Runner
from src.lib.lab03.model import Swimmer as Lab03Swimmer
from src.lib.lab03.model import Lab03AthleteCollection

class TrainingLoadComparable(Comparable):
    def compare_to(self, other) -> int:
        if not isinstance(other, Comparable):
            raise TypeError("Объект должен реализовывать интерфейс Comparable")

        if self.training_load() > other.training_load():
            return 1

        if self.training_load() < other.training_load():
            return -1

        return 0


class Runner(Lab03Runner, Printable, TrainingLoadComparable):
    def to_string(self) -> str:
        return (
            f"Runner: {self.name}, "
            f"distance: {self.distance}m, "
            f"best time: {self.best_time}s, "
            f"training load: {self.training_load()}"
        )

class Swimmer(Lab03Swimmer, Printable, TrainingLoadComparable):
    def to_string(self) -> str:
        return (
            f"Swimmer: {self.name}, "
            f"pool distance: {self.pool_distance}m, "
            f"best time: {self.best_time}s, "
            f"style: {self.swimming_style}, "
            f"training load: {self.training_load()}"
        )

class Lab04AthleteCollection(Lab03AthleteCollection):

    def get_printable(self):
        new_collection = Lab04AthleteCollection()
        for athlete in self:
            if isinstance(athlete, Printable):
                new_collection.add(athlete)

        return new_collection

    def get_comparable(self):
        new_collection = Lab04AthleteCollection()
        for athlete in self:
            if isinstance(athlete, Comparable):
                    new_collection.add(athlete)
        return new_collection
    
    def print_all_by_interface(self):
        for athtete in self.get_printable():
            print(athtete.to_string())
    
    def sort_by_comparable(self, reverse=False):
        comparable_items = list(self.get_comparable())
        comparable_items.sort(key=cmp_to_key(lambda a, b: a.compare_to(b)),reverse=reverse)
        new_collection = Lab04AthleteCollection()
        for item in comparable_items:
            new_collection.add(item)
        return new_collection
