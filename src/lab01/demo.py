from model import Athlete
# создаем спортсменов
a1 = Athlete(1, "Иван Петров", 25, 70.5, 180.0, status=True, num_visiting=5, paid=False)
a2 = Athlete(2, "Петр Иванов", 30, 80.0, 175.0,status=True, num_visiting=3, paid=True)

# Проверка магических методов
# __str__
print("Десмонтсрация __str__: ", a1) # Вывод спортсменов через
# __repr__
print("Десмонтсрация __repr__: ", repr(a2))
# __eq__
a3 = Athlete(1, "Иван Сидоров", 26, 72.3, 180.0, status=True, num_visiting=7, paid=False)  # тот же ID
print("Десмонтсрация __eq__:")
print("a1 == a3?", a1 == a3)   # должно быть True (ID одинаков)
print("a1 == a2?", a1 == a2)   # False (разные ID)

# Проверка валидаций
a1.age = 26
a1.weight = 65.3
print("\nИзмениение возраста и веса спортсмена: ", f"возраст: {a1.age}, вес: {a1.weight}")

# Некоректный спортсмен
print("\nПроверка на некоректные данные спортсмена:")
try:
    bad_athlete = Athlete(-5, "", 15, -10.0, -5.0, "not_bool", -3, "yes")
except (TypeError, ValueError) as e:
    print("Ошибка при создании спортсмена:", e)
try:
    # Проверка установки возраста
    a1.age = -5  
except ValueError as e:
    print("Ошибка при установке возраста:", e)

try:
    # Проверка установки веса
    a1.weight = -5.0 
except ValueError as e:
    print("Ошибка при установке веса:", e)

# Проверка на доступ к атрибуту класса через класс
print('\nПроверка на доступ к атрибуту класса через класс')
print(f"Минимальный возраст для спортсменов: {Athlete.min_age}")
# Проверка на доступ к атрибуту класса через экземпляр
print('\nПроверка на доступ к атрибуту класса через экземпляр')
print(f"Минимальный возраст (через экземпляр): {a1.min_age}")
# Проверка бизнес методов
print("\nПопытка провести тренировку, не заплатив:")
try:
    # попытка провести тренировку, не заплатив
    a1.train(1)
except ValueError as e:
    print(e)
# после оплаты
a1.pay()
print(f"После оплаты: payment = {a1.payment}")
a1.train(1)
print(a1)

#  Проверка индекс массы тела (BMI) и весовая категория
print("\nПроверка индекс массы тела (BMI) и весовая категория: ")
print(f"BMI спортсмена {a1.name}: {a1.bmi()}")
print(f"Весовая категория: {a1.weight_category()}")

# Проверка возможности соревноваться
print("\nПроверка возможности соревноваться: ")
if a1.can_compete_with(a2):
    print(f"{a1.name} и {a2.name} могут соревноваться")
else:
    print(f"{a1.name} и {a2.name} НЕ могут соревноваться")

# Изменение состояния активности 
print("\nИзменение состояния активности:")
a2.deactive()
print(f"{a2.name} деактивирован. Статус: {a2.status}")
try:
    a2.train(1)   # попытка тренировки у неактивного
except ValueError as e:
    print("Ошибка при тренировке неактивного:", e)

a2.active()
print(f"{a2.name} активирован. Статус: {a2.status}")

print("\n" + "=" * 60)
print("ДЕМОНСТРАЦИЯ ЗАВЕРШЕНА")
print("=" * 60)


