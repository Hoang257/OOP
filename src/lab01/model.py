class Athlete:
    
    def __init__(self, id: int, name: str, age: int, weight: float, height: float, status: bool, num_visiting: int):

        self._id = id 
        self._name = name 
        self._age = age 
        self._weight = weight 
        self._height = height 
        self._status = True 
        self._num_visiting = num_visiting 

    @property
    def name(self):
        return self._name 
    
    @property
    def name(self):
        return self.name
    
    @name.setter
    def name(self, )