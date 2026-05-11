from src.lib.lab03.model import Swimmer, Runner

# Стратегии сортировки по имени, возрасту, нагрузке, возрасту и имени
# Стратегия сортировки - это правило, по которому мы упорядочиваем список

def by_name(athlete):
    return athlete.name

def by_age(athlete):
    return athlete.age

def by_training_load(athlete):
    return athlete.training_load()

def by_name_age(athlete):
    return athlete.name, athlete.age

# Функции фильтры

def is_active(athlete):
    return athlete.status

def is_runner(athlete):
    return isinstance(athlete, Runner)

def is_swimmer(athlete):
    return isinstance(athlete, Swimmer)

# Фабрики функций

def make_min_age_filter(min_age):
    def filter(athlete):
        return athlete.training_load() >= min_age
    return filter

def make_min_training_load_filter(min_load):
    def filter(athlete):
        return athlete.training_load() >= min_load
    return filter

# функция обработчики

def activate_athlete(athelete):
    athelete.active()
    return athelete

def deactivate_athlete(athlete):
    athlete.deactive()
    return athlete


def athlete_to_string(athlete):
    return str(athlete)

# Callable-стратегии 

class AddVisitsStrategy: # добавляет атлету заданное кол-во занятий
    def __init__(self, visits):
        self.visits = visits
    
    def __call__(self, athlete):
        athlete.num_visiting = athlete.num_visiting + self.visits
        return athlete

class SetPaidStrategy: # Меняет статус оплаты спортсмена на True.
    def __call__(self, athlete):
        athlete.pay()
        return athlete