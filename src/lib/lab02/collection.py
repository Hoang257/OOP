try:
    # Пакетный запуск
    from ..lab01.model import Athlete
except ImportError:
    # Прямой запуск / импорт как top-level модуля
    import sys
    from pathlib import Path

    lib_root = Path(__file__).resolve().parents[1]
    if str(lib_root) not in sys.path:
        sys.path.insert(0, str(lib_root))
    from lab01.model import Athlete


class AthleteCollection:
    def __init__(self):
        self._athletes = [] # создаем коллекцию
    
    # Различные методы с коллекцией(добавление и удаление)
    
    def add(self, athelete): # функция добавления
        if not isinstance(athelete, Athlete): # Проверка на тип объекта
            raise TypeError("Можно добавлять только объекты Athlete")
        
        if any(a.id == athelete.id for a in self._athletes): # Проверка на существование спротсмена
            raise ValueError("Спортсмен уже существует")
        
        self._athletes.append(athelete)
    
    def remove(self, athlete):
        if athlete not in self._athletes:
            raise ValueError("Такого спорсмена нет в коллекции")
        self._athletes.remove(athlete)
    
    def remove_at(self, index): # метод удаления по индексу
        if not isinstance(index, int):
            raise TypeError("Индекс должен быть целым числом")
        if index < 0 or index > len(self._athletes):
            raise ValueError("Индекс вышел из диапазона")
        
        deleted = self._athletes.pop(index)
        return deleted
    
        
    def get_all(self):
        return self._athletes
    

    # Методы нахождения
    

    def find_by_id(self, athelete_id): # поиск по id
        for a in self._athletes:
            if a.id == athelete_id:
                return a
        return None
    
    def find_by_name(self, athlete_name): # поиск по имени
        for a in self._athletes: 
            if a.name == athlete_name:
                return a
        return None

    # Работа с коллекцией 
    
    def __len__(self): # возвращает сколько спортсменов в коллекции
        return len(self._athletes)
    
    def __iter__(self): # позволяет итерироваться по коллекции
        return iter(self._athletes)
    
    def __getitem__(self, index): # позволяет обращаться по индексу, тоесть типа среза
        return self._athletes[index]

    def sort_by(self, key, reverse=False): # сортировка по убыванию или возрастанию
        self._athletes.sort(key=key, reverse=reverse)

    # Сортироки
    
    def sort_by_name(self, reverse=False): # сортирока по алфавитному порядку
         self.sort_by(key=lambda a: a.name, reverse=reverse)

    def sort_by_age(self, reverse=False):
        self.sort_by(key=lambda a: a.age, reverse=reverse)
    
    def sort_by_weight(self, reverse=False):
        self.sort_by(key=lambda a: a.weight, reverse=reverse)

    # Вызов новых коллекций(Логические операции над коллекцией)

    def get_active_athletes(self):
        new_collection = AthleteCollection() # создаем новую коллекцию
        for a in self._athletes:
            if a.status == True: 
                new_collection.add(a) # добавляем только активных атлетов
        return new_collection
    

    def get_by_weight_category(self, category):
        new_collection = AthleteCollection() # создаем новую коллекцию
        for a in self._athletes:
            if a.weight_category() == category: 
                new_collection.add(a) # добавляем атлеты с одинаковой весовой категорией
        return new_collection
    
    
    def __str__(self): # Вывод всей коллекции
        if not self._athletes:
            return "Пустая коллекция"
        return "Коллекция: [" + ", ".join(str(a) for a in self._athletes) + "]"
    
