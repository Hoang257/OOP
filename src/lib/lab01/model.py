try:
    # Пакетный импорт
    from .validate import (
        validate_id,
        validate_name,
        validate_age,
        validate_weight,
        validate_height,
        validate_status,
        validate_num_visiting,
        validate_paid,
    )
except ImportError:
    # Прямой запуск файла
    from validate import (
        validate_id,
        validate_name,
        validate_age,
        validate_weight,
        validate_height,
        validate_status,
        validate_num_visiting,
        validate_paid,
    )
class Athlete:
    min_age = 16

    def __init__(self, id: int, name: str, age: int, weight: float, height: float, status: bool, num_visiting: int, paid: bool):
        validate_id(id)
        validate_name(name)
        validate_age(age, self.min_age)
        validate_weight(weight)
        validate_height(height)
        validate_status(status)
        validate_num_visiting(num_visiting)
        validate_paid(paid)

        self._id = id 
        self._name = name 
        self._age = age 
        self._weight = weight 
        self._height = height 
        self._status = status 
        self._num_visiting = num_visiting 
        self._paid = paid

    @property
    def id(self):
        return self._id
    
    @property
    def name(self):
        return self._name
    
    @property
    def age(self):
        return self._age
    
    @age.setter
    def age(self, new_age):
        validate_age(new_age, self.min_age)
        self._age = new_age

    @property 
    def weight(self):
        return self._weight
    
    @weight.setter
    def weight(self, new_weight):
        validate_weight(new_weight)
        self._weight = new_weight
    
    @property 
    def height(self):
        return self._height
    
    @property 
    def status(self):
        return self._status
    
    @height.setter
    def height(self, new_height):
        validate_height(new_height)
        self._height = new_height
    
    @property
    def num_visiting(self):
        return self._num_visiting
    
    @num_visiting.setter
    def num_visiting(self, new_num_visiting):
        validate_num_visiting(new_num_visiting)
        self._num_visiting = new_num_visiting
    
    @property
    def payment(self):
        return self._paid
    
    @payment.setter
    def payment(self, value):
        validate_paid(value)
        self._paid = value


# Changing the state

    def active(self):
        self._status = True
    
    def deactive(self):
        self._status = False
    
    def pay(self):
        self._paid = True

    def not_pay(self):
        self._paid = False
    
# Business methods

# Какие бизнес методы у нас будут?
# потренироваться (можно только если спортсмен активен и оплатил.)
# mbti (расчет bmi)
# соревнования (можно провести воревнования с другими участниками, если вы в одной весовой категории и разница в возрасте не выше 15)
# весовая категория (легкая, средняя, тяжелая)


    def train(self, times=1):
        if not self._status:
            raise ValueError("Нельзя тренироваться: спортсмен неактивен.")
        if not self._paid:
            raise ValueError("Нельзя тренироваться: спортсмен не оплатил тренировку")
        
        if not isinstance(times, int) or times  <= 0:
            raise ValueError("Нельзя уменьшить посещения")
        
        self._num_visiting += times
        self._paid = False
        print(f"{self.name} сегодня провел тренировку.Всего тренировок {self._num_visiting}")
    
    def bmi(self):
        height = self._height / 100
        return round(self._weight / (height ** 2), 2)
    
    def weight_category(self):
        if self._weight < 65:
            return "Lightweight"
        elif self._weight < 85:
            return "Middleweight"
        else:
            return "Heavyweight"
    
    def can_compete_with(self, other):

        if not isinstance(other, Athlete):
            return False
        
        if self.weight_category() != other.weight_category():
            return False
        
        if abs(self._age - other._age) > 15:
            return False
        
        return True

    def __str__(self):
        status = "active" if self._status else "inactive"
        paid = "paid" if self._paid else "not paid"
        return (f"Athlete {self._name} (ID:{self._id}): age {self._age}, "
                f"weight {self._weight}kg, height {self._height}cm, "
                f"visits {self._num_visiting} ({status}, {paid})")

    def __repr__(self):
        return (f"Athlete(id={self._id}, name='{self._name}', age={self._age}, "
                f"weight={self._weight}, height={self._height}, "
                f"status={self._status}, num_visiting={self._num_visiting}, "
                f"paid={self._paid})")

    def __eq__(self, other):
        if not isinstance(other, Athlete):
            return False
        return self._id == other._id
