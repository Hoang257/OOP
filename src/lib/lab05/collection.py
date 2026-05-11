from src.lib.lab03.model import Lab03AthleteCollection
# Сортирует коллекцию по переданной функции-стратегии, возвращает новую коллекцию.
# key_func - по чему сортировать
class Lab05AthleteCollection(Lab03AthleteCollection):
    def sort_by(self, key_func, reverse=False):
        sorted_items = sorted(self, key=key_func, reverse=reverse)
        new_collection = Lab05AthleteCollection()
        for athlete in sorted_items:
            new_collection.add(athlete)
        return new_collection

    # Фильтрует коллекцию по переданной функции-предикату.
    # predicate — это функция-фильтр. Она возвращает True или False.
    def filter_by(self, predicate):
            filtered_items = filter(predicate, self)
            new_collection = Lab05AthleteCollection()
            for athlete in filtered_items:
                new_collection.add(athlete)
            return new_collection

    # Применяет произвольную функцию ко всем элементам коллекции.
    def apply(self, func):
            new_collection = Lab05AthleteCollection()
            for athlete in self:
                result = func(athlete)
                new_collection.add(result)
            return new_collection

    #Удобный метод для вывода коллекции.
    def show(self, title=None):
            if title:
                print(title)
            for athlete in self:
                print(athlete)
            return self

