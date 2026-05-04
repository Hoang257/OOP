import sys
from pathlib import Path

project_root = Path(__file__).resolve().parents[3]

if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

try:
    from .base import Athlete
except ImportError:
    from base import Athlete
from src.lib.lab02.collection import AthleteCollection as Lab02AthleteCollection



class Runner(Athlete):
    def __init__(self, id, name, age, weight, height, status, num_visiting, paid, distance: int, best_time: float):
        super().__init__(id, name, age, weight, height, status, num_visiting, paid)
        self._distance = distance
        self._best_time = best_time

    @property
    def distance(self):
        return self._distance
    
    @property
    def best_time(self):
        return self._best_time
    
    def average_speed(self):
        return round(self._distance / self._best_time, 2)
    
    # Переопределение бизнес-метода из базового класса
    def can_compete_with(self, other):
        if not super().can_compete_with(other):
            return False
        
        if not isinstance(other, Runner):
            return False
        
        return self.distance == other.distance
    
    # Полиморфный метод
    def training_load(self):
        return self.num_visiting * self.distance
    
    def __str__(self):
        return (
            f"{super().__str__()}, "
            f"distance {self.distance}m, "
            f"best time {self.best_time}s, "
            f"average speed {self.average_speed()} m/s"
        )

    

class Swimmer(Athlete):
    def __init__(self, id, name, age, weight, height, status, num_visiting, paid, distance: int, best_time: float, swimming_style: str):
        super().__init__(id, name, age, weight, height, status, num_visiting, paid)

        self._distance = distance
        self._best_time = best_time
        self._swimming_style = swimming_style

    @property
    def pool_distance(self):
        return self._distance
    
    @property
    def best_time(self):
        return self._best_time
    
    def swim_distance(self, laps: int):
        if not isinstance(laps, int) or laps <= 0:
            raise ValueError("Неверное количество кругов")
        return self.pool_distance * laps
    
    @property
    def swimming_style(self):
        return self._swimming_style
    
    # Переопределение бизнес-метода из базового класса
    def can_compete_with(self, other):
        if not super().can_compete_with(other):
            return False
        if  not isinstance(other, Swimmer):
            return False
        
        return (
            self.swimming_style == other.swimming_style and
            self.pool_distance == other.pool_distance
        )
    
    # Полиморфный метод
    def training_load(self):
        return self.num_visiting * self.pool_distance
    
    def __str__(self):
        return (
            f"{super().__str__()}, "
            f"pool distance {self.pool_distance}m, "
            f"best time {self.best_time}s, "
            f"style {self.swimming_style}"
        )
    
class Lab03AthleteCollection(Lab02AthleteCollection):

    def get_only_runners(self):
        new_collection = Lab03AthleteCollection()
    
        for athlete in self:
            if isinstance(athlete, Runner):
                new_collection.add(athlete)
        return new_collection


    def get_only_swimmers(self):
        new_collection = Lab03AthleteCollection()

        for athlete in self:
            if isinstance(athlete, Swimmer):
                new_collection.add(athlete)
        return new_collection
    

    def show_training_loads(self):
        for athlete in self:
            print(f"{athlete.name}: training load = {athlete.training_load()}")
        
    def display_all(self):
        for athlete in self:
            athlete.display()
