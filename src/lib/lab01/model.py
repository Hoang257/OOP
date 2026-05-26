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
    min_age: int = 16

    def __init__(self, id: int, name: str, age: int, weight: float, height: float, status: bool, num_visiting: int, paid: bool) -> None:
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
    def id(self) -> int:
        return self._id
    
    @property
    def name(self) -> str:
        return self._name
    
    @property
    def age(self) -> int:
        return self._age
    
    @age.setter
    def age(self, new_age: int) -> None:
        validate_age(new_age, self.min_age)
        self._age = new_age

    @property 
    def weight(self) -> float:
        return self._weight
    
    @weight.setter
    def weight(self, new_weight: float) -> None:
        validate_weight(new_weight)
        self._weight = new_weight
    
    @property 
    def height(self) -> float:
        return self._height
    
    @property 
    def status(self) -> bool:
        return self._status
    
    @height.setter
    def height(self, new_height: float) -> None:
        validate_height(new_height)
        self._height = new_height
    
    @property
    def num_visiting(self) -> int:
        return self._num_visiting
    
    @num_visiting.setter
    def num_visiting(self, new_num_visiting: int) -> None:
        validate_num_visiting(new_num_visiting)
        self._num_visiting = new_num_visiting
    
    @property
    def payment(self) -> bool:
        return self._paid
    
    @payment.setter
    def payment(self, value: bool) -> None:
        validate_paid(value)
        self._paid = value


# Changing the state

    def active(self) -> None:
        self._status = True
    
    def deactive(self) -> None:
        self._status = False
    
    def pay(self) -> None:
        self._paid = True

    def not_pay(self) -> None:
        self._paid = False
    
# Business methods

# Какие бизнес методы у нас будут?
# потренироваться (можно только если спортсмен активен и оплатил.)
# mbti (расчет bmi)
# соревнования (можно провести воревнования с другими участниками, если вы в одной весовой категории и разница в возрасте не выше 15)
# весовая категория (легкая, средняя, тяжелая)


    def train(self, times: int=1) -> None:
        if not self._status:
            raise ValueError("Нельзя тренироваться: спортсмен неактивен.")
        if not self._paid:
            raise ValueError("Нельзя тренироваться: спортсмен не оплатил тренировку")
        
        if not isinstance(times, int) or times  <= 0:
            raise ValueError("Нельзя уменьшить посещения")
        
        self._num_visiting += times
        self._paid = False
        print(f"{self.name} сегодня провел тренировку.Всего тренировок {self._num_visiting}")
    
    def bmi(self) -> float:
        height = self._height / 100
        return round(self._weight / (height ** 2), 2)
    
    def weight_category(self) -> str:
        if self._weight < 65:
            return "Lightweight"
        elif self._weight < 85:
            return "Middleweight"
        else:
            return "Heavyweight"
    
    def can_compete_with(self, other: object) -> bool:

        if not isinstance(other, Athlete):
            return False
        
        if self.weight_category() != other.weight_category():
            return False
        
        if abs(self._age - other._age) > 15:
            return False
        
        return True

    def __str__(self) -> str:
        status = "active" if self._status else "inactive"
        paid = "paid" if self._paid else "not paid"
        return (f"Athlete {self._name} (ID:{self._id}): age {self._age}, "
                f"weight {self._weight}kg, height {self._height}cm, "
                f"visits {self._num_visiting} ({status}, {paid})")

    def __repr__(self) -> str:
        return (f"Athlete(id={self._id}, name='{self._name}', age={self._age}, "
                f"weight={self._weight}, height={self._height}, "
                f"status={self._status}, num_visiting={self._num_visiting}, "
                f"paid={self._paid})")

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Athlete):
            return False
        return self._id == other._id
